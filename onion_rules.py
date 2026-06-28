from experta import Rule, Fact, MATCH, TEST, OR, AND
from core import (
    Symptom, PlantDiagnosisEngine,
    CF_FULL, CF_PARTIAL, CF_WEAK,
    HINT_MORE_SYMPTOMS, HINT_SIMILAR_DISEASE,
)

class OnionRules(PlantDiagnosisEngine):

    SYMPTOMS = [
        "بقع صفراء باهتة أو بنية طويلة على الأوراق الخارجية قد تتحول إلى نمو رمادي-بنفسجي تحت الرطوبة",
        "ذبول الأوراق المصابة وانحناؤها أو تساقطها",
        "البصليات تصبح طرية ومائية بسبب المرض",
        "بقعة مائية صغيرة تتحول إلى بقعة داكنة ذات هالة صفراء",
        "تظهر بقعة هدف بنية-أرجوانية على الأوراق",
        "انتشار البقع وقت المطر أو الرذاذ",
        "طرى ورخاوة في قاعدة رقبة البصلة (الياقة)",
        "ظهور نمو فطري رمادي أو زغب أسود على الياقة أو بين القشور",
        "تعفن البصلة من الأعلى باتجاه الداخل أثناء التخزين",
        "جذور مصابة تصبح وردية أولاً، ثم تتحول إلى حمراء أو أرجوانية",
        "الجذور تصبح مائية وقابلة للتفتت",
        "ضعف نمو النبات وجفافه حتى قبل إنضاج البصلية",
        "تضخم في الجذوع السفلية وتعفن جزئي",
        "أوراق ملتفة، صفراء وسريعة الذبول",
        "البصليات مشوهة أو ناعمة، غير قابلة للبيع",
    ]

    # ── البياض الزغبي ───────────────────────────────────────────────────────
    @Rule(
        Symptom(
            name="بقع صفراء باهتة أو بنية طويلة على الأوراق الخارجية قد تتحول إلى نمو رمادي-بنفسجي تحت الرطوبة",
            cf=MATCH.cf1,
        ),
        Symptom(name="ذبول الأوراق المصابة وانحناؤها أو تساقطها", cf=MATCH.cf2),
        Symptom(name="البصليات تصبح طرية ومائية بسبب المرض", cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60),
    )
    def downy_mildew_full(self, cf1, cf2, cf3):
        self._diagnose_full("البياض الزغبي", cf1, cf2, cf3)

    @Rule(
        OR(
            AND(Symptom(name="بقع صفراء باهتة أو بنية طويلة على الأوراق الخارجية قد تتحول إلى نمو رمادي-بنفسجي تحت الرطوبة", cf=MATCH.cf1),
                Symptom(name="ذبول الأوراق المصابة وانحناؤها أو تساقطها", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="بقع صفراء باهتة أو بنية طويلة على الأوراق الخارجية قد تتحول إلى نمو رمادي-بنفسجي تحت الرطوبة", cf=MATCH.cf1),
                Symptom(name="البصليات تصبح طرية ومائية بسبب المرض", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="ذبول الأوراق المصابة وانحناؤها أو تساقطها", cf=MATCH.cf1),
                Symptom(name="البصليات تصبح طرية ومائية بسبب المرض", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
        )
    )
    def downy_mildew_partial(self, cf1, cf2):
        self._diagnose_partial("البياض الزغبي", cf1, cf2)

    @Rule(
        OR(
            Symptom(name="بقع صفراء باهتة أو بنية طويلة على الأوراق الخارجية قد تتحول إلى نمو رمادي-بنفسجي تحت الرطوبة", cf=MATCH.cf1),
            Symptom(name="ذبول الأوراق المصابة وانحناؤها أو تساقطها", cf=MATCH.cf1),
            Symptom(name="البصليات تصبح طرية ومائية بسبب المرض", cf=MATCH.cf1),
        ),
        TEST(lambda cf1: cf1 >= 60),
    )
    def downy_mildew_weak(self, cf1):
        self._diagnose_weak("البياض الزغبي", cf1)

    @Rule(Fact(disease="البياض الزغبي"))
    def downy_mildew_treatment(self):
        self._treat(
            disease_name="البياض الزغبي - البصل",
            cause="مرض البياض الزغبي في البصل يُسببه الفطر Peronospora destructor.",
            steps=[
                "رش مبيدات فطرية تحتوي على Metalaxyl أو Mancozeb",
                "تكرار الرش كل 7–10 أيام حسب الظروف الجوية",
                "تحسين التهوية والتخلص من الأجزاء المصابة",
                "تجنب الري بالرش لتقليل الرطوبة على الأوراق",
            ],
        )

    # ── البقعة الأرجوانية ────────────────────────────────────────────────────

    @Rule(
        Symptom(name="بقعة مائية صغيرة تتحول إلى بقعة داكنة ذات هالة صفراء", cf=MATCH.cf1),
        Symptom(name="تظهر بقعة هدف بنية-أرجوانية على الأوراق", cf=MATCH.cf2),
        Symptom(name="انتشار البقع وقت المطر أو الرذاذ", cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60),
    )
    def purple_blotch_full(self, cf1, cf2, cf3):
        self._diagnose_full("البقعة الأرجوانية", cf1, cf2, cf3)

    @Rule(
        OR(
            AND(Symptom(name="بقعة مائية صغيرة تتحول إلى بقعة داكنة ذات هالة صفراء", cf=MATCH.cf1),
                Symptom(name="تظهر بقعة هدف بنية-أرجوانية على الأوراق", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="بقعة مائية صغيرة تتحول إلى بقعة داكنة ذات هالة صفراء", cf=MATCH.cf1),
                Symptom(name="انتشار البقع وقت المطر أو الرذاذ", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="تظهر بقعة هدف بنية-أرجوانية على الأوراق", cf=MATCH.cf1),
                Symptom(name="انتشار البقع وقت المطر أو الرذاذ", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
        )
    )
    def purple_blotch_partial(self, cf1, cf2):
        self._diagnose_partial("البقعة الأرجوانية", cf1, cf2)

    @Rule(
        OR(
            Symptom(name="بقعة مائية صغيرة تتحول إلى بقعة داكنة ذات هالة صفراء", cf=MATCH.cf1),
            Symptom(name="تظهر بقعة هدف بنية-أرجوانية على الأوراق", cf=MATCH.cf1),
            Symptom(name="انتشار البقع وقت المطر أو الرذاذ", cf=MATCH.cf1),
        ),
        TEST(lambda cf1: cf1 >= 60),
    )
    def purple_blotch_weak(self, cf1):
        self._diagnose_weak("البقعة الأرجوانية", cf1)

    @Rule(Fact(disease="البقعة الأرجوانية"))
    def purple_blotch_treatment(self):
        self._treat(
            disease_name="البقعة الأرجوانية - البصل",
            cause="مرض البقعة الأرجوانية في البصل يُسببه الفطر Alternaria porri.",
            steps=[
                "رش مبيدات فطرية تحتوي على Iprodione أو Chlorothalonil",
                "تكرار الرش كل 7–14 يوم خلال موسم النمو",
                "تجنب الري المفرط وتحسين التصريف",
                "إزالة بقايا النباتات المصابة بعد الحصاد",
            ],
        )

    # ── عفن رقبة البصل (Botrytis) ───────────────────────────────────────────

    @Rule(
        Symptom(name="طرى ورخاوة في قاعدة رقبة البصلة (الياقة)", cf=MATCH.cf1),
        Symptom(name="ظهور نمو فطري رمادي أو زغب أسود على الياقة أو بين القشور", cf=MATCH.cf2),
        Symptom(name="تعفن البصلة من الأعلى باتجاه الداخل أثناء التخزين", cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60),
    )
    def neck_rot_full(self, cf1, cf2, cf3):
        self._diagnose_full("عفن رقبة البصل", cf1, cf2, cf3)

    @Rule(
        OR(
            AND(Symptom(name="طرى ورخاوة في قاعدة رقبة البصلة (الياقة)", cf=MATCH.cf1),
                Symptom(name="ظهور نمو فطري رمادي أو زغب أسود على الياقة أو بين القشور", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="طرى ورخاوة في قاعدة رقبة البصلة (الياقة)", cf=MATCH.cf1),
                Symptom(name="تعفن البصلة من الأعلى باتجاه الداخل أثناء التخزين", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="ظهور نمو فطري رمادي أو زغب أسود على الياقة أو بين القشور", cf=MATCH.cf1),
                Symptom(name="تعفن البصلة من الأعلى باتجاه الداخل أثناء التخزين", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
        )
    )
    def neck_rot_partial(self, cf1, cf2):
        self._diagnose_partial("عفن رقبة البصل", cf1, cf2)

    @Rule(
        OR(
            Symptom(name="طرى ورخاوة في قاعدة رقبة البصلة (الياقة)", cf=MATCH.cf1),
            Symptom(name="ظهور نمو فطري رمادي أو زغب أسود على الياقة أو بين القشور", cf=MATCH.cf1),
            Symptom(name="تعفن البصلة من الأعلى باتجاه الداخل أثناء التخزين", cf=MATCH.cf1),
        ),
        TEST(lambda cf1: cf1 >= 60),
    )
    def neck_rot_weak(self, cf1):
        self._diagnose_weak("عفن رقبة البصل", cf1)

    @Rule(Fact(disease="عفن رقبة البصل"))
    def neck_rot_treatment(self):
        self._treat(
            disease_name="عفن رقبة البصل - Botrytis",
            cause="مرض عفن رقبة البصل يُسببه الفطر Botrytis allii.",
            steps=[
                "تجفيف البصل جيداً قبل التخزين (التقليد أو الذبول المتعمد)",
                "تخزين البصل في مكان جاف وجيد التهوية",
                "رش مبيدات فطرية قبل الحصاد بـ2–3 أسابيع",
                "استخدام بذور أو شتلات خالية من الإصابة",
            ],
        )

    # ── عفن الجذور الوردي ───────────────────────────────────────────────────

    @Rule(
        Symptom(name="جذور مصابة تصبح وردية أولاً، ثم تتحول إلى حمراء أو أرجوانية", cf=MATCH.cf1),
        Symptom(name="الجذور تصبح مائية وقابلة للتفتت", cf=MATCH.cf2),
        Symptom(name="ضعف نمو النبات وجفافه حتى قبل إنضاج البصلية", cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60),
    )
    def pink_root_rot_full(self, cf1, cf2, cf3):
        self._diagnose_full("عفن الجذور الوردي", cf1, cf2, cf3)

    @Rule(
        OR(
            AND(Symptom(name="جذور مصابة تصبح وردية أولاً، ثم تتحول إلى حمراء أو أرجوانية", cf=MATCH.cf1),
                Symptom(name="الجذور تصبح مائية وقابلة للتفتت", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="جذور مصابة تصبح وردية أولاً، ثم تتحول إلى حمراء أو أرجوانية", cf=MATCH.cf1),
                Symptom(name="ضعف نمو النبات وجفافه حتى قبل إنضاج البصلية", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="الجذور تصبح مائية وقابلة للتفتت", cf=MATCH.cf1),
                Symptom(name="ضعف نمو النبات وجفافه حتى قبل إنضاج البصلية", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
        )
    )
    def pink_root_rot_partial(self, cf1, cf2):
        self._diagnose_partial("عفن الجذور الوردي", cf1, cf2)

    @Rule(
        OR(
            Symptom(name="جذور مصابة تصبح وردية أولاً، ثم تتحول إلى حمراء أو أرجوانية", cf=MATCH.cf1),
            Symptom(name="الجذور تصبح مائية وقابلة للتفتت", cf=MATCH.cf1),
            Symptom(name="ضعف نمو النبات وجفافه حتى قبل إنضاج البصلية", cf=MATCH.cf1),
        ),
        TEST(lambda cf1: cf1 >= 60),
    )
    def pink_root_rot_weak(self, cf1):
        self._diagnose_weak("عفن الجذور الوردي", cf1)

    @Rule(Fact(disease="عفن الجذور الوردي"))
    def pink_root_rot_treatment(self):
        self._treat(
            disease_name="عفن الجذور الوردي - البصل",
            cause="مرض عفن الجذور الوردي في البصل يُسببه الفطر Pyrenochaeta terrestris.",
            steps=[
                "تدوير المحاصيل لتجنب تراكم الفطر في التربة",
                "زراعة أصناف مقاومة إن توفرت",
                "تحسين تصريف التربة وتجنب الري الزائد",
                "معالجة التربة بمبيدات فطرية مناسبة قبل الزراعة",
            ],
        )

    # ── النيماتودا الجذعية ───────────────────────────────────────────────────

    @Rule(
        Symptom(name="تضخم في الجذوع السفلية وتعفن جزئي", cf=MATCH.cf1),
        Symptom(name="أوراق ملتفة، صفراء وسريعة الذبول", cf=MATCH.cf2),
        Symptom(name="البصليات مشوهة أو ناعمة، غير قابلة للبيع", cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60),
    )
    def stem_nematode_full(self, cf1, cf2, cf3):
        self._diagnose_full("النيماتودا الجذعية", cf1, cf2, cf3)

    @Rule(
        OR(
            AND(Symptom(name="تضخم في الجذوع السفلية وتعفن جزئي", cf=MATCH.cf1),
                Symptom(name="أوراق ملتفة، صفراء وسريعة الذبول", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="تضخم في الجذوع السفلية وتعفن جزئي", cf=MATCH.cf1),
                Symptom(name="البصليات مشوهة أو ناعمة، غير قابلة للبيع", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="أوراق ملتفة، صفراء وسريعة الذبول", cf=MATCH.cf1),
                Symptom(name="البصليات مشوهة أو ناعمة، غير قابلة للبيع", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
        )
    )
    def stem_nematode_partial(self, cf1, cf2):
        self._diagnose_partial("النيماتودا الجذعية", cf1, cf2)

    @Rule(
        OR(
            Symptom(name="تضخم في الجذوع السفلية وتعفن جزئي", cf=MATCH.cf1),
            Symptom(name="أوراق ملتفة، صفراء وسريعة الذبول", cf=MATCH.cf1),
            Symptom(name="البصليات مشوهة أو ناعمة، غير قابلة للبيع", cf=MATCH.cf1),
        ),
        TEST(lambda cf1: cf1 >= 60),
    )
    def stem_nematode_weak(self, cf1):
        self._diagnose_weak("النيماتودا الجذعية", cf1)

    @Rule(Fact(disease="النيماتودا الجذعية"))
    def stem_nematode_treatment(self):
        self._treat(
            disease_name="النيماتودا الجذعية - البصل",
            cause="النيماتودا الجذعية في البصل تُسببها الديدان الخيطية Ditylenchus dipsaci.",
            steps=[
                "استخدام بذور معالجة بالحرارة أو مبيدات النيماتودا",
                "تدوير المحاصيل لمدة 4 سنوات على الأقل",
                "تجنب الري الزائد وتحسين تصريف التربة",
                "معالجة التربة بمبيدات النيماتودا الكيميائية أو البيولوجية",
                "تعقيم أدوات العمل لمنع انتشار النيماتودا",
            ],
        )