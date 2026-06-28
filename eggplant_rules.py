from experta import Rule, Fact, MATCH, TEST, OR, AND
from core import (
    Symptom, PlantDiagnosisEngine,
    CF_FULL, CF_PARTIAL, CF_WEAK,
    HINT_MORE_SYMPTOMS, HINT_SIMILAR_DISEASE,
)

class EggplantRules(PlantDiagnosisEngine):

    SYMPTOMS = [
        "ذبول مفاجئ للنبات بدون اصفرار سابق",
        "تحول الساق الداخلي إلى اللون البني – يظهر عند قطع الجذع انسياب سائل مخاطي",
        "موت النبات بالكامل، خصوصًا في الطقس الدافئ والرطب",
        "اصفرار الأوراق السفلية تدريجيًا، ثم ذبولها",
        "تظهر بقع بنية على الأوعية الوعائية داخل الساق عند تقطيعها",
        "ضعف النمو وتراجع إنتاج الثمار",
        "بقع بنية مائية على الثمار، خاصة في النبات السفلي",
        "تعفن الساقين عند قاعدة النبات، مع ظهور طبقة بيضاء زغبية",
        "بقع دائرية داكنة على الأوراق، غالبًا محاطة بهالة صفراء",
        'انثقاب البقع وتحولها إلى "ثقوب" عند تقدم الإصابة',
        "تساقط الأوراق وضعف التمثيل الضوئي",
        "إعوجاجات وتفحم في قاعدة الساق عند سطح التربة",
        'ظهور شبكة من الفطريات البيضاء وثم "جذور سوداء" (sclerotia)',
        "ذبول وموت مفاجئ للنبات حتى في الطقس المعتدل",
    ]

    # ── الذبول البكتيري ─────────────────────────────────────────────────────

    @Rule(
        Symptom(name="ذبول مفاجئ للنبات بدون اصفرار سابق", cf=MATCH.cf1),
        Symptom(
            name="تحول الساق الداخلي إلى اللون البني – يظهر عند قطع الجذع انسياب سائل مخاطي",
            cf=MATCH.cf2,
        ),
        Symptom(name="موت النبات بالكامل، خصوصًا في الطقس الدافئ والرطب", cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60),
    )
    def bacterial_wilt_full(self, cf1, cf2, cf3):
        self._diagnose_full("الذبول البكتيري", cf1, cf2, cf3)

    @Rule(
        OR(
            AND(Symptom(name="ذبول مفاجئ للنبات بدون اصفرار سابق", cf=MATCH.cf1),
                Symptom(name="تحول الساق الداخلي إلى اللون البني – يظهر عند قطع الجذع انسياب سائل مخاطي", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="ذبول مفاجئ للنبات بدون اصفرار سابق", cf=MATCH.cf1),
                Symptom(name="موت النبات بالكامل، خصوصًا في الطقس الدافئ والرطب", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="تحول الساق الداخلي إلى اللون البني – يظهر عند قطع الجذع انسياب سائل مخاطي", cf=MATCH.cf1),
                Symptom(name="موت النبات بالكامل، خصوصًا في الطقس الدافئ والرطب", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
        )
    )
    def bacterial_wilt_partial(self, cf1, cf2):
        self._diagnose_partial("الذبول البكتيري", cf1, cf2)

    @Rule(
        OR(
            Symptom(name="ذبول مفاجئ للنبات بدون اصفرار سابق", cf=MATCH.cf1),
            Symptom(name="تحول الساق الداخلي إلى اللون البني – يظهر عند قطع الجذع انسياب سائل مخاطي", cf=MATCH.cf1),
            Symptom(name="موت النبات بالكامل، خصوصًا في الطقس الدافئ والرطب", cf=MATCH.cf1),
        ),
        TEST(lambda cf1: cf1 >= 60),
    )
    def bacterial_wilt_weak(self, cf1):
        self._diagnose_weak("الذبول البكتيري", cf1)

    @Rule(Fact(disease="الذبول البكتيري"))
    def bacterial_wilt_treatment(self):
        self._treat(
            disease_name="مرض الذبول البكتيري - الباذنجان",
            cause=(
                "مرض الذبول البكتيري في الباذنجان يُسببه "
                "البكتيريا Ralstonia solanacearum."
            ),
            steps=[
                "إزالة النباتات المصابة فورًا والتخلص منها (لا تُعاد كسماد)",
                "تجنب زراعة الباذنجان أو البطاطا في نفس التربة المصابة لمدة 2–3 سنوات",
                "تعقيم أدوات العمل بين النباتات",
                "تحسين تصريف التربة وتقليل الرطوبة حول الجذور",
                "لا يوجد علاج فعّال، لذا يُركز على الوقاية فقط",
            ],
        )

    # ── الذبول الفيوزاريومي ─────────────────────────────────────────────────

    @Rule(
        Symptom(name="اصفرار الأوراق السفلية تدريجيًا، ثم ذبولها", cf=MATCH.cf1),
        Symptom(name="تظهر بقع بنية على الأوعية الوعائية داخل الساق عند تقطيعها", cf=MATCH.cf2),
        Symptom(name="ضعف النمو وتراجع إنتاج الثمار", cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60),
    )
    def fusarium_wilt_full(self, cf1, cf2, cf3):
        self._diagnose_full("الذبول الفيوزاريومي", cf1, cf2, cf3)

    @Rule(
        OR(
            AND(Symptom(name="اصفرار الأوراق السفلية تدريجيًا، ثم ذبولها", cf=MATCH.cf1),
                Symptom(name="تظهر بقع بنية على الأوعية الوعائية داخل الساق عند تقطيعها", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="اصفرار الأوراق السفلية تدريجيًا، ثم ذبولها", cf=MATCH.cf1),
                Symptom(name="ضعف النمو وتراجع إنتاج الثمار", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="تظهر بقع بنية على الأوعية الوعائية داخل الساق عند تقطيعها", cf=MATCH.cf1),
                Symptom(name="ضعف النمو وتراجع إنتاج الثمار", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
        )
    )
    def fusarium_wilt_partial(self, cf1, cf2):
        self._diagnose_partial("الذبول الفيوزاريومي", cf1, cf2)

    @Rule(
        OR(
            Symptom(name="اصفرار الأوراق السفلية تدريجيًا، ثم ذبولها", cf=MATCH.cf1),
            Symptom(name="تظهر بقع بنية على الأوعية الوعائية داخل الساق عند تقطيعها", cf=MATCH.cf1),
            Symptom(name="ضعف النمو وتراجع إنتاج الثمار", cf=MATCH.cf1),
        ),
        TEST(lambda cf1: cf1 >= 60),
        salience=10,
    )
    def fusarium_wilt_weak(self, cf1):
        self._diagnose_weak("الذبول الفيوزاريومي", cf1, hint=HINT_SIMILAR_DISEASE)

    @Rule(Fact(disease="الذبول الفيوزاريومي"))
    def fusarium_wilt_treatment(self):
        self._treat(
            disease_name="مرض الذبول الفيوزاريومي - الباذنجان",
            cause=(
                "مرض الذبول الفيوزاريومي في الباذنجان يُسببه "
                "الفطر Fusarium oxysporum f. sp. melongenae."
            ),
            steps=[
                "زراعة أصناف مقاومة للمرض (معتمدة)",
                "تدوير المحاصيل وعدم زراعة الباذنجان أو البطاطا أو الطماطم في نفس التربة لمدة 3–4 سنوات",
                "تعقيم التربة بالبخار أو المواد الكيميائية المناسبة",
                "تحسين تصريف التربة وتقليل الري الزائد",
                "إزالة وإتلاف النباتات المصابة",
            ],
        )

    # ── عفن الفاكهة والفيوغثور ──────────────────────────────────────────────

    @Rule(
        Symptom(name="بقع بنية مائية على الثمار، خاصة في النبات السفلي", cf=MATCH.cf1),
        Symptom(name="تعفن الساقين عند قاعدة النبات، مع ظهور طبقة بيضاء زغبية", cf=MATCH.cf2),
        Symptom(name="ضعف النمو وتراجع إنتاج الثمار", cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60),
    )
    def phytophthora_blight_full(self, cf1, cf2, cf3):
        self._diagnose_full("عفن الفاكهة والفيوغثور", cf1, cf2, cf3)

    @Rule(
        OR(
            AND(Symptom(name="بقع بنية مائية على الثمار، خاصة في النبات السفلي", cf=MATCH.cf1),
                Symptom(name="تعفن الساقين عند قاعدة النبات، مع ظهور طبقة بيضاء زغبية", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="بقع بنية مائية على الثمار، خاصة في النبات السفلي", cf=MATCH.cf1),
                Symptom(name="ضعف النمو وتراجع إنتاج الثمار", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="تعفن الساقين عند قاعدة النبات، مع ظهور طبقة بيضاء زغبية", cf=MATCH.cf1),
                Symptom(name="ضعف النمو وتراجع إنتاج الثمار", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
        )
    )
    def phytophthora_blight_partial(self, cf1, cf2):
        self._diagnose_partial("عفن الفاكهة والفيوغثور", cf1, cf2)

    @Rule(
        OR(
            Symptom(name="بقع بنية مائية على الثمار، خاصة في النبات السفلي", cf=MATCH.cf1),
            Symptom(name="تعفن الساقين عند قاعدة النبات، مع ظهور طبقة بيضاء زغبية", cf=MATCH.cf1),
            Symptom(name="ضعف النمو وتراجع إنتاج الثمار", cf=MATCH.cf1),
        ),
        TEST(lambda cf1: cf1 >= 60),
        salience=5,
    )
    def phytophthora_blight_weak(self, cf1):
        self._diagnose_weak("عفن الفاكهة والفيوغثور", cf1, hint=HINT_SIMILAR_DISEASE)

    @Rule(Fact(disease="عفن الفاكهة والفيوغثور"))
    def phytophthora_blight_treatment(self):
        self._treat(
            disease_name="مرض عفن الفاكهة والفيوغثور - الباذنجان",
            cause=(
                "مرض عفن الفاكهة والفيوغثور في الباذنجان "
                "يُسببه الفطر Phytophthora capsici."
            ),
            steps=[
                "تحسين تصريف التربة وتقليل الري الزائد",
                "رش النبات بمبيد فطري مضاد للفيوغثور مثل مبيدات تحتوي على ميتالاكسيل",
                "إزالة وإتلاف النباتات المصابة فورًا",
                "تعقيم التربة قبل الزراعة الجديدة",
                "تجنب الزراعة الكثيفة وتحسين التهوية بين النباتات",
            ],
        )

    # ── تبقع الأوراق (Cercospora) ────────────────────────────────────────────

    @Rule(
        Symptom(name="بقع دائرية داكنة على الأوراق، غالبًا محاطة بهالة صفراء", cf=MATCH.cf1),
        Symptom(name='انثقاب البقع وتحولها إلى "ثقوب" عند تقدم الإصابة', cf=MATCH.cf2),
        Symptom(name="تساقط الأوراق وضعف التمثيل الضوئي", cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60),
    )
    def leaf_spot_full(self, cf1, cf2, cf3):
        self._diagnose_full("تبقّع الأوراق", cf1, cf2, cf3)

    @Rule(
        OR(
            AND(Symptom(name="بقع دائرية داكنة على الأوراق، غالبًا محاطة بهالة صفراء", cf=MATCH.cf1),
                Symptom(name='انثقاب البقع وتحولها إلى "ثقوب" عند تقدم الإصابة', cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="بقع دائرية داكنة على الأوراق، غالبًا محاطة بهالة صفراء", cf=MATCH.cf1),
                Symptom(name="تساقط الأوراق وضعف التمثيل الضوئي", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name='انثقاب البقع وتحولها إلى "ثقوب" عند تقدم الإصابة', cf=MATCH.cf1),
                Symptom(name="تساقط الأوراق وضعف التمثيل الضوئي", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
        )
    )
    def leaf_spot_partial(self, cf1, cf2):
        self._diagnose_partial("تبقّع الأوراق", cf1, cf2)

    @Rule(
        OR(
            Symptom(name="بقع دائرية داكنة على الأوراق، غالبًا محاطة بهالة صفراء", cf=MATCH.cf1),
            Symptom(name='انثقاب البقع وتحولها إلى "ثقوب" عند تقدم الإصابة', cf=MATCH.cf1),
            Symptom(name="تساقط الأوراق وضعف التمثيل الضوئي", cf=MATCH.cf1),
        ),
        TEST(lambda cf1: cf1 >= 60),
    )
    def leaf_spot_weak(self, cf1):
        self._diagnose_weak("تبقّع الأوراق", cf1)

    @Rule(Fact(disease="تبقّع الأوراق"))
    def leaf_spot_treatment(self):
        self._treat(
            disease_name="مرض تبقّع الأوراق (Cercospora) - الباذنجان",
            cause="مرض تبقّع الأوراق في الباذنجان يُسببه الفطر Alternaria solani.",
            steps=[
                "رش النبات بمبيد فطري وقائي مثل مبيدات تحتوي على النحاس أو البنزيميدازول",
                "إزالة الأوراق المصابة فورًا ومنع تراكم بقايا النباتات",
                "تحسين التهوية وتقليل الرطوبة حول النباتات",
                "تجنب الري بالرش والتركيز على الري الجذري",
                "زراعة أصناف مقاومة للمرض إن أمكن",
            ],
        )

    # ── عفن الساق (Sclerotium Rot) ──────────────────────────────────────────

    @Rule(
        Symptom(name="إعوجاجات وتفحم في قاعدة الساق عند سطح التربة", cf=MATCH.cf1),
        Symptom(name='ظهور شبكة من الفطريات البيضاء وثم "جذور سوداء" (sclerotia)', cf=MATCH.cf2),
        Symptom(name="ذبول وموت مفاجئ للنبات حتى في الطقس المعتدل", cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60),
    )
    def stem_rot_full(self, cf1, cf2, cf3):
        self._diagnose_full("عفن الساق", cf1, cf2, cf3)

    @Rule(
        OR(
            AND(Symptom(name="إعوجاجات وتفحم في قاعدة الساق عند سطح التربة", cf=MATCH.cf1),
                Symptom(name='ظهور شبكة من الفطريات البيضاء وثم "جذور سوداء" (sclerotia)', cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="إعوجاجات وتفحم في قاعدة الساق عند سطح التربة", cf=MATCH.cf1),
                Symptom(name="ذبول وموت مفاجئ للنبات حتى في الطقس المعتدل", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name='ظهور شبكة من الفطريات البيضاء وثم "جذور سوداء" (sclerotia)', cf=MATCH.cf1),
                Symptom(name="ذبول وموت مفاجئ للنبات حتى في الطقس المعتدل", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
        )
    )
    def stem_rot_partial(self, cf1, cf2):
        self._diagnose_partial("عفن الساق", cf1, cf2)

    @Rule(
        OR(
            Symptom(name="إعوجاجات وتفحم في قاعدة الساق عند سطح التربة", cf=MATCH.cf1),
            Symptom(name='ظهور شبكة من الفطريات البيضاء وثم "جذور سوداء" (sclerotia)', cf=MATCH.cf1),
            Symptom(name="ذبول وموت مفاجئ للنبات حتى في الطقس المعتدل", cf=MATCH.cf1),
        ),
        TEST(lambda cf1: cf1 >= 60),
    )
    def stem_rot_weak(self, cf1):
        self._diagnose_weak("عفن الساق", cf1)

    @Rule(Fact(disease="عفن الساق"))
    def stem_rot_treatment(self):
        self._treat(
            disease_name="مرض عفن الساق (Sclerotium Rot) - الباذنجان",
            cause="مرض عفن الساق في الباذنجان يُسببه الفطر Rhizoctonia solani.",
            steps=[
                "إزالة وإتلاف النباتات المصابة فورًا (لا تُعاد كسماد)",
                "تعقيم التربة باستخدام البخار أو مبيدات الفطريات الوقائية",
                "تحسين تصريف التربة وتقليل الرطوبة حول قاعدة النباتات",
                "تجنب الزراعة الكثيفة وتحسين التهوية",
                "استخدام أصناف مقاومة إن أمكن",
            ],
        )
