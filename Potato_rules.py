from experta import Rule, Fact, MATCH, TEST, OR, AND
from core import (
    Symptom, PlantDiagnosisEngine,
    CF_FULL, CF_PARTIAL, CF_WEAK, CF_MED_HIGH,
    HINT_MORE_SYMPTOMS,
)

class PotatoRules(PlantDiagnosisEngine):

    SYMPTOMS = [
        "بقع مائية داكنة على الأوراق",
        "هالات خضراء إلى بنية على الساق",
        "تعفن بني على الدرنات",
        "ورقة ناصعة اللون أو موزاييك مصفر",
        "تشوه أو تجعد الأوراق",
        "صغر حجم الدرنات",          # كان مفقوداً من قائمة الأعراض سابقاً
        "بقع سوداء صلبة على الدرنات",
        "آفات في الساق عند القاعدة",
        "ظهور بثور صغيرة بيضاء أو بنية على الدرنات",
        "تشوه سطح الدرنات",
        "تندّب أو تقشير جلدي في منطقة القروح",
    ]

    # ── اللفحة المتأخرة ─────────────────────────────────────────────────────

    @Rule(
        Symptom(name="بقع مائية داكنة على الأوراق", cf=MATCH.cf1),
        Symptom(name="هالات خضراء إلى بنية على الساق", cf=MATCH.cf2),
        Symptom(name="تعفن بني على الدرنات", cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60),
    )
    def late_blight_full(self, cf1, cf2, cf3):
        self._diagnose_full("اللفحة المتأخرة", cf1, cf2, cf3)

    @Rule(
        OR(
            AND(Symptom(name="بقع مائية داكنة على الأوراق", cf=MATCH.cf1),
                Symptom(name="هالات خضراء إلى بنية على الساق", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="بقع مائية داكنة على الأوراق", cf=MATCH.cf1),
                Symptom(name="تعفن بني على الدرنات", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="هالات خضراء إلى بنية على الساق", cf=MATCH.cf1),
                Symptom(name="تعفن بني على الدرنات", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
        )
    )
    def late_blight_partial(self, cf1, cf2):
        self._diagnose_partial("اللفحة المتأخرة", cf1, cf2)

    @Rule(
        OR(
            Symptom(name="بقع مائية داكنة على الأوراق", cf=MATCH.cf1),
            Symptom(name="هالات خضراء إلى بنية على الساق", cf=MATCH.cf1),
            Symptom(name="تعفن بني على الدرنات", cf=MATCH.cf1),
        ),
        TEST(lambda cf1: cf1 >= 60),
    )
    def late_blight_weak(self, cf1):
        self._diagnose_weak("اللفحة المتأخرة", cf1)

    @Rule(Fact(disease="اللفحة المتأخرة"))
    def late_blight_treatment(self):
        self._treat(
            disease_name="اللفحة المتأخرة - البطاطا",
            cause="مرض اللفحة المتأخرة في البطاطا يُسببه الفطر Phytophthora infestans.",
            steps=[
                "استخدام مبيد فطري مثل Mancozeb أو Cymoxanil",
                "رش عند بداية ظهور الأعراض مع تكرار كل 7–10 أيام",
            ],
        )

    # ── فيروس PVY ────────────────────────────────────────────────────────────

    @Rule(
        Symptom(name="ورقة ناصعة اللون أو موزاييك مصفر", cf=MATCH.cf1),
        Symptom(name="تشوه أو تجعد الأوراق", cf=MATCH.cf2),
        Symptom(name="صغر حجم الدرنات", cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60),
    )
    def pvy_full(self, cf1, cf2, cf3):
        self._diagnose_full("PVY", cf1, cf2, cf3)

    @Rule(
        OR(
            AND(Symptom(name="ورقة ناصعة اللون أو موزاييك مصفر", cf=MATCH.cf1),
                Symptom(name="تشوه أو تجعد الأوراق", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="تشوه أو تجعد الأوراق", cf=MATCH.cf1),
                Symptom(name="صغر حجم الدرنات", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="ورقة ناصعة اللون أو موزاييك مصفر", cf=MATCH.cf1),
                Symptom(name="صغر حجم الدرنات", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
        )
    )
    def pvy_partial(self, cf1, cf2):
        self._diagnose_partial("PVY", cf1, cf2)

    @Rule(
        OR(
            Symptom(name="ورقة ناصعة اللون أو موزاييك مصفر", cf=MATCH.cf1),
            Symptom(name="تشوه أو تجعد الأوراق", cf=MATCH.cf1),
            Symptom(name="صغر حجم الدرنات", cf=MATCH.cf1),
        ),
        TEST(lambda cf1: cf1 >= 60),
    )
    def pvy_weak(self, cf1):
        self._diagnose_weak("PVY", cf1)

    @Rule(Fact(disease="PVY"))
    def pvy_treatment(self):
        self._treat(
            disease_name="فيروس PVY - البطاطا",
            cause="فيروس اللفحة العصوية للبطاطا (Potato Virus Y) - PVY.",
            steps=[
                "لا يوجد علاج مباشر، يُفضل استخدام درنات خالية من الفيروس",
                "السيطرة على حشرات المن (ناقل رئيسي)",
                "التخلص من النباتات المصابة",
            ],
        )

    # ── القشرة السوداء (Black Scurf) ────────────────────────────────────────

    @Rule(
        Symptom(name="بقع سوداء صلبة على الدرنات", cf=MATCH.cf1),
        Symptom(name="آفات في الساق عند القاعدة", cf=MATCH.cf2),
        TEST(lambda cf1, cf2: min(cf1, cf2) >= 60),
    )
    def black_scurf_full(self, cf1, cf2):
        self._diagnose_full("Black Scurf", cf1, cf2)

    @Rule(
        OR(
            Symptom(name="بقع سوداء صلبة على الدرنات", cf=MATCH.cf1),
            Symptom(name="آفات في الساق عند القاعدة", cf=MATCH.cf1),
        ),
        TEST(lambda cf1: cf1 >= 60),
    )
    def black_scurf_weak(self, cf1):
        self._diagnose_weak("Black Scurf", cf1)

    @Rule(Fact(disease="Black Scurf"))
    def black_scurf_treatment(self):
        self._treat(
            disease_name="عفن القشرة السوداء - البطاطا",
            cause="مرض القشرة السوداء (Black Scurf) في البطاطا يُسببه الفطر Rhizoctonia solani.",
            steps=[
                "الزراعة في تربة جيدة التصريف وتغيير الدورة الزراعية",
                "معالجة الدرنات قبل الزراعة بمبيد مناسب مثل flutolanil",
            ],
        )

    # ── عفن القروح الجذري ───────────────────────────────────────────────────

    @Rule(
        Symptom(name="ظهور بثور صغيرة بيضاء أو بنية على الدرنات", cf=MATCH.cf1),
        Symptom(name="تشوه سطح الدرنات", cf=MATCH.cf2),
        Symptom(name="تندّب أو تقشير جلدي في منطقة القروح", cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60),
    )
    def powdery_scab_full(self, cf1, cf2, cf3):
        self._diagnose_full("عفن القروح الجذري", cf1, cf2, cf3)

    @Rule(
        OR(
            AND(Symptom(name="ظهور بثور صغيرة بيضاء أو بنية على الدرنات", cf=MATCH.cf1),
                Symptom(name="تشوه سطح الدرنات", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="تشوه سطح الدرنات", cf=MATCH.cf1),
                Symptom(name="تندّب أو تقشير جلدي في منطقة القروح", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="ظهور بثور صغيرة بيضاء أو بنية على الدرنات", cf=MATCH.cf1),
                Symptom(name="تندّب أو تقشير جلدي في منطقة القروح", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
        )
    )
    def powdery_scab_partial(self, cf1, cf2):
        self._diagnose_partial("عفن القروح الجذري", cf1, cf2)

    @Rule(
        OR(
            Symptom(name="ظهور بثور صغيرة بيضاء أو بنية على الدرنات", cf=MATCH.cf1),
            Symptom(name="تشوه سطح الدرنات", cf=MATCH.cf1),
            Symptom(name="تندّب أو تقشير جلدي في منطقة القروح", cf=MATCH.cf1),
        ),
        TEST(lambda cf1: cf1 >= 60),
    )
    def powdery_scab_weak(self, cf1):
        self._diagnose_weak("عفن القروح الجذري", cf1)

    @Rule(Fact(disease="عفن القروح الجذري"))
    def powdery_scab_treatment(self):
        self._treat(
            disease_name="عفن القروح الجذري - البطاطا",
            cause="مرض عفن القروح الجذري في البطاطا يُسببه الفطر Spongospora subterranea.",
            steps=[
                "لا يوجد علاج فعّال، لكن يمكن اتخاذ الإجراءات الوقائية التالية:",
                "زراعة درنات خالية من الإصابة",
                "تجنّب التربة الثقيلة والرطبة",
                "تطبيق دورات زراعية وعدم زراعة البطاطا في نفس المكان لعدة مواسم",
            ],
        )
