"""
=====================================================================
سكريبت اختبار شامل — نظام تشخيص أمراض النباتات
=====================================================================
يُفحص:
  1. Syntax  — كل ملف يُحلَّل بدون خطأ
  2. تكرار أسماء الدوال — لا تكرار بين الملفات
  3. المخالفات — لا for/while/listcomp/generator داخل @Rule
  4. salience — كل قاعدة لها أولوية صحيحة
  5. halt()   — كل قاعدة علاج تنتهي بـ halt()
  6. تشغيل حي — كل engine يشتغل مع أعراض حقيقية ويُنتج تشخيصاً

طريقة التشغيل:
  ضع هذا الملف في نفس مجلد المشروع ثم:
      python test_project.py
=====================================================================
"""

import ast
import re
import sys
import os
import traceback

# ── ألوان الطرفية ──────────────────────────────────────────────────
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

def ok(msg):   print(f"  {GREEN}✅ {msg}{RESET}")
def fail(msg): print(f"  {RED}🔴 {msg}{RESET}")
def warn(msg): print(f"  {YELLOW}⚠️  {msg}{RESET}")
def section(title):
    print(f"\n{BOLD}{CYAN}{'='*60}{RESET}")
    print(f"{BOLD}{CYAN}  {title}{RESET}")
    print(f"{BOLD}{CYAN}{'='*60}{RESET}")

# ── ملفات المشروع ──────────────────────────────────────────────────
RULE_FILES = [
    'apple_rules.py', 'cherry_rules.py', 'citrus_rules.py',
    'eggplant_rules.py', 'garlic_rules.py', 'grape_rules.py',
    'onion_rules.py', 'Potato_rules.py', 'tomato_rules.py',
    'zucchini_rules.py',
]
ALL_FILES = RULE_FILES + ['core.py', 'main.py']

results = {'passed': 0, 'failed': 0, 'warnings': 0}

def record(passed, message):
    if passed:
        ok(message)
        results['passed'] += 1
    else:
        fail(message)
        results['failed'] += 1

# ══════════════════════════════════════════════════════════════════
# TEST 1 — Syntax
# ══════════════════════════════════════════════════════════════════
section("TEST 1 — Syntax (كل ملف يُقرأ بدون خطأ)")

for fname in ALL_FILES:
    if not os.path.exists(fname):
        fail(f"{fname}: الملف غير موجود!")
        results['failed'] += 1
        continue
    try:
        with open(fname, encoding='utf-8') as f:
            source = f.read()
        ast.parse(source)
        record(True, f"{fname}")
    except SyntaxError as e:
        record(False, f"{fname}: SyntaxError سطر {e.lineno} — {e.msg}")
    except Exception as e:
        record(False, f"{fname}: {e}")

# ══════════════════════════════════════════════════════════════════
# TEST 2 — تكرار أسماء الدوال
# ══════════════════════════════════════════════════════════════════
section("TEST 2 — لا تكرار في أسماء دوال @Rule")

all_funcs = {}
for fname in RULE_FILES:
    if not os.path.exists(fname): continue
    with open(fname, encoding='utf-8') as f:
        source = f.read()
    for m in re.finditer(r'^\s{4}def (\w+)\s*\(', source, re.MULTILINE):
        fn = m.group(1)
        all_funcs.setdefault(fn, []).append(fname)

dups = {k: v for k, v in all_funcs.items() if len(v) > 1}
if dups:
    for fn, fnames in sorted(dups.items()):
        record(False, f"'{fn}' مكررة في: {', '.join(fnames)}")
else:
    record(True, f"كل {len(all_funcs)} دالة فريدة")

# ══════════════════════════════════════════════════════════════════
# TEST 3 — لا مخالفات للحلقات داخل @Rule
# ══════════════════════════════════════════════════════════════════
section("TEST 3 — لا for/while/listcomp/generator داخل @Rule")

FORBIDDEN_PATTERNS = [
    (r'\[.*\bfor\b.*\]',            'list comprehension'),
    (r'(min|max)\s*\(.*\bfor\b.*\)','generator في min/max'),
    (r'^\s+(for |while )',           'حلقة for/while'),
    (r'\*\*kwargs',                  '**kwargs'),
]

total_violations = 0
for fname in RULE_FILES:
    if not os.path.exists(fname): continue
    with open(fname, encoding='utf-8') as f:
        lines = f.readlines()

    in_body = False
    indent_level = None
    file_violations = []

    for lineno, line in enumerate(lines, 1):
        s = line.strip()
        if not s or s.startswith('#'): continue

        if s.startswith('@Rule'):
            in_body = True
            continue
        if in_body and s.startswith('def '):
            indent_level = len(line) - len(line.lstrip())
            in_body = 'body'
            continue
        if in_body == 'body':
            curr = len(line) - len(line.lstrip()) if line.strip() else 999
            if curr <= indent_level and line.strip():
                in_body = False
                continue
            for pattern, label in FORBIDDEN_PATTERNS:
                if re.search(pattern, line):
                    file_violations.append((lineno, label, s[:60]))
                    break

    if file_violations:
        total_violations += len(file_violations)
        for lineno, label, code in file_violations:
            record(False, f"[{fname}] سطر {lineno} | {label}: {code}")
    else:
        record(True, f"{fname}: نظيف")

if total_violations == 0:
    ok(f"إجمالي المخالفات: 0")

# ══════════════════════════════════════════════════════════════════
# TEST 4 — salience صحيح
# ══════════════════════════════════════════════════════════════════
section("TEST 4 — salience موجود وصحيح في كل قاعدة")

VALID_SALIENCE = {5, 10, 20, 30}   # القيم المقبولة

for fname in RULE_FILES:
    if not os.path.exists(fname): continue
    with open(fname, encoding='utf-8') as f:
        source = f.read()

    # استخراج كل @Rule مع salience
    rules_sal = re.findall(r'salience\s*=\s*(-?\d+)', source)
    rule_count = source.count('@Rule(')

    if not rules_sal:
        record(False, f"{fname}: لا يوجد salience في أي قاعدة")
        continue

    wrong = [int(v) for v in rules_sal if int(v) not in VALID_SALIENCE]
    missing = rule_count - len(rules_sal)

    if wrong:
        warn(f"{fname}: قيم salience غير متوقعة: {list(set(wrong))}")
        results['warnings'] += 1
    if missing > 0:
        record(False, f"{fname}: {missing} قاعدة بدون salience")
    else:
        record(True, f"{fname}: {rule_count} قاعدة ← salience: {sorted(set(int(v) for v in rules_sal))}")

# ══════════════════════════════════════════════════════════════════
# TEST 5 — قواعد العلاج تنتهي بـ halt()
# ══════════════════════════════════════════════════════════════════
section("TEST 5 — كل قاعدة علاج (Fact(disease=...)) تنتهي بـ halt()")

for fname in RULE_FILES:
    if not os.path.exists(fname): continue
    with open(fname, encoding='utf-8') as f:
        lines = f.readlines()

    in_treatment = False
    indent_level = None
    body_lines = []
    current_def = ""
    no_halt = []

    for lineno, line in enumerate(lines, 1):
        s = line.strip()

        if "@Rule(Fact(disease=" in s or "@Rule(\n" in s:
            pass  # نتعامل مع decorator متعدد الأسطر

        # كشف treatment rule: @Rule التي تحتوي Fact(disease=
        if s.startswith('@Rule') and 'Fact(disease=' in s:
            in_treatment = True
            body_lines = []
            continue

        if in_treatment and s.startswith('def '):
            current_def = s
            indent_level = len(line) - len(line.lstrip())
            body_lines = []
            in_treatment = 'body'
            continue

        if in_treatment == 'body':
            curr = len(line) - len(line.lstrip()) if line.strip() else 999
            if curr <= indent_level and line.strip() and not line.strip().startswith('#'):
                # نهاية الدالة
                has_halt = any('self.halt()' in bl for bl in body_lines)
                if not has_halt:
                    no_halt.append(current_def[:50])
                in_treatment = False
                body_lines = []
            else:
                body_lines.append(line)

    if no_halt:
        for d in no_halt:
            record(False, f"{fname}: بدون halt() → {d}")
    else:
        record(True, f"{fname}: كل قواعد العلاج تنتهي بـ halt()")

# ══════════════════════════════════════════════════════════════════
# TEST 6 — تشغيل حي لكل engine
# ══════════════════════════════════════════════════════════════════
section("TEST 6 — تشغيل حي (كل engine يُنتج تشخيصاً)")

# أعراض اختبارية مضمونة لكل نبات (cf=90 لضمان التفعيل)
TEST_CASES = {
    'apple_rules.py': {
        'class': 'AppleRules',
        'symptoms': [
            ('بقع زيتية على الأوراق', 90),
            ('تشوه الثمار', 90),
            ('تقشر لون الأوراق', 90),
        ],
        'expected_disease': 'جرب التفاح',
    },
    'cherry_rules.py': {
        'class': 'CherryRules',
        'symptoms': [
            ('بقع بيضاء على سطح الأوراق', 90),
            ('تشوه الأوراق', 90),
            ('تبقع وتلف الثمار', 90),
        ],
        'expected_disease': 'البياض الدقيقي',
    },
    'grape_rules.py': {
        'class': 'GrapeRules',
        'symptoms': [
            ('بقع صفراء على الأوراق', 90),
            ('نمو أبيض قطني تحت الأوراق', 90),
            ('ذبول الأوراق وسقوطها', 90),
        ],
        'expected_disease': None,  # أي تشخيص مقبول
    },
    'tomato_rules.py': {
        'class': 'TomatoRules',
        'symptoms': [
            ('هالات صفراء حول البقع', 90),
            ('ذبول الأوراق السفلية', 90),
            ('بقع بنية مائية على حواف الأوراق', 90),
        ],
        'expected_disease': None,
    },
    'Potato_rules.py': {
        'class': 'PotatoRules',
        'symptoms': [
            ('بقع مائية داكنة على الأوراق', 90),
            ('هالات خضراء إلى بنية على الساق', 90),
            ('تعفن بني على الدرنات', 90),
        ],
        'expected_disease': None,
    },
    'citrus_rules.py': {
        'class': 'CitrusRules',
        'symptoms': [
            ('اصفرار وتمدد للأوراق والشعيرات الخشبية', 90),
            ('ذبول وفناء أجزاء من الفروع', 90),
            ('إفرازات صمغية وردية أو رمادية في الجذوع', 90),
        ],
        'expected_disease': None,
    },
    'zucchini_rules.py': {
        'class': 'ZucchiniRules',
        'symptoms': [
            ('فسيفساء (mosaic) وتبقع أصفر على الأوراق', 90),
            ('تشوه وتقزز أوراق الكوسا', 90),
            ('ثمار مشوّهة أو ملوّنة وغير منتظمة', 90),
        ],
        'expected_disease': None,
    },
    'eggplant_rules.py': {
        'class': 'EggplantRules',
        'symptoms': [
            ('ذبول مفاجئ للنبات بدون اصفرار سابق', 90),
            ('تحول الساق الداخلي إلى اللون البني – يظهر عند قطع الجذع انسياب سائل مخاطي', 90),
            ('موت النبات بالكامل، خصوصًا في الطقس الدافئ والرطب', 90),
        ],
        'expected_disease': None,
    },
    'onion_rules.py': {
        'class': 'OnionRules',
        'symptoms': [
            ('بقع صفراء باهتة أو بنية طويلة على الأوراق الخارجية قد تتحول إلى نمو رمادي-بنفسجي تحت الرطوبة', 90),
            ('ذبول الأوراق المصابة وانحناؤها أو تساقطها', 90),
            ('البصليات تصبح طرية ومائية بسبب المرض', 90),
        ],
        'expected_disease': None,
    },
    'garlic_rules.py': {
        'class': 'GarlicRules',
        'symptoms': [
            ('اصفرار الأوراق من الأطراف نحو القاعدة', 90),
            ('ظهور نمو رمادي مزرق على السطح السفلي للأوراق', 90),
            ('تدهور مبكر للنباتات وسقوط الأوراق', 90),
        ],
        'expected_disease': None,
    },
}

# استيراد مكتبات experta
try:
    import collections.abc
    import collections
    collections.Mapping = collections.abc.Mapping
    collections.MutableMapping = collections.abc.MutableMapping
    collections.Callable = collections.abc.Callable
    from experta import KnowledgeEngine, Fact
    experta_ok = True
except ImportError:
    warn("experta غير مُثبَّتة — تخطي TEST 6")
    warn("لتثبيتها: pip install experta")
    experta_ok = False

if experta_ok:
    import importlib.util, io, contextlib

    def load_class(fname, classname):
        spec = importlib.util.spec_from_file_location(fname[:-3], fname)
        mod  = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return getattr(mod, classname)

    for fname, tc in TEST_CASES.items():
        if not os.path.exists(fname):
            warn(f"{fname}: الملف غير موجود — تخطي")
            continue
        try:
            EngineClass = load_class(fname, tc['class'])

            # الإمساك بـ stdout لمنع الطباعة
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                from core import Symptom
                engine = EngineClass()
                engine.reset()
                for sym_name, cf in tc['symptoms']:
                    engine.declare(Symptom(name=sym_name, cf=cf))
                engine.run()

            output = buf.getvalue()
            got_diagnosis = '✅' in output or '⚠️' in output or '❗' in output
            got_treatment  = '💡' in output

            if tc['expected_disease']:
                found = tc['expected_disease'] in output
                record(found and got_treatment,
                       f"{fname} → {'تشخيص صحيح ✓' if found else 'تشخيص خاطئ ✗'} | علاج: {'✓' if got_treatment else '✗'}")
            else:
                record(got_diagnosis and got_treatment,
                       f"{fname} → تشخيص: {'✓' if got_diagnosis else '✗'} | علاج: {'✓' if got_treatment else '✗'}")

        except Exception as e:
            record(False, f"{fname}: خطأ أثناء التشغيل — {e}")
            if '--verbose' in sys.argv:
                traceback.print_exc()

# ══════════════════════════════════════════════════════════════════
# النتيجة النهائية
# ══════════════════════════════════════════════════════════════════
section("النتيجة النهائية")

total = results['passed'] + results['failed']
pct   = round(results['passed'] / total * 100) if total else 0

print(f"\n  {GREEN}✅ ناجح   : {results['passed']}{RESET}")
print(f"  {RED}🔴 فاشل   : {results['failed']}{RESET}")
if results['warnings']:
    print(f"  {YELLOW}⚠️  تحذيرات: {results['warnings']}{RESET}")
print(f"\n  {'✅' if results['failed'] == 0 else '❌'} "
      f"{BOLD}النسبة: {pct}% ({results['passed']}/{total}){RESET}")

if results['failed'] > 0:
    print(f"\n  {RED}المشروع يحتاج إصلاحات. راجع الفشل بالأعلى.{RESET}")
    sys.exit(1)
else:
    print(f"\n  {GREEN}المشروع اجتاز جميع الاختبارات.{RESET}")
    sys.exit(0)
