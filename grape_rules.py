from experta import Rule, Fact, MATCH, TEST, OR, AND
from core import (
    Symptom, PlantDiagnosisEngine,
    CF_FULL, CF_PARTIAL, CF_WEAK, CF_VERY_HIGH,
    HINT_MORE_SYMPTOMS, HINT_SIMILAR_DISEASE,
)

class GrapeRules(PlantDiagnosisEngine):

    SYMPTOMS = [
        "بقع صفراء على الأوراق",
        "نمو أبيض قطني تحت الأوراق",
        "ذبول الأوراق وسقوطها",
        "بقع رمادية على العناقيد",
        "تعفن طري على الثمار",
        "وجود زغب رمادي اللون",
        "مسحوق أبيض على سطح الأوراق والثمار",
        "تشوه الثمار وتوقف نموها",
        "تشقق الثمار وتلفها",
        "توقف نمو النبات أو موته المفاجئ",
    ]

    # ── البياض الزغبي ───────────────────────────────────────────────────────

    @Rule(
        Symptom(name="بقع صفراء على الأوراق", cf=MATCH.cf1),
        Symptom(name="نمو أبيض قطني تحت الأوراق", cf=MATCH.cf2),
        Symptom(name="ذبول الأوراق وسقوطها", cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60),
    )
    def downy_mildew_full(self, cf1, cf2, cf3):
        self._diagnose_full("البياض الزغبي", cf1, cf2, cf3)

    @Rule(
        OR(
            AND(Symptom(name="بقع صفراء على الأوراق", cf=MATCH.cf1),
                Symptom(name="نمو أبيض قطني تحت الأوراق", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="بقع صفراء على الأوراق", cf=MATCH.cf1),
                Symptom(name="ذبول الأوراق وسقوطها", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="نمو أبيض قطني تحت الأوراق", cf=MATCH.cf1),
                Symptom(name="ذبول الأوراق وسقوطها", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
        ),
        salience=11,
    )
    def downy_mildew_partial(self, cf1, cf2):
        self._diagnose_partial("البياض الزغبي", cf1, cf2, hint=HINT_SIMILAR_DISEASE)

    @Rule(
        OR(
            Symptom(name="بقع صفراء على الأوراق", cf=MATCH.cf1),
            Symptom(name="نمو أبيض قطني تحت الأوراق", cf=MATCH.cf1),
            Symptom(name="ذبول الأوراق وسقوطها", cf=MATCH.cf1),
        ),
        TEST(lambda cf1: cf1 >= 60),
        salience=10,
    )
    def downy_mildew_weak(self, cf1):
        self._diagnose_weak("البياض الزغبي", cf1, hint=HINT_SIMILAR_DISEASE)

    @Rule(Fact(disease="البياض الزغبي"))
    def downy_mildew_treatment(self):
        self._treat(
            disease_name="البياض الزغبي - العنب",
            cause="مرض البياض الزغبي في العنب يُسببه الفطر Plasmopara viticola.",
            steps=[
                "رش مبيد فطري يحتوي على Metalaxyl أو Mancozeb",
                "تكرار الرش كل 7–10 أيام حسب الظروف الجوية",
                "تحسين التهوية والتخلص من الأجزاء المصابة",
            ],
        )

    # ── العفن الرمادي ────────────────────────────────────────────────────────

    @Rule(
        Symptom(name="بقع رمادية على العناقيد", cf=MATCH.cf1),
        Symptom(name="تعفن طري على الثمار", cf=MATCH.cf2),
        Symptom(name="وجود زغب رمادي اللون", cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60),
    )
    def gray_mold_full(self, cf1, cf2, cf3):
        self._diagnose_full("العفن الرمادي", cf1, cf2, cf3)

    @Rule(
        OR(
            AND(Symptom(name="بقع رمادية على العناقيد", cf=MATCH.cf1),
                Symptom(name="تعفن طري على الثمار", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="بقع رمادية على العناقيد", cf=MATCH.cf1),
                Symptom(name="وجود زغب رمادي اللون", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="تعفن طري على الثمار", cf=MATCH.cf1),
                Symptom(name="وجود زغب رمادي اللون", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
        )
    )
    def gray_mold_partial(self, cf1, cf2):
        self._diagnose_partial("العفن الرمادي", cf1, cf2)

    @Rule(
        OR(
            Symptom(name="بقع رمادية على العناقيد", cf=MATCH.cf1),
            Symptom(name="تعفن طري على الثمار", cf=MATCH.cf1),
            Symptom(name="وجود زغب رمادي اللون", cf=MATCH.cf1),
        ),
        TEST(lambda cf1: cf1 >= 60),
    )
    def gray_mold_weak(self, cf1):
        self._diagnose_weak("العفن الرمادي", cf1)

    @Rule(Fact(disease="العفن الرمادي"))
    def gray_mold_treatment(self):
        self._treat(
            disease_name="العفن الرمادي - العنب",
            cause="مرض العفن الرمادي في العنب يُسببه الفطر Botrytis cinerea.",
            steps=[
                "إزالة العناقيد والثمار المصابة فورًا",
                "تحسين التهوية والتعرض لأشعة الشمس بالتقليم",
                "استخدام مبيدات فطرية مثل iprodione أو fenhexamid قبل الإزهار وبعده",
                "تجنب الرطوبة الزائدة وري النباتات في الصباح الباكر",
            ],
        )

    # ── البياض الدقيقي ───────────────────────────────────────────────────────

    @Rule(
        Symptom(name="مسحوق أبيض على سطح الأوراق والثمار", cf=MATCH.cf1),
        Symptom(name="تشوه الثمار وتوقف نموها", cf=MATCH.cf2),
        Symptom(name="تشقق الثمار وتلفها", cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60),
    )
    def powdery_mildew_full(self, cf1, cf2, cf3):
        self._diagnose_full("البياض الدقيقي - العنب", cf1, cf2, cf3)

    @Rule(
        OR(
            AND(Symptom(name="مسحوق أبيض على سطح الأوراق والثمار", cf=MATCH.cf1),
                Symptom(name="تشوه الثمار وتوقف نموها", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="مسحوق أبيض على سطح الأوراق والثمار", cf=MATCH.cf1),
                Symptom(name="تشقق الثمار وتلفها", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="تشوه الثمار وتوقف نموها", cf=MATCH.cf1),
                Symptom(name="تشقق الثمار وتلفها", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
        )
    )
    def powdery_mildew_partial(self, cf1, cf2):
        self._diagnose_partial("البياض الدقيقي - العنب", cf1, cf2)

    @Rule(
        OR(
            Symptom(name="مسحوق أبيض على سطح الأوراق والثمار", cf=MATCH.cf1),
            Symptom(name="تشوه الثمار وتوقف نموها", cf=MATCH.cf1),
            Symptom(name="تشقق الثمار وتلفها", cf=MATCH.cf1),
        ),
        TEST(lambda cf1: cf1 >= 60),
    )
    def powdery_mildew_weak(self, cf1):
        self._diagnose_weak("البياض الدقيقي - العنب", cf1)

    @Rule(Fact(disease="البياض الدقيقي - العنب"))
    def powdery_mildew_treatment(self):
        self._treat(
            disease_name="البياض الدقيقي - العنب",
            cause="مرض البياض الدقيقي في العنب يُسببه الفطر Erysiphe necator.",
            steps=[
                "رش الكبريت القابل للبلل أو مبيدات تحتوي على Myclobutanil",
                "التكرار كل 10 أيام خلال الفترة الحساسة (قبل الإزهار وحتى نضج الثمار)",
                "تقليل الرطوبة وتحسين التهوية بالتقليم",
                "إزالة الأجزاء المصابة وتقليل التزاحم بين العناقيد",
            ],
        )

    # ── عفن الجذور ──────────────────────────────────────────────────────────

    @Rule(
        Symptom(name="ذبول الأوراق وسقوطها", cf=MATCH.cf1),
        Symptom(name="بقع صفراء على الأوراق", cf=MATCH.cf2),
        Symptom(name="توقف نمو النبات أو موته المفاجئ", cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60),
    )
    def root_rot_full(self, cf1, cf2, cf3):
        self._diagnose_full("عفن الجذور", cf1, cf2, cf3, multiplier=CF_VERY_HIGH)

    @Rule(
        OR(
            AND(Symptom(name="ذبول الأوراق وسقوطها", cf=MATCH.cf1),
                Symptom(name="بقع صفراء على الأوراق", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="ذبول الأوراق وسقوطها", cf=MATCH.cf1),
                Symptom(name="توقف نمو النبات أو موته المفاجئ", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="بقع صفراء على الأوراق", cf=MATCH.cf1),
                Symptom(name="توقف نمو النبات أو موته المفاجئ", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
        ),
        salience=6,
    )
    def root_rot_partial(self, cf1, cf2):
        self._diagnose_partial("عفن الجذور", cf1, cf2, hint=HINT_SIMILAR_DISEASE)

    @Rule(
        OR(
            Symptom(name="ذبول الأوراق وسقوطها", cf=MATCH.cf1),
            Symptom(name="بقع صفراء على الأوراق", cf=MATCH.cf1),
            Symptom(name="توقف نمو النبات أو موته المفاجئ", cf=MATCH.cf1),
        ),
        TEST(lambda cf1: cf1 >= 60),
        salience=5,
    )
    def root_rot_weak(self, cf1):
        self._diagnose_weak("عفن الجذور", cf1, hint=HINT_SIMILAR_DISEASE)

    @Rule(Fact(disease="عفن الجذور"))
    def root_rot_treatment(self):
        self._treat(
            disease_name="عفن الجذور - العنب",
            cause="مرض عفن الجذور في العنب يُسببه الفطر Phytophthora spp.",
            steps=[
                "تحسين صرف التربة لتجنب تجمع المياه",
                "تقليل الري في التربة الطينية الثقيلة",
                "إزالة النباتات المصابة بالكامل لمنع الانتشار",
                "يمكن استخدام مبيدات فطرية مثل Metalaxyl حسب توصيات المختصين",
            ],
        )
