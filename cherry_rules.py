from experta import Rule, Fact, MATCH, TEST, OR, AND
from core import (
    Symptom, PlantDiagnosisEngine,
    CF_FULL, CF_PARTIAL, CF_WEAK,
    HINT_MORE_SYMPTOMS,
)

class CherryRules(PlantDiagnosisEngine):

    SYMPTOMS = [
        "بقع بيضاء على سطح الأوراق",
        "تشوه الأوراق",
        "تبقع وتلف الثمار",
        "بقع أرجوانية أو حمراء على الأوراق",
        "ثقوب دائرية في الأوراق",
        "بقع داكنة على الثمار",
        "بقع بنية طرية على الثمار",
        "ظهور دوائر بيضاء من الأبواغ",
        "تعفن الثمار وتساقطها",
        "تقرحات غائرة على الساق أو الأغصان",
        "تسرب صمغ من أماكن التقرحات",
        "ذبول مفاجئ للأوراق أو الأغصان",
    ]

    # ── البياض الدقيقي ──────────────────────────────────────────────────────

    @Rule(
        Symptom(name="بقع بيضاء على سطح الأوراق", cf=MATCH.cf1),
        Symptom(name="تشوه الأوراق", cf=MATCH.cf2),
        Symptom(name="تبقع وتلف الثمار", cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60),
    )
    def powdery_mildew_full(self, cf1, cf2, cf3):
        self._diagnose_full("البياض الدقيقي", cf1, cf2, cf3)

    @Rule(
        OR(
            AND(Symptom(name="بقع بيضاء على سطح الأوراق", cf=MATCH.cf1),
                Symptom(name="تشوه الأوراق", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="بقع بيضاء على سطح الأوراق", cf=MATCH.cf1),
                Symptom(name="تبقع وتلف الثمار", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="تشوه الأوراق", cf=MATCH.cf1),
                Symptom(name="تبقع وتلف الثمار", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
        )
    )
    def powdery_mildew_partial(self, cf1, cf2):
        self._diagnose_partial("البياض الدقيقي", cf1, cf2)

    @Rule(
        OR(
            Symptom(name="بقع بيضاء على سطح الأوراق", cf=MATCH.cf1),
            Symptom(name="تشوه الأوراق", cf=MATCH.cf1),
            Symptom(name="تبقع وتلف الثمار", cf=MATCH.cf1),
        ),
        TEST(lambda cf1: cf1 >= 60),
    )
    def powdery_mildew_weak(self, cf1):
        self._diagnose_weak("البياض الدقيقي", cf1)

    @Rule(Fact(disease="البياض الدقيقي"))
    def powdery_mildew_treatment(self):
        self._treat(
            disease_name="البياض الدقيقي - الكرز",
            cause="مرض البياض الدقيقي في الكرز يُسببه الفطر Podosphaera clandestina.",
            steps=[
                "رش الكبريت الميكروني أو Triadimefon عند ظهور أولى العلامات",
                "إعادة الرش كل 10–14 يوم عند الحاجة",
                "إزالة الأوراق المصابة لتحسين التهوية",
                "تقليم الفروع لتقليل الرطوبة حول النبات",
            ],
        )

    # ── تبقع الأوراق ────────────────────────────────────────────────────────

    @Rule(
        Symptom(name="بقع أرجوانية أو حمراء على الأوراق", cf=MATCH.cf1),
        Symptom(name="ثقوب دائرية في الأوراق", cf=MATCH.cf2),
        Symptom(name="بقع داكنة على الثمار", cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60),
    )
    def shot_hole_full(self, cf1, cf2, cf3):
        self._diagnose_full("تَبَقُّع الأوراق", cf1, cf2, cf3)

    @Rule(
        OR(
            AND(Symptom(name="بقع أرجوانية أو حمراء على الأوراق", cf=MATCH.cf1),
                Symptom(name="ثقوب دائرية في الأوراق", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="بقع أرجوانية أو حمراء على الأوراق", cf=MATCH.cf1),
                Symptom(name="بقع داكنة على الثمار", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="ثقوب دائرية في الأوراق", cf=MATCH.cf1),
                Symptom(name="بقع داكنة على الثمار", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
        )
    )
    def shot_hole_partial(self, cf1, cf2):
        self._diagnose_partial("تَبَقُّع الأوراق", cf1, cf2)

    @Rule(
        OR(
            Symptom(name="بقع أرجوانية أو حمراء على الأوراق", cf=MATCH.cf1),
            Symptom(name="ثقوب دائرية في الأوراق", cf=MATCH.cf1),
            Symptom(name="بقع داكنة على الثمار", cf=MATCH.cf1),
        ),
        TEST(lambda cf1: cf1 >= 60),
    )
    def shot_hole_weak(self, cf1):
        self._diagnose_weak("تَبَقُّع الأوراق", cf1)

    @Rule(Fact(disease="تَبَقُّع الأوراق"))
    def shot_hole_treatment(self):
        self._treat(
            disease_name="تَبَقُّع الأوراق - الكرز",
            cause="مرض تبقّع الأوراق في الكرز يُسببه الفطر Blumeriella jaapii.",
            steps=[
                "رش مبيدات فطرية تحتوي على النحاس أو Captan خلال الخريف والربيع",
                "إزالة الأوراق والثمار المصابة وتقليل الرطوبة",
                "تحسين التهوية من خلال تقليم جيد",
            ],
        )

    # ── عفن الثمار البني ────────────────────────────────────────────────────

    @Rule(
        Symptom(name="بقع بنية طرية على الثمار", cf=MATCH.cf1),
        Symptom(name="ظهور دوائر بيضاء من الأبواغ", cf=MATCH.cf2),
        Symptom(name="تعفن الثمار وتساقطها", cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60),
    )
    def brown_rot_full(self, cf1, cf2, cf3):
        self._diagnose_full("عفن الثمار البني", cf1, cf2, cf3)

    @Rule(
        OR(
            AND(Symptom(name="بقع بنية طرية على الثمار", cf=MATCH.cf1),
                Symptom(name="ظهور دوائر بيضاء من الأبواغ", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="بقع بنية طرية على الثمار", cf=MATCH.cf1),
                Symptom(name="تعفن الثمار وتساقطها", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="ظهور دوائر بيضاء من الأبواغ", cf=MATCH.cf1),
                Symptom(name="تعفن الثمار وتساقطها", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
        )
    )
    def brown_rot_partial(self, cf1, cf2):
        self._diagnose_partial("عفن الثمار البني", cf1, cf2)

    @Rule(
        OR(
            Symptom(name="بقع بنية طرية على الثمار", cf=MATCH.cf1),
            Symptom(name="ظهور دوائر بيضاء من الأبواغ", cf=MATCH.cf1),
            Symptom(name="تعفن الثمار وتساقطها", cf=MATCH.cf1),
        ),
        TEST(lambda cf1: cf1 >= 60),
    )
    def brown_rot_weak(self, cf1):
        self._diagnose_weak("عفن الثمار البني", cf1)

    @Rule(Fact(disease="عفن الثمار البني"))
    def brown_rot_treatment(self):
        self._treat(
            disease_name="عفن الثمار البني - الكرز",
            cause="مرض عفن الثمار البني في الكرز يُسببه الفطر Monilinia fructicola.",
            steps=[
                "إزالة الثمار المصابة وعدم تركها على الشجرة أو في الأرض",
                "الرش بمبيدات فطرية مثل Captan أو Myclobutanil في فترة الإزهار وقبل القطاف",
                "تقليم الفروع المصابة وتحسين التهوية",
                "تقليل الري وقت نضج الثمار لتقليل الرطوبة الزائدة",
            ],
        )

    # ── سرطان اللحاء البكتيري ───────────────────────────────────────────────

    @Rule(
        Symptom(name="تقرحات غائرة على الساق أو الأغصان", cf=MATCH.cf1),
        Symptom(name="تسرب صمغ من أماكن التقرحات", cf=MATCH.cf2),
        Symptom(name="ذبول مفاجئ للأوراق أو الأغصان", cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60),
    )
    def bacterial_canker_full(self, cf1, cf2, cf3):
        self._diagnose_full("سرطان اللحاء البكتيري", cf1, cf2, cf3)

    @Rule(
        OR(
            AND(Symptom(name="تقرحات غائرة على الساق أو الأغصان", cf=MATCH.cf1),
                Symptom(name="تسرب صمغ من أماكن التقرحات", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="تقرحات غائرة على الساق أو الأغصان", cf=MATCH.cf1),
                Symptom(name="ذبول مفاجئ للأوراق أو الأغصان", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="تسرب صمغ من أماكن التقرحات", cf=MATCH.cf1),
                Symptom(name="ذبول مفاجئ للأوراق أو الأغصان", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
        )
    )
    def bacterial_canker_partial(self, cf1, cf2):
        self._diagnose_partial("سرطان اللحاء البكتيري", cf1, cf2)

    @Rule(
        OR(
            Symptom(name="تقرحات غائرة على الساق أو الأغصان", cf=MATCH.cf1),
            Symptom(name="تسرب صمغ من أماكن التقرحات", cf=MATCH.cf1),
            Symptom(name="ذبول مفاجئ للأوراق أو الأغصان", cf=MATCH.cf1),
        ),
        TEST(lambda cf1: cf1 >= 60),
    )
    def bacterial_canker_weak(self, cf1):
        self._diagnose_weak("سرطان اللحاء البكتيري", cf1)

    @Rule(Fact(disease="سرطان اللحاء البكتيري"))
    def bacterial_canker_treatment(self):
        self._treat(
            disease_name="سرطان اللحاء البكتيري - الكرز",
            cause=(
                "مرض سرطان اللحاء البكتيري في الكرز يُسببه "
                "البكتيريا Pseudomonas syringae pv. syringae."
            ),
            steps=[
                "تقليم الأغصان المصابة في الصيف فقط (لتقليل انتشار البكتيريا)",
                "رش مضادات بكتيرية مثل أوكسي كلوريد النحاس بعد التقليم",
                "تطهير أدوات التقليم بمحلول كحولي أو مبيض مخفف",
                "زراعة أصناف مقاومة والابتعاد عن الزراعة في الأراضي المجهدة",
            ],
        )
