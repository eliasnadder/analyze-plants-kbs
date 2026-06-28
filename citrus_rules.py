from experta import Rule, Fact, MATCH, TEST, OR, AND
from core import (
    Symptom, PlantDiagnosisEngine,
    CF_VERY_HIGH, CF_FULL, CF_HIGH_3,
    CF_MED_HIGH, CF_PARTIAL, CF_MEDIUM,
    CF_MED_LOW, CF_LOW,
    HINT_MORE_SYMPTOMS, HINT_SIMILAR_DISEASE,
)

class CitrusRules(PlantDiagnosisEngine):

    SYMPTOMS = [
        "اصفرار وتمدد للأوراق والشعيرات الخشبية",
        "ذبول وفناء أجزاء من الفروع",
        "إفرازات صمغية وردية أو رمادية في الجذوع",
        "بقع داكنة أو تكاثف للنسيج الخشبي تحت اللحاء",
        "إفرازات صمغية سوداء أو بنية عند قاعدة الجذع",
        "تقرحات أو تصدعات في اللحاء بالقرب من سطح التربة",
        "ذبول الأصناف وضعف نمو الأوراق",
        "اختناق النسيج الوعائي وموت الفروع",
        "تجعد أو تساقط الأوراق",
        "ضعف في النمو، وقلة الإنتاجية",
        "بقع داكنة غائرة على الثمار",
        "تساقط مبكر للثمار",
        "بقع صغيرة على الأوراق في بعض الحالات",
        "تقرحات مائية على الأوراق والسيقان والثمار",
        "يحيط بها هالة صفراء",
        "بقع صفراء-بنية لامعة على السطح السفلي للأوراق",
    ]

    # ── مرض مالسيكو (4 أعراض) ───────────────────────────────────────────────

    @Rule(
        Symptom(name="اصفرار وتمدد للأوراق والشعيرات الخشبية", cf=MATCH.cf1),
        Symptom(name="ذبول وفناء أجزاء من الفروع", cf=MATCH.cf2),
        Symptom(name="إفرازات صمغية وردية أو رمادية في الجذوع", cf=MATCH.cf3),
        Symptom(name="بقع داكنة أو تكاثف للنسيج الخشبي تحت اللحاء", cf=MATCH.cf4),
        TEST(lambda cf1, cf2, cf3, cf4: min(cf1, cf2, cf3, cf4) >= 60),
    )
    def mal_secco_full(self, cf1, cf2, cf3, cf4):
        self._diagnose_full("مالسيكو", cf1, cf2, cf3, cf4, multiplier=CF_VERY_HIGH)

    @Rule(
        OR(
            AND(Symptom(name="اصفرار وتمدد للأوراق والشعيرات الخشبية", cf=MATCH.cf1),
                Symptom(name="ذبول وفناء أجزاء من الفروع", cf=MATCH.cf2),
                Symptom(name="إفرازات صمغية وردية أو رمادية في الجذوع", cf=MATCH.cf3)),
            AND(Symptom(name="ذبول وفناء أجزاء من الفروع", cf=MATCH.cf1),
                Symptom(name="إفرازات صمغية وردية أو رمادية في الجذوع", cf=MATCH.cf2),
                Symptom(name="بقع داكنة أو تكاثف للنسيج الخشبي تحت اللحاء", cf=MATCH.cf3)),
            AND(Symptom(name="اصفرار وتمدد للأوراق والشعيرات الخشبية", cf=MATCH.cf1),
                Symptom(name="إفرازات صمغية وردية أو رمادية في الجذوع", cf=MATCH.cf2),
                Symptom(name="بقع داكنة أو تكاثف للنسيج الخشبي تحت اللحاء", cf=MATCH.cf3)),
            AND(Symptom(name="اصفرار وتمدد للأوراق والشعيرات الخشبية", cf=MATCH.cf1),
                Symptom(name="ذبول وفناء أجزاء من الفروع", cf=MATCH.cf2),
                Symptom(name="بقع داكنة أو تكاثف للنسيج الخشبي تحت اللحاء", cf=MATCH.cf3)),
        ),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60),
    )
    def mal_secco_partial_strong(self, cf1, cf2, cf3):
        # 3 من 4 أعراض: تشخيص مؤكد جزئياً
        self._diagnose(
            "مالسيكو", cf1, cf2, cf3,
            multiplier=CF_HIGH_3,
            label="تشخيص مؤكد جزئيًا",
            hint=HINT_MORE_SYMPTOMS,
        )

    @Rule(
        OR(
            AND(Symptom(name="اصفرار وتمدد للأوراق والشعيرات الخشبية", cf=MATCH.cf1),
                Symptom(name="ذبول وفناء أجزاء من الفروع", cf=MATCH.cf2)),
            AND(Symptom(name="إفرازات صمغية وردية أو رمادية في الجذوع", cf=MATCH.cf1),
                Symptom(name="بقع داكنة أو تكاثف للنسيج الخشبي تحت اللحاء", cf=MATCH.cf2)),
            AND(Symptom(name="اصفرار وتمدد للأوراق والشعيرات الخشبية", cf=MATCH.cf1),
                Symptom(name="بقع داكنة أو تكاثف للنسيج الخشبي تحت اللحاء", cf=MATCH.cf2)),
        ),
        TEST(lambda cf1, cf2: min(cf1, cf2) >= 60),
    )
    def mal_secco_partial_basic(self, cf1, cf2):
        self._diagnose_partial("مالسيكو", cf1, cf2, multiplier=CF_MEDIUM)

    @Rule(
        OR(
            Symptom(name="اصفرار وتمدد للأوراق والشعيرات الخشبية", cf=MATCH.cf1),
            Symptom(name="ذبول وفناء أجزاء من الفروع", cf=MATCH.cf1),
            Symptom(name="إفرازات صمغية وردية أو رمادية في الجذوع", cf=MATCH.cf1),
            Symptom(name="بقع داكنة أو تكاثف للنسيج الخشبي تحت اللحاء", cf=MATCH.cf1),
        ),
        TEST(lambda cf1: cf1 >= 60),
    )
    def mal_secco_weak(self, cf1):
        self._diagnose_weak("مالسيكو", cf1, multiplier=CF_MED_LOW)

    @Rule(Fact(disease="مالسيكو"))
    def mal_secco_treatment(self):
        self._treat(
            disease_name="مرض مالسيكو - الحمضيات",
            cause="مرض مالسيكو في الحمضيات يُسببه الفطر Plenodomus tracheiphilus.",
            steps=[
                "تقليم الأفرع المصابة فورًا والتخلص منها بالحرق",
                "تطهير أدوات التقليم لمنع الانتشار",
                "رش مبيد فطري نحاسي بعد التقليم",
                "زراعة أصناف مقاومة وتحسين صرف التربة",
            ],
        )

    # ── عفن الجذور والصمغ ───────────────────────────────────────────────────

    @Rule(
        Symptom(name="إفرازات صمغية سوداء أو بنية عند قاعدة الجذع", cf=MATCH.cf1),
        Symptom(name="تقرحات أو تصدعات في اللحاء بالقرب من سطح التربة", cf=MATCH.cf2),
        Symptom(name="ذبول الأصناف وضعف نمو الأوراق", cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60),
    )
    def root_rot_full(self, cf1, cf2, cf3):
        self._diagnose_full("عفن الجذور والصمغ", cf1, cf2, cf3)

    @Rule(
        OR(
            AND(Symptom(name="إفرازات صمغية سوداء أو بنية عند قاعدة الجذع", cf=MATCH.cf1),
                Symptom(name="تقرحات أو تصدعات في اللحاء بالقرب من سطح التربة", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="إفرازات صمغية سوداء أو بنية عند قاعدة الجذع", cf=MATCH.cf1),
                Symptom(name="ذبول الأصناف وضعف نمو الأوراق", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="تقرحات أو تصدعات في اللحاء بالقرب من سطح التربة", cf=MATCH.cf1),
                Symptom(name="ذبول الأصناف وضعف نمو الأوراق", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
        )
    )
    def root_rot_partial(self, cf1, cf2):
        self._diagnose_partial("عفن الجذور والصمغ", cf1, cf2)

    @Rule(
        OR(
            Symptom(name="إفرازات صمغية سوداء أو بنية عند قاعدة الجذع", cf=MATCH.cf1),
            Symptom(name="تقرحات أو تصدعات في اللحاء بالقرب من سطح التربة", cf=MATCH.cf1),
            Symptom(name="ذبول الأصناف وضعف نمو الأوراق", cf=MATCH.cf1),
        ),
        TEST(lambda cf1: cf1 >= 60),
    )
    def root_rot_weak(self, cf1):
        self._diagnose_weak("عفن الجذور والصمغ", cf1)

    @Rule(Fact(disease="عفن الجذور والصمغ"))
    def root_rot_treatment(self):
        self._treat(
            disease_name="مرض عفن الجذور / الصمغ - الحمضيات",
            cause="مرض عفن الجذور في الحمضيات يُسببه الفطر Phytophthora spp.",
            steps=[
                "تحسين تصريف التربة وتقليل الري",
                "رش أو تطهير الجذوع بمبيدات فطرية مضادة لـ Phytophthora (مثل فوندازول)",
                "معالجة التربة بمبيد فطري عند الزراعة",
                "زراعة أشجار على تلال مرتفعة لتقليل تجمع المياه",
                "التخلص من الأشجار الشديدة الإصابة",
            ],
        )

    # ── فيروس ترايستيزا ─────────────────────────────────────────────────────

    @Rule(
        Symptom(name="اختناق النسيج الوعائي وموت الفروع", cf=MATCH.cf1),
        Symptom(name="تجعد أو تساقط الأوراق", cf=MATCH.cf2),
        Symptom(name="ضعف في النمو، وقلة الإنتاجية", cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60),
    )
    def tristeza_full(self, cf1, cf2, cf3):
        self._diagnose_full("ترايستيزا", cf1, cf2, cf3)

    @Rule(
        OR(
            AND(Symptom(name="اختناق النسيج الوعائي وموت الفروع", cf=MATCH.cf1),
                Symptom(name="تجعد أو تساقط الأوراق", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="اختناق النسيج الوعائي وموت الفروع", cf=MATCH.cf1),
                Symptom(name="ضعف في النمو، وقلة الإنتاجية", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="تجعد أو تساقط الأوراق", cf=MATCH.cf1),
                Symptom(name="ضعف في النمو، وقلة الإنتاجية", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
        )
    )
    def tristeza_partial(self, cf1, cf2):
        self._diagnose_partial("ترايستيزا", cf1, cf2)

    @Rule(
        OR(
            Symptom(name="اختناق النسيج الوعائي وموت الفروع", cf=MATCH.cf1),
            Symptom(name="تجعد أو تساقط الأوراق", cf=MATCH.cf1),
            Symptom(name="ضعف في النمو، وقلة الإنتاجية", cf=MATCH.cf1),
        ),
        TEST(lambda cf1: cf1 >= 60),
        salience=10,
    )
    def tristeza_weak(self, cf1):
        self._diagnose_weak("ترايستيزا", cf1, hint=HINT_SIMILAR_DISEASE)

    @Rule(Fact(disease="ترايستيزا"))
    def tristeza_treatment(self):
        self._treat(
            disease_name="مرض ترايستيزا الفيروسي - الحمضيات",
            cause="فيروس ترايستيزا (Citrus Tristeza Virus) - CTV.",
            steps=[
                "زراعة أصناف مقاومة للفيروس",
                "مكافحة حشرات المن ناقل الفيروس باستخدام مبيدات حشرية",
                "إزالة الأشجار المصابة فورًا ومنع انتشارها",
                "استخدام تطعيمات خالية من الفيروس عند الزراعة الجديدة",
                "تعقيم أدوات العمل بين الأشجار",
            ],
        )

    # ── التبقع الأسود ────────────────────────────────────────────────────────

    @Rule(
        Symptom(name="بقع داكنة غائرة على الثمار", cf=MATCH.cf1),
        Symptom(name="تساقط مبكر للثمار", cf=MATCH.cf2),
        Symptom(name="بقع صغيرة على الأوراق في بعض الحالات", cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60),
    )
    def black_spot_full(self, cf1, cf2, cf3):
        self._diagnose_full("التبقّع الأسود", cf1, cf2, cf3)

    @Rule(
        OR(
            AND(Symptom(name="بقع داكنة غائرة على الثمار", cf=MATCH.cf1),
                Symptom(name="تساقط مبكر للثمار", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="بقع داكنة غائرة على الثمار", cf=MATCH.cf1),
                Symptom(name="بقع صغيرة على الأوراق في بعض الحالات", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="تساقط مبكر للثمار", cf=MATCH.cf1),
                Symptom(name="بقع صغيرة على الأوراق في بعض الحالات", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
        )
    )
    def black_spot_partial(self, cf1, cf2):
        self._diagnose_partial("التبقّع الأسود", cf1, cf2)

    @Rule(
        OR(
            Symptom(name="بقع داكنة غائرة على الثمار", cf=MATCH.cf1),
            Symptom(name="تساقط مبكر للثمار", cf=MATCH.cf1),
            Symptom(name="بقع صغيرة على الأوراق في بعض الحالات", cf=MATCH.cf1),
        ),
        TEST(lambda cf1: cf1 >= 60),
    )
    def black_spot_weak(self, cf1):
        self._diagnose_weak("التبقّع الأسود", cf1)

    @Rule(Fact(disease="التبقّع الأسود"))
    def black_spot_treatment(self):
        self._treat(
            disease_name="مرض التبقّع الأسود - الحمضيات",
            cause=(
                "مرض التبقّع الأسود في الحمضيات يُسببه "
                "البكتيريا Xanthomonas citri subsp. citri."
            ),
            steps=[
                "رش الأشجار بمبيدات فطرية تحتوي على النحاس (مثل بوردو ميكس)",
                "تقليم الأفرع المصابة وإزالة الثمار الساقطة والتالفة",
                "تحسين التهوية بين الأشجار وتقليل الرطوبة",
                "مراقبة البؤر المرضية والحد من انتشارها",
                "زراعة أصناف مقاومة إن أمكن",
            ],
        )

    # ── الحصف البكتيري (عرضان فقط) ─────────────────────────────────────────

    @Rule(
        Symptom(name="تقرحات مائية على الأوراق والسيقان والثمار", cf=MATCH.cf1),
        Symptom(name="يحيط بها هالة صفراء", cf=MATCH.cf2),
        TEST(lambda cf1, cf2: min(cf1, cf2) >= 60),
    )
    def bacterial_canker_full(self, cf1, cf2):
        self._diagnose_full("الحصف البكتيري", cf1, cf2, multiplier=CF_MED_HIGH)

    @Rule(
        OR(
            Symptom(name="تقرحات مائية على الأوراق والسيقان والثمار", cf=MATCH.cf1),
            Symptom(name="يحيط بها هالة صفراء", cf=MATCH.cf1),
        ),
        TEST(lambda cf1: cf1 >= 60),
    )
    def bacterial_canker_weak(self, cf1):
        self._diagnose_weak("الحصف البكتيري", cf1, multiplier=CF_LOW)

    @Rule(Fact(disease="الحصف البكتيري"))
    def bacterial_canker_treatment(self):
        self._treat(
            disease_name="مرض الحصف البكتيري - الحمضيات",
            cause=(
                "مرض الحصف البكتيري في الحمضيات يُسببه "
                "البكتيريا Xanthomonas citri subsp. citri."
            ),
            steps=[
                "إزالة وتدمير الأجزاء المصابة بالمرض (حرق أو دفن عميق)",
                "رش الأشجار بمحلول نحاسي (مثل أوكسي كلوريد النحاس أو بوردو ميكس)",
                "تقليم الأشجار لتحسين التهوية وتقليل الرطوبة",
                "منع انتقال البكتيريا عبر المياه أو أدوات التقليم دون تعقيم",
                "زراعة أصناف مقاومة للمرض إن أمكن",
            ],
        )

    # ── البقعة الدهنية (عرضان فقط) ─────────────────────────────────────────

    @Rule(
        Symptom(name="بقع صفراء-بنية لامعة على السطح السفلي للأوراق", cf=MATCH.cf1),
        Symptom(name="تجعد أو تساقط الأوراق", cf=MATCH.cf2),
        TEST(lambda cf1, cf2: min(cf1, cf2) >= 60),
    )
    def greasy_spot_full(self, cf1, cf2):
        self._diagnose_full("البقعة الدهنية", cf1, cf2, multiplier=CF_MED_HIGH)

    @Rule(
        OR(
            Symptom(name="بقع صفراء-بنية لامعة على السطح السفلي للأوراق", cf=MATCH.cf1),
            Symptom(name="تجعد أو تساقط الأوراق", cf=MATCH.cf1),
        ),
        TEST(lambda cf1: cf1 >= 60),
        salience=5,
    )
    def greasy_spot_weak(self, cf1):
        self._diagnose_weak("البقعة الدهنية", cf1, multiplier=CF_LOW, hint=HINT_SIMILAR_DISEASE)

    @Rule(Fact(disease="البقعة الدهنية"))
    def greasy_spot_treatment(self):
        self._treat(
            disease_name="مرض البقعة الدهنية - الحمضيات",
            cause=(
                "مرض البقعة الدهنية في الحمضيات يُسببه "
                "الفطر Alternaria citri أو Alternaria alternata."
            ),
            steps=[
                "رش الأشجار بمبيد فطري نحاسي أو مبيد يحتوي على الكبريت",
                "تقليم الأوراق المصابة وإزالة بقايا الأوراق الساقطة من حول الشجرة",
                "تحسين التهوية بين الأشجار وتقليل الرطوبة",
                "تكرار الرش الوقائي خاصة في فترات الرطوبة العالية",
            ],
        )
