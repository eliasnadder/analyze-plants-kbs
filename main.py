import sys
import collections
import collections.abc

try:
    collections.Mapping  # noqa: B018
except AttributeError:
    collections.Mapping = collections.abc.Mapping

from apple_rules    import AppleRules
from cherry_rules   import CherryRules
from grape_rules    import GrapeRules
from tomato_rules   import TomatoRules
from Potato_rules   import PotatoRules
from citrus_rules   import CitrusRules
from zucchini_rules import ZucchiniRules
from eggplant_rules import EggplantRules
from onion_rules    import OnionRules
from garlic_rules   import GarlicRules
from core           import Symptom
from symptom_mapper import map_text_to_symptoms

# ── تسجيل المحركات ────────────────────────────────────────────────────────
ENGINES: dict[int, tuple[str, type]] = {
    1:  ("تفاح",    AppleRules),
    2:  ("كرز",     CherryRules),
    3:  ("عنب",     GrapeRules),
    4:  ("طماطم",   TomatoRules),
    5:  ("بطاطا",   PotatoRules),
    6:  ("حمضيات",  CitrusRules),
    7:  ("كوسا",    ZucchiniRules),
    8:  ("باذنجان", EggplantRules),
    9:  ("البصل",   OnionRules),
    10: ("الثوم",   GarlicRules),
}
EXIT_CHOICE = len(ENGINES) + 1


# ── اختيار المحصول ─────────────────────────────────────────────────────────
def _select_crop() -> tuple[str, type] | None:
    print("\n🌿 اختر نوع النبات:")
    for key, (name, _) in ENGINES.items():
        print(f"  {key}. {name}")
    print(f"  {EXIT_CHOICE}. خروج")

    raw = input("> ").strip()
    if not raw.isdigit():
        print("⚠️  أدخل رقماً من القائمة.")
        return None

    idx = int(raw)
    if idx == EXIT_CHOICE:
        return ()
    if idx not in ENGINES:
        print("⚠️  رقم غير موجود.")
        return None
    return ENGINES[idx]


# ── الإدخال اليدوي (قائمة) ────────────────────────────────────────────────
def _collect_manual_symptoms(engine_class: type, crop_name: str) -> list:
    symptoms = engine_class.SYMPTOMS
    print(f"\n📋 أعراض {crop_name} المتاحة:")
    for i, sym in enumerate(symptoms, start=1):
        print(f"  {i:2}. {sym}")

    raw = input("\nأدخل أرقام الأعراض (مفصولة بمسافات): ").strip()
    if not any(t.isdigit() for t in raw.split()):
        print("⚠️  يرجى إدخال أرقام (مثال: 1 3 7).")
        return []

    selected = []
    for token in raw.split():
        if not token.isdigit():
            continue
        idx = int(token) - 1
        if not (0 <= idx < len(symptoms)):
            print(f"  ⚠️  الرقم {token} خارج النطاق، تم تجاهله.")
            continue
        try:
            cf = int(input(f"  درجة التأكد (0–100) لـ '{symptoms[idx]}': ").strip())
            cf = max(0, min(100, cf))
            selected.append(Symptom(name=symptoms[idx], cf=cf))
        except ValueError:
            print("  ⚠️  إدخال غير صالح، تم تجاهل هذا العرض.")
    return selected


# ── الإدخال النصي (NLP) ───────────────────────────────────────────────────
def _collect_nlp_symptoms(engine_class: type, crop_name: str) -> list:
    print(f"\n✍️  صِف لي الأعراض التي تلاحظها على {crop_name}:")
    print("    (مثال: الأوراق صفراء وعم تتساقط، في تورم من الأسفل)")
    user_text = input("> ").strip()

    if not user_text:
        print("⚠️  لم تكتب شيئاً.")
        return []

    # ✅ التصحيح الرئيسي: نمرر قائمة أعراض المحصول الحالي كفلتر
    detected = map_text_to_symptoms(user_text, crop_symptoms=engine_class.SYMPTOMS)

    if not detected:
        print("⚠️  لم أستطع استخراج أعراض واضحة من نصك.")
        print("    جرّب الإدخال اليدوي، أو أعِد صياغة الجملة بشكل أوضح.")
        return []

    print(f"\n✅ تم اكتشاف {len(detected)} عرض:")
    selected = []
    for name in detected:
        print(f"  - {name}")
        try:
            cf_raw = input(f"    درجة تأكدك (0–100)؟ [اضغط Enter للافتراض 80]: ").strip()
            cf = int(cf_raw) if cf_raw else 80
            cf = max(0, min(100, cf))
        except ValueError:
            cf = 80
            print("    ⚠️  إدخال غير صالح، تم افتراض 80.")
        selected.append(Symptom(name=name, cf=cf))

    return selected


# ── الحلقة الرئيسية ───────────────────────────────────────────────────────
def main() -> None:
    print("=" * 50)
    print("  🌱 نظام تشخيص الأمراض النباتية")
    print("=" * 50)

    while True:
        result = _select_crop()
        if result is None:
            continue
        if result == ():
            print("👋 مع السلامة.")
            break

        crop_name, engine_class = result

        print(f"\nطريقة إدخال الأعراض لـ [{crop_name}]:")
        print("  1. إدخال نصي حر (NLP) — اكتب ما تراه بكلامك")
        print("  2. اختيار يدوي من القائمة")
        mode = input("> ").strip()

        engine = engine_class()
        engine.reset()

        if mode == "1":
            facts = _collect_nlp_symptoms(engine_class, crop_name)
        else:
            facts = _collect_manual_symptoms(engine_class, crop_name)

        if not facts:
            print("  لم تُدخل أي أعراض، تم تجاهل التشخيص.")
        else:
            print("\n" + "─" * 40)
            for fact in facts:
                engine.declare(fact)
            engine.run()
            print("─" * 40)

        again = input("\nهل تريد تشخيص مرض آخر؟ (نعم/لا): ").strip().lower()
        if again not in ("نعم", "yes", "y"):
            print("👋 مع السلامة.")
            break


if __name__ == "__main__":
    main()
