from experta import Rule, Fact, MATCH, TEST, OR, AND
from core import (
    Symptom, PlantDiagnosisEngine,
    CF_FULL, CF_PARTIAL, CF_WEAK,
    HINT_MORE_SYMPTOMS,
)

class GarlicRules(PlantDiagnosisEngine):

    SYMPTOMS = [
        "اصفرار الأوراق من الأطراف نحو القاعدة",
        "ظهور نمو رمادي مزرق على السطح السفلي للأوراق",
        "تدهور مبكر للنباتات وسقوط الأوراق",
        "رقّة قاعدة الساق (العنق) وتلونها بلون بني رمادي",
        "ظهور زغب رمادي على العنق أثناء التخزين",
        "تفكك أنسجة العنق وتعفن البصلة من الأعلى",
        "بقع مائية على البصلة تبدأ من الجروح",
        "نمو فطري أزرق مخضر على سطح البصلة",
        "رائحة عفن نفاذة عند شق البصلة",
        "اصفرار الأوراق وذبول مفاجئ للنبات",
        "نمو أبيض قطني كثيف على قاعدة النبات",
        "ظهور أجسام سوداء صغيرة (سكليروشيا) في التربة حول الجذور",
        "تبرقش أصفر أو أخضر فاتح على الأوراق الطرية",
        "تقزم النبات وضعف في تكوين الأبصال",
        "تشوه في شكل الأوراق وتأخر في النمو",
    ]

    # ── البياض الزغبي ───────────────────────────────────────────────────────

    @Rule(
        Symptom(name="اصفرار الأوراق من الأطراف نحو القاعدة", cf=MATCH.cf1),
        Symptom(name="ظهور نمو رمادي مزرق على السطح السفلي للأوراق", cf=MATCH.cf2),
        Symptom(name="تدهور مبكر للنباتات وسقوط الأوراق", cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60),
    )
    def downy_mildew_full(self, cf1, cf2, cf3):
        self._diagnose_full("البياض الزغبي", cf1, cf2, cf3)

    @Rule(
        OR(
            AND(Symptom(name="اصفرار الأوراق من الأطراف نحو القاعدة", cf=MATCH.cf1),
                Symptom(name="ظهور نمو رمادي مزرق على السطح السفلي للأوراق", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="اصفرار الأوراق من الأطراف نحو القاعدة", cf=MATCH.cf1),
                Symptom(name="تدهور مبكر للنباتات وسقوط الأوراق", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="ظهور نمو رمادي مزرق على السطح السفلي للأوراق", cf=MATCH.cf1),
                Symptom(name="تدهور مبكر للنباتات وسقوط الأوراق", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
        )
    )
    def downy_mildew_partial(self, cf1, cf2):
        self._diagnose_partial("البياض الزغبي", cf1, cf2)

    @Rule(
        OR(
            Symptom(name="اصفرار الأوراق من الأطراف نحو القاعدة", cf=MATCH.cf1),
            Symptom(name="ظهور نمو رمادي مزرق على السطح السفلي للأوراق", cf=MATCH.cf1),
            Symptom(name="تدهور مبكر للنباتات وسقوط الأوراق", cf=MATCH.cf1),
        ),
        TEST(lambda cf1: cf1 >= 60),
    )
    def downy_mildew_weak(self, cf1):
        self._diagnose_weak("البياض الزغبي", cf1)

    @Rule(Fact(disease="البياض الزغبي"))
    def downy_mildew_treatment(self):
        self._treat(
            disease_name="البياض الزغبي - الثوم",
            cause="مرض البياض الزغبي في الثوم يُسببه الفطر Peronospora destructor.",
            steps=[
                "رش مبيدات فطرية تحتوي على Metalaxyl أو Mancozeb",
                "تكرار الرش كل 7–10 أيام حسب الظروف الجوية",
                "تحسين التهوية والتخلص من الأجزاء المصابة",
                "تجنب الري بالرش لتقليل الرطوبة على الأوراق",
            ],
        )

    # ── عفن رقبة الثوم الرمادي ──────────────────────────────────────────────

    @Rule(
        Symptom(name="رقّة قاعدة الساق (العنق) وتلونها بلون بني رمادي", cf=MATCH.cf1),
        Symptom(name="ظهور زغب رمادي على العنق أثناء التخزين", cf=MATCH.cf2),
        Symptom(name="تفكك أنسجة العنق وتعفن البصلة من الأعلى", cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60),
    )
    def gray_neck_rot_full(self, cf1, cf2, cf3):
        self._diagnose_full("عفن رقبة الثوم الرمادي", cf1, cf2, cf3)

    @Rule(
        OR(
            AND(Symptom(name="رقّة قاعدة الساق (العنق) وتلونها بلون بني رمادي", cf=MATCH.cf1),
                Symptom(name="ظهور زغب رمادي على العنق أثناء التخزين", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="رقّة قاعدة الساق (العنق) وتلونها بلون بني رمادي", cf=MATCH.cf1),
                Symptom(name="تفكك أنسجة العنق وتعفن البصلة من الأعلى", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="ظهور زغب رمادي على العنق أثناء التخزين", cf=MATCH.cf1),
                Symptom(name="تفكك أنسجة العنق وتعفن البصلة من الأعلى", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
        )
    )
    def gray_neck_rot_partial(self, cf1, cf2):
        self._diagnose_partial("عفن رقبة الثوم الرمادي", cf1, cf2)

    @Rule(
        OR(
            Symptom(name="رقّة قاعدة الساق (العنق) وتلونها بلون بني رمادي", cf=MATCH.cf1),
            Symptom(name="ظهور زغب رمادي على العنق أثناء التخزين", cf=MATCH.cf1),
            Symptom(name="تفكك أنسجة العنق وتعفن البصلة من الأعلى", cf=MATCH.cf1),
        ),
        TEST(lambda cf1: cf1 >= 60),
    )
    def gray_neck_rot_weak(self, cf1):
        self._diagnose_weak("عفن رقبة الثوم الرمادي", cf1)

    @Rule(Fact(disease="عفن رقبة الثوم الرمادي"))
    def gray_neck_rot_treatment(self):
        self._treat(
            disease_name="عفن رقبة الثوم الرمادي",
            cause="مرض عفن رقبة الثوم الرمادي يُسببه الفطر Botrytis allii.",
            steps=[
                "تجفيف الثوم جيداً بعد الحصاد قبل التخزين",
                "تخزين الثوم في مكان بارد وجيد التهوية",
                "رش مبيدات فطرية (مثل Iprodione) قبل الحصاد بأسبوعين",
                "تجنب الجروح عند الحصاد لتقليل مداخل العدوى",
            ],
        )

    # ── العفن الأزرق ────────────────────────────────────────────────────────

    @Rule(
        Symptom(name="بقع مائية على البصلة تبدأ من الجروح", cf=MATCH.cf1),
        Symptom(name="نمو فطري أزرق مخضر على سطح البصلة", cf=MATCH.cf2),
        Symptom(name="رائحة عفن نفاذة عند شق البصلة", cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60),
    )
    def blue_mold_full(self, cf1, cf2, cf3):
        self._diagnose_full("العفن الأزرق", cf1, cf2, cf3)

    @Rule(
        OR(
            AND(Symptom(name="بقع مائية على البصلة تبدأ من الجروح", cf=MATCH.cf1),
                Symptom(name="نمو فطري أزرق مخضر على سطح البصلة", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="بقع مائية على البصلة تبدأ من الجروح", cf=MATCH.cf1),
                Symptom(name="رائحة عفن نفاذة عند شق البصلة", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="نمو فطري أزرق مخضر على سطح البصلة", cf=MATCH.cf1),
                Symptom(name="رائحة عفن نفاذة عند شق البصلة", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
        )
    )
    def blue_mold_partial(self, cf1, cf2):
        self._diagnose_partial("العفن الأزرق", cf1, cf2)

    @Rule(
        OR(
            Symptom(name="بقع مائية على البصلة تبدأ من الجروح", cf=MATCH.cf1),
            Symptom(name="نمو فطري أزرق مخضر على سطح البصلة", cf=MATCH.cf1),
            Symptom(name="رائحة عفن نفاذة عند شق البصلة", cf=MATCH.cf1),
        ),
        TEST(lambda cf1: cf1 >= 60),
    )
    def blue_mold_weak(self, cf1):
        self._diagnose_weak("العفن الأزرق", cf1)

    @Rule(Fact(disease="العفن الأزرق"))
    def blue_mold_treatment(self):
        self._treat(
            disease_name="العفن الأزرق - الثوم",
            cause="مرض العفن الأزرق في الثوم يُسببه الفطر Penicillium hirsutum.",
            steps=[
                "تجنب الجروح أثناء الحصاد والتخزين",
                "تخزين الثوم في درجات حرارة منخفضة (0–4 درجة مئوية) ورطوبة نسبية منخفضة",
                "رش الثوم بمبيد فطري مثل Thiabendazole قبل التخزين",
                "فرز الثوم جيداً وإزالة أي فص مصاب قبل التخزين",
            ],
        )

    # ── العفن الأبيض ────────────────────────────────────────────────────────

    @Rule(
        Symptom(name="اصفرار الأوراق وذبول مفاجئ للنبات", cf=MATCH.cf1),
        Symptom(name="نمو أبيض قطني كثيف على قاعدة النبات", cf=MATCH.cf2),
        Symptom(name="ظهور أجسام سوداء صغيرة (سكليروشيا) في التربة حول الجذور", cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60),
    )
    def white_rot_full(self, cf1, cf2, cf3):
        self._diagnose_full("العفن الأبيض", cf1, cf2, cf3)

    @Rule(
        OR(
            AND(Symptom(name="اصفرار الأوراق وذبول مفاجئ للنبات", cf=MATCH.cf1),
                Symptom(name="نمو أبيض قطني كثيف على قاعدة النبات", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="اصفرار الأوراق وذبول مفاجئ للنبات", cf=MATCH.cf1),
                Symptom(name="ظهور أجسام سوداء صغيرة (سكليروشيا) في التربة حول الجذور", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="نمو أبيض قطني كثيف على قاعدة النبات", cf=MATCH.cf1),
                Symptom(name="ظهور أجسام سوداء صغيرة (سكليروشيا) في التربة حول الجذور", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
        )
    )
    def white_rot_partial(self, cf1, cf2):
        self._diagnose_partial("العفن الأبيض", cf1, cf2)

    @Rule(
        OR(
            Symptom(name="اصفرار الأوراق وذبول مفاجئ للنبات", cf=MATCH.cf1),
            Symptom(name="نمو أبيض قطني كثيف على قاعدة النبات", cf=MATCH.cf1),
            Symptom(name="ظهور أجسام سوداء صغيرة (سكليروشيا) في التربة حول الجذور", cf=MATCH.cf1),
        ),
        TEST(lambda cf1: cf1 >= 60),
    )
    def white_rot_weak(self, cf1):
        self._diagnose_weak("العفن الأبيض", cf1)

    @Rule(Fact(disease="العفن الأبيض"))
    def white_rot_treatment(self):
        self._treat(
            disease_name="العفن الأبيض - الثوم",
            cause="مرض العفن الأبيض في الثوم يُسببه الفطر Sclerotium cepivorum.",
            steps=[
                "تدوير المحاصيل لمدة 5–8 سنوات في التربة المصابة",
                "معالجة التربة بمبيدات فطرية مثل Tebuconazole أو Iprodione",
                "إزالة وإتلاف النباتات المصابة فورًا (حرق أو دفن عميق)",
                "تجنب نقل التربة الملوثة إلى مناطق سليمة",
                "زراعة أصناف مقاومة إن توفرت",
            ],
        )

    # ── المركّب الفيروسي ─────────────────────────────────────────────────────

    @Rule(
        Symptom(name="تبرقش أصفر أو أخضر فاتح على الأوراق الطرية", cf=MATCH.cf1),
        Symptom(name="تقزم النبات وضعف في تكوين الأبصال", cf=MATCH.cf2),
        Symptom(name="تشوه في شكل الأوراق وتأخر في النمو", cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60),
    )
    def viral_complex_full(self, cf1, cf2, cf3):
        self._diagnose_full("المركّب الفيروسي", cf1, cf2, cf3)

    @Rule(
        OR(
            AND(Symptom(name="تبرقش أصفر أو أخضر فاتح على الأوراق الطرية", cf=MATCH.cf1),
                Symptom(name="تقزم النبات وضعف في تكوين الأبصال", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="تبرقش أصفر أو أخضر فاتح على الأوراق الطرية", cf=MATCH.cf1),
                Symptom(name="تشوه في شكل الأوراق وتأخر في النمو", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="تقزم النبات وضعف في تكوين الأبصال", cf=MATCH.cf1),
                Symptom(name="تشوه في شكل الأوراق وتأخر في النمو", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
        )
    )
    def viral_complex_partial(self, cf1, cf2):
        self._diagnose_partial("المركّب الفيروسي", cf1, cf2)

    @Rule(
        OR(
            Symptom(name="تبرقش أصفر أو أخضر فاتح على الأوراق الطرية", cf=MATCH.cf1),
            Symptom(name="تقزم النبات وضعف في تكوين الأبصال", cf=MATCH.cf1),
            Symptom(name="تشوه في شكل الأوراق وتأخر في النمو", cf=MATCH.cf1),
        ),
        TEST(lambda cf1: cf1 >= 60),
    )
    def viral_complex_weak(self, cf1):
        self._diagnose_weak("المركّب الفيروسي", cf1)

    @Rule(Fact(disease="المركّب الفيروسي"))
    def viral_complex_treatment(self):
        self._treat(
            disease_name="المركّب الفيروسي - الثوم",
            cause=(
                "المركّب الفيروسي في الثوم يُسببه مجموعة من الفيروسات "
                "أبرزها OYDV و LYSV."
            ),
            steps=[
                "استخدام فصوص ثوم خالية من الفيروسات (معتمدة مخبرياً)",
                "مكافحة حشرات المن الناقلة للفيروسات باستخدام مبيدات حشرية",
                "إزالة النباتات المصابة فورًا لمنع انتشار الفيروس",
                "تجنب إعادة استخدام الفصوص من محاصيل مصابة كبذار",
            ],
        )
