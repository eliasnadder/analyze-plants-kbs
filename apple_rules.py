from experta import Rule, Fact, MATCH, TEST, OR, AND
from core import (
    Symptom, PlantDiagnosisEngine,
    CF_FULL, CF_PARTIAL, CF_WEAK,
    HINT_MORE_SYMPTOMS,
)

class AppleRules(PlantDiagnosisEngine):

    SYMPTOMS = [
        "بقع زيتية على الأوراق",
        "تشوه الثمار",
        "تقشر لون الأوراق",
        "بقع بنفسجية على الأوراق",
        "تقرحات على الأغصان",
        "تعفن بني على الثمار",
        "بقع صفراء على الأوراق",
        "أورام برتقالية",
        "تورم الأوراق من الأسفل",
    ]

    # ── جرب التفاح ─────────────────────────────────────────────────────────

    @Rule(
        Symptom(name="بقع زيتية على الأوراق", cf=MATCH.cf1),
        Symptom(name="تشوه الثمار", cf=MATCH.cf2),
        Symptom(name="تقشر لون الأوراق", cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60),
    )
    def apple_scab_full(self, cf1, cf2, cf3):
        self._diagnose_full("جرب التفاح", cf1, cf2, cf3)

    @Rule(
        OR(
            AND(Symptom(name="بقع زيتية على الأوراق", cf=MATCH.cf1),
                Symptom(name="تشوه الثمار", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="بقع زيتية على الأوراق", cf=MATCH.cf1),
                Symptom(name="تقشر لون الأوراق", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="تشوه الثمار", cf=MATCH.cf1),
                Symptom(name="تقشر لون الأوراق", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
        )
    )
    def apple_scab_partial(self, cf1, cf2):
        self._diagnose_partial("جرب التفاح", cf1, cf2)

    @Rule(
        OR(
            Symptom(name="بقع زيتية على الأوراق", cf=MATCH.cf1),
            Symptom(name="تشوه الثمار", cf=MATCH.cf1),
            Symptom(name="تقشر لون الأوراق", cf=MATCH.cf1),
        ),
        TEST(lambda cf1: cf1 >= 60),
    )
    def apple_scab_weak(self, cf1):
        self._diagnose_weak("جرب التفاح", cf1)

    @Rule(Fact(disease="جرب التفاح"))
    def apple_scab_treatment(self):
        self._treat(
            disease_name="جرب التفاح",
            cause="مرض جرب التفاح يُسببه الفطر Venturia inaequalis.",
            steps=[
                "رش Captan أو Kumulus كل 7–14 يوم لمدة 2–3 شهور",
                "رش علاجي بعد الأعراض خلال 48 ساعة",
                "إزالة الأوراق/الثمار المصابة باستمرار",
                "تقليم الأغصان سنويًا",
            ],
        )

    # ── العفن الأسود ────────────────────────────────────────────────────────

    @Rule(
        Symptom(name="بقع بنفسجية على الأوراق", cf=MATCH.cf1),
        Symptom(name="تقرحات على الأغصان", cf=MATCH.cf2),
        Symptom(name="تعفن بني على الثمار", cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60),
    )
    def black_rot_full(self, cf1, cf2, cf3):
        self._diagnose_full("العفن الأسود", cf1, cf2, cf3)

    @Rule(
        OR(
            AND(Symptom(name="بقع بنفسجية على الأوراق", cf=MATCH.cf1),
                Symptom(name="تقرحات على الأغصان", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="بقع بنفسجية على الأوراق", cf=MATCH.cf1),
                Symptom(name="تعفن بني على الثمار", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="تقرحات على الأغصان", cf=MATCH.cf1),
                Symptom(name="تعفن بني على الثمار", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
        )
    )
    def black_rot_partial(self, cf1, cf2):
        self._diagnose_partial("العفن الأسود", cf1, cf2)

    @Rule(
        OR(
            Symptom(name="بقع بنفسجية على الأوراق", cf=MATCH.cf1),
            Symptom(name="تقرحات على الأغصان", cf=MATCH.cf1),
            Symptom(name="تعفن بني على الثمار", cf=MATCH.cf1),
        ),
        TEST(lambda cf1: cf1 >= 60),
    )
    def black_rot_weak(self, cf1):
        self._diagnose_weak("العفن الأسود", cf1)

    @Rule(Fact(disease="العفن الأسود"))
    def black_rot_treatment(self):
        self._treat(
            disease_name="العفن الأسود",
            cause="مرض العفن الأسود في التفاح يُسببه الفطر Botryosphaeria obtusa.",
            steps=[
                "تقليم وإزالة الثمار/الأغصان المصابة طوال السنة",
                "رش Captan أو Polyram كل 10–14 يوم لمدة 4–6 أسابيع",
                "بديل بيولوجي: Trianum Shield حسب الحاجة",
                "تقليم Cankers 15 سم تحت الأنسجة المريضة",
            ],
        )

    # ── صدأ التفاح الصنوبري ─────────────────────────────────────────────────

    @Rule(
        Symptom(name="بقع صفراء على الأوراق", cf=MATCH.cf1),
        Symptom(name="أورام برتقالية", cf=MATCH.cf2),
        Symptom(name="تورم الأوراق من الأسفل", cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60),
    )
    def cedar_rust_full(self, cf1, cf2, cf3):
        self._diagnose_full("صدأ التفاح الصنوبري", cf1, cf2, cf3)

    @Rule(
        OR(
            AND(Symptom(name="بقع صفراء على الأوراق", cf=MATCH.cf1),
                Symptom(name="أورام برتقالية", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="بقع صفراء على الأوراق", cf=MATCH.cf1),
                Symptom(name="تورم الأوراق من الأسفل", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="أورام برتقالية", cf=MATCH.cf1),
                Symptom(name="تورم الأوراق من الأسفل", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
        )
    )
    def cedar_rust_partial(self, cf1, cf2):
        self._diagnose_partial("صدأ التفاح الصنوبري", cf1, cf2)

    @Rule(
        OR(
            Symptom(name="بقع صفراء على الأوراق", cf=MATCH.cf1),
            Symptom(name="أورام برتقالية", cf=MATCH.cf1),
            Symptom(name="تورم الأوراق من الأسفل", cf=MATCH.cf1),
        ),
        TEST(lambda cf1: cf1 >= 60),
    )
    def cedar_rust_weak(self, cf1):
        self._diagnose_weak("صدأ التفاح الصنوبري", cf1)

    @Rule(Fact(disease="صدأ التفاح الصنوبري"))
    def cedar_rust_treatment(self):
        self._treat(
            disease_name="صدأ التفاح الصنوبري",
            cause="مرض صدأ التفاح يُسببه الفطر Gymnosporangium juniperi-virginianae.",
            steps=[
                "رش مبيدات فطرية تحتوي على Myclobutanil أو Mancozeb كل 7–10 أيام أثناء الربيع",
                "إزالة أوراق العرعر القريبة إن أمكن (ناقل المرض)",
                "تقليم الأغصان المصابة وتحسين التهوية",
                "زراعة أصناف مقاومة للمرض في المستقبل",
            ],
        )
