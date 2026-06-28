from experta import Rule, Fact, MATCH, TEST, OR, AND
from core import (
    Symptom, PlantDiagnosisEngine,
    CF_FULL, CF_PARTIAL, CF_WEAK,
    HINT_MORE_SYMPTOMS,
)

class ZucchiniRules(PlantDiagnosisEngine):

    SYMPTOMS = [
        "فسيفساء (mosaic) وتبقع أصفر على الأوراق",
        "تشوه وتقزز أوراق الكوسا",
        "ثمار مشوّهة أو ملوّنة وغير منتظمة",
        "مسحوق أبيض رمادي يغطي السطح العلوي أو السفلي للأوراق",
        "اصفرار وتجعيد الأوراق مسبقًا",
        "تباطؤ نمو النبات وجفاف الأوراق المتقدمة",
        "ذبول فوري للنبات بدون اصفرار سابق",
        "أوراق قد تتحوّل إلى لون أخضر داكن ممل أو باهت",
        "سوائل مخاطية على جذع النبات عند القطع",
        "بقع دائرية مائية على الأوراق",
        "تقرحات وسوائل بنية/لزجة تنطلق من الساق",
        "تعفن الثمار أو صدأ على الثمار",
    ]

    # ── فيروس موزاييك الكوسا (ZYMV) ─────────────────────────────────────────

    @Rule(
        Symptom(name="فسيفساء (mosaic) وتبقع أصفر على الأوراق", cf=MATCH.cf1),
        Symptom(name="تشوه وتقزز أوراق الكوسا", cf=MATCH.cf2),
        Symptom(name="ثمار مشوّهة أو ملوّنة وغير منتظمة", cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60),
    )
    def zymv_full(self, cf1, cf2, cf3):
        self._diagnose_full("ZYMV", cf1, cf2, cf3)

    @Rule(
        OR(
            AND(Symptom(name="فسيفساء (mosaic) وتبقع أصفر على الأوراق", cf=MATCH.cf1),
                Symptom(name="تشوه وتقزز أوراق الكوسا", cf=MATCH.cf2)),
            AND(Symptom(name="فسيفساء (mosaic) وتبقع أصفر على الأوراق", cf=MATCH.cf1),
                Symptom(name="ثمار مشوّهة أو ملوّنة وغير منتظمة", cf=MATCH.cf2)),
            AND(Symptom(name="تشوه وتقزز أوراق الكوسا", cf=MATCH.cf1),
                Symptom(name="ثمار مشوّهة أو ملوّنة وغير منتظمة", cf=MATCH.cf2)),
        ),
        TEST(lambda cf1, cf2: min(cf1, cf2) >= 60),
    )
    def zymv_partial(self, cf1, cf2):
        self._diagnose_partial("ZYMV", cf1, cf2)

    @Rule(
        OR(
            Symptom(name="فسيفساء (mosaic) وتبقع أصفر على الأوراق", cf=MATCH.cf1),
            Symptom(name="تشوه وتقزز أوراق الكوسا", cf=MATCH.cf1),
            Symptom(name="ثمار مشوّهة أو ملوّنة وغير منتظمة", cf=MATCH.cf1),
        ),
        TEST(lambda cf1: cf1 >= 60),
    )
    def zymv_weak(self, cf1):
        self._diagnose_weak("ZYMV", cf1)

    @Rule(Fact(disease="ZYMV"))
    def zymv_treatment(self):
        self._treat(
            disease_name="فيروس موزاييك الكوسا الأصفر (ZYMV)",
            cause="فيروس موزاييك الكوسا (Zucchini Yellow Mosaic Virus) - ZYMV.",
            steps=[
                "إزالة وإتلاف النباتات المصابة فورًا",
                "مكافحة الحشرات الناقلة (خاصة المن) بمبيدات حشرية",
                "استخدام أصناف مقاومة أو مطعّمة",
                "تجنب زراعة الكوسا بالقرب من المحاصيل المصابة",
                "استخدام بذور خالية من الفيروس",
            ],
        )

    # ── البياض البودري ──────────────────────────────────────────────────────

    @Rule(
        Symptom(name="مسحوق أبيض رمادي يغطي السطح العلوي أو السفلي للأوراق", cf=MATCH.cf1),
        Symptom(name="اصفرار وتجعيد الأوراق مسبقًا", cf=MATCH.cf2),
        Symptom(name="تباطؤ نمو النبات وجفاف الأوراق المتقدمة", cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60),
    )
    def powdery_mildew_full(self, cf1, cf2, cf3):
        self._diagnose_full("البياض البودري", cf1, cf2, cf3)

    @Rule(
        OR(
            AND(Symptom(name="مسحوق أبيض رمادي يغطي السطح العلوي أو السفلي للأوراق", cf=MATCH.cf1),
                Symptom(name="اصفرار وتجعيد الأوراق مسبقًا", cf=MATCH.cf2)),
            AND(Symptom(name="مسحوق أبيض رمادي يغطي السطح العلوي أو السفلي للأوراق", cf=MATCH.cf1),
                Symptom(name="تباطؤ نمو النبات وجفاف الأوراق المتقدمة", cf=MATCH.cf2)),
            AND(Symptom(name="اصفرار وتجعيد الأوراق مسبقًا", cf=MATCH.cf1),
                Symptom(name="تباطؤ نمو النبات وجفاف الأوراق المتقدمة", cf=MATCH.cf2)),
        ),
        TEST(lambda cf1, cf2: min(cf1, cf2) >= 60),
    )
    def powdery_mildew_partial(self, cf1, cf2):
        self._diagnose_partial("البياض البودري", cf1, cf2)

    @Rule(
        OR(
            Symptom(name="مسحوق أبيض رمادي يغطي السطح العلوي أو السفلي للأوراق", cf=MATCH.cf1),
            Symptom(name="اصفرار وتجعيد الأوراق مسبقًا", cf=MATCH.cf1),
            Symptom(name="تباطؤ نمو النبات وجفاف الأوراق المتقدمة", cf=MATCH.cf1),
        ),
        TEST(lambda cf1: cf1 >= 60),
    )
    def powdery_mildew_weak(self, cf1):
        self._diagnose_weak("البياض البودري", cf1)

    @Rule(Fact(disease="البياض البودري"))
    def powdery_mildew_treatment(self):
        self._treat(
            disease_name="مرض البياض البودري - الكوسا",
            cause="مرض البياض البودري في الكوسا يُسببه الفطر Podosphaera xanthii.",
            steps=[
                "رش النبات بمبيد فطري مخصص للبياض البودري (مثل الكبريت الميكروني أو محلول بوردو)",
                "تحسين التهوية وتقليل الرطوبة داخل البيوت المحمية",
                "إزالة الأوراق المصابة فورًا ومنع تراكم بقايا النباتات",
                "تجنب الري بالرش ويفضل الري الجذري",
                "زراعة أصناف مقاومة للمرض",
            ],
        )

    # ── الذبول البكتيري ─────────────────────────────────────────────────────

    @Rule(
        Symptom(name="ذبول فوري للنبات بدون اصفرار سابق", cf=MATCH.cf1),
        Symptom(name="أوراق قد تتحوّل إلى لون أخضر داكن ممل أو باهت", cf=MATCH.cf2),
        Symptom(name="سوائل مخاطية على جذع النبات عند القطع", cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60),
    )
    def bacterial_wilt_full(self, cf1, cf2, cf3):
        self._diagnose_full("الذبول البكتيري", cf1, cf2, cf3)

    @Rule(
        OR(
            AND(Symptom(name="ذبول فوري للنبات بدون اصفرار سابق", cf=MATCH.cf1),
                Symptom(name="أوراق قد تتحوّل إلى لون أخضر داكن ممل أو باهت", cf=MATCH.cf2)),
            AND(Symptom(name="ذبول فوري للنبات بدون اصفرار سابق", cf=MATCH.cf1),
                Symptom(name="سوائل مخاطية على جذع النبات عند القطع", cf=MATCH.cf2)),
            AND(Symptom(name="أوراق قد تتحوّل إلى لون أخضر داكن ممل أو باهت", cf=MATCH.cf1),
                Symptom(name="سوائل مخاطية على جذع النبات عند القطع", cf=MATCH.cf2)),
        ),
        TEST(lambda cf1, cf2: min(cf1, cf2) >= 60),
    )
    def bacterial_wilt_partial(self, cf1, cf2):
        self._diagnose_partial("الذبول البكتيري", cf1, cf2)

    @Rule(
        OR(
            Symptom(name="ذبول فوري للنبات بدون اصفرار سابق", cf=MATCH.cf1),
            Symptom(name="أوراق قد تتحوّل إلى لون أخضر داكن ممل أو باهت", cf=MATCH.cf1),
            Symptom(name="سوائل مخاطية على جذع النبات عند القطع", cf=MATCH.cf1),
        ),
        TEST(lambda cf1: cf1 >= 60),
    )
    def bacterial_wilt_weak(self, cf1):
        self._diagnose_weak("الذبول البكتيري", cf1)

    @Rule(Fact(disease="الذبول البكتيري"))
    def bacterial_wilt_treatment(self):
        self._treat(
            disease_name="مرض الذبول البكتيري - الكوسا",
            cause="مرض الذبول البكتيري في الكوسا يُسببه البكتيريا Erwinia tracheiphila.",
            steps=[
                "إزالة النباتات المصابة فورًا والتخلص منها (لا تُعاد كسماد)",
                "تعقيم أدوات الزراعة بعد كل استخدام",
                "مكافحة الخنافس الناقلة للبكتيريا باستخدام مبيدات حشرية",
                "تجنب زراعة الكوسا في تربة سبق إصابة نباتات فيها بالمرض",
                "لا يوجد علاج كيميائي فعّال، لذا يُركز على الوقاية فقط",
            ],
        )

    # ── عفن الجذع اللزج ─────────────────────────────────────────────────────

    @Rule(
        Symptom(name="بقع دائرية مائية على الأوراق", cf=MATCH.cf1),
        Symptom(name="تقرحات وسوائل بنية/لزجة تنطلق من الساق", cf=MATCH.cf2),
        Symptom(name="تعفن الثمار أو صدأ على الثمار", cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60),
    )
    def gummy_stem_blight_full(self, cf1, cf2, cf3):
        self._diagnose_full("عفن الجذع اللزج", cf1, cf2, cf3)

    @Rule(
        OR(
            AND(Symptom(name="بقع دائرية مائية على الأوراق", cf=MATCH.cf1),
                Symptom(name="تقرحات وسوائل بنية/لزجة تنطلق من الساق", cf=MATCH.cf2)),
            AND(Symptom(name="بقع دائرية مائية على الأوراق", cf=MATCH.cf1),
                Symptom(name="تعفن الثمار أو صدأ على الثمار", cf=MATCH.cf2)),
            AND(Symptom(name="تقرحات وسوائل بنية/لزجة تنطلق من الساق", cf=MATCH.cf1),
                Symptom(name="تعفن الثمار أو صدأ على الثمار", cf=MATCH.cf2)),
        ),
        TEST(lambda cf1, cf2: min(cf1, cf2) >= 60),
    )
    def gummy_stem_blight_partial(self, cf1, cf2):
        self._diagnose_partial("عفن الجذع اللزج", cf1, cf2)

    @Rule(
        OR(
            Symptom(name="بقع دائرية مائية على الأوراق", cf=MATCH.cf1),
            Symptom(name="تقرحات وسوائل بنية/لزجة تنطلق من الساق", cf=MATCH.cf1),
            Symptom(name="تعفن الثمار أو صدأ على الثمار", cf=MATCH.cf1),
        ),
        TEST(lambda cf1: cf1 >= 60),
    )
    def gummy_stem_blight_weak(self, cf1):
        self._diagnose_weak("عفن الجذع اللزج", cf1)

    @Rule(Fact(disease="عفن الجذع اللزج"))
    def gummy_stem_blight_treatment(self):
        self._treat(
            disease_name="مرض عفن الجذع اللزج - الكوسا",
            cause="مرض عفن الجذع اللزج في الكوسا يُسببه البكتيريا Pectobacterium carotovorum.",
            steps=[
                "رش النبات بمبيد فطري وقائي مثل مبيدات النحاس أو البنزيميدازول",
                "إزالة وإتلاف الأجزاء المصابة فورًا",
                "تجنب الري بالرش لتفادي زيادة الرطوبة والانتشار",
                "تعقيم أدوات العمل بين النباتات",
                "تجنب الزراعة الكثيفة وتحسين التهوية بين النباتات",
            ],
        )
