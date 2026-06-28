from experta import Rule, Fact, MATCH, TEST, OR, AND
from core import (
    Symptom, PlantDiagnosisEngine,
    CF_FULL, CF_PARTIAL, CF_WEAK, CF_MED_HIGH,
    HINT_MORE_SYMPTOMS, HINT_SIMILAR_DISEASE,
)

class TomatoRules(PlantDiagnosisEngine):

    SYMPTOMS = [
        "هالات صفراء حول البقع",
        "ذبول الأوراق السفلية",
        "بقع بنية مائية على حواف الأوراق",
        "تعفن بني على السيقان أو الثمار",
        "ظهور زغب رمادي أو أبيض تحت الأوراق",
        "ذبول مفاجئ دون اصفرار",
        "لا يظهر تعفن على الساق",
        "إفرازات مخاطية من قاعدة الساق",
        "بقع بنية مائية على الأوراق",
        "تشقق الجلد على الثمار",
        "تساقط الأوراق",
        "بقعة سوداء غائرة في أسفل الثمرة",
        "تصبح قاسية وجافة",
        "تبرقش في لون الأوراق (أخضر فاتح/غامق)",
        "تشوه شكل الأوراق",
        "صغر حجم الثمار",
    ]

    # ── اللفحة المبكرة ──────────────────────────────────────────────────────

    @Rule(
        Symptom(name="بقع بنية مائية على حواف الأوراق", cf=MATCH.cf1),
        Symptom(name="هالات صفراء حول البقع", cf=MATCH.cf2),
        Symptom(name="ذبول الأوراق السفلية", cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60),
    )
    def early_blight_full(self, cf1, cf2, cf3):
        self._diagnose_full("اللفحة المبكرة", cf1, cf2, cf3)

    @Rule(
        OR(
            AND(Symptom(name="بقع بنية مائية على حواف الأوراق", cf=MATCH.cf1),
                Symptom(name="هالات صفراء حول البقع", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="بقع بنية مائية على حواف الأوراق", cf=MATCH.cf1),
                Symptom(name="ذبول الأوراق السفلية", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="هالات صفراء حول البقع", cf=MATCH.cf1),
                Symptom(name="ذبول الأوراق السفلية", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
        )
    )
    def early_blight_partial(self, cf1, cf2):
        self._diagnose_partial("اللفحة المبكرة", cf1, cf2)

    @Rule(
        OR(
            Symptom(name="بقع بنية مائية على حواف الأوراق", cf=MATCH.cf1),
            Symptom(name="هالات صفراء حول البقع", cf=MATCH.cf1),
            Symptom(name="ذبول الأوراق السفلية", cf=MATCH.cf1),
        ),
        TEST(lambda cf1: cf1 >= 60),
        salience=5,
    )
    def early_blight_weak(self, cf1):
        self._diagnose_weak("اللفحة المبكرة", cf1, hint=HINT_SIMILAR_DISEASE)

    @Rule(Fact(disease="اللفحة المبكرة"))
    def early_blight_treatment(self):
        self._treat(
            disease_name="اللفحة المبكرة - الطماطم",
            cause="مرض اللفحة المبكرة في الطماطم يُسببه الفطر Alternaria solani.",
            steps=[
                "إزالة الأوراق المصابة وتحسين التهوية",
                "رش مبيدات فطرية تحتوي على Chlorothalonil أو Mancozeb",
                "تجنب الري فوق الأوراق",
            ],
        )

    # ── اللفحة المتأخرة ─────────────────────────────────────────────────────

    @Rule(
        Symptom(name="بقع بنية مائية على حواف الأوراق", cf=MATCH.cf1),
        Symptom(name="تعفن بني على السيقان أو الثمار", cf=MATCH.cf2),
        Symptom(name="ظهور زغب رمادي أو أبيض تحت الأوراق", cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60),
    )
    def late_blight_full(self, cf1, cf2, cf3):
        self._diagnose_full("اللفحة المتأخرة", cf1, cf2, cf3)

    @Rule(
        OR(
            AND(Symptom(name="بقع بنية مائية على حواف الأوراق", cf=MATCH.cf1),
                Symptom(name="تعفن بني على السيقان أو الثمار", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="بقع بنية مائية على حواف الأوراق", cf=MATCH.cf1),
                Symptom(name="ظهور زغب رمادي أو أبيض تحت الأوراق", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="تعفن بني على السيقان أو الثمار", cf=MATCH.cf1),
                Symptom(name="ظهور زغب رمادي أو أبيض تحت الأوراق", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
        )
    )
    def late_blight_partial(self, cf1, cf2):
        self._diagnose_partial("اللفحة المتأخرة", cf1, cf2)

    @Rule(
        OR(
            Symptom(name="بقع بنية مائية على حواف الأوراق", cf=MATCH.cf1),
            Symptom(name="تعفن بني على السيقان أو الثمار", cf=MATCH.cf1),
            Symptom(name="ظهور زغب رمادي أو أبيض تحت الأوراق", cf=MATCH.cf1),
        ),
        TEST(lambda cf1: cf1 >= 60),
        salience=10,
    )
    def late_blight_weak(self, cf1):
        self._diagnose_weak("اللفحة المتأخرة", cf1, hint=HINT_SIMILAR_DISEASE)

    @Rule(Fact(disease="اللفحة المتأخرة"))
    def late_blight_treatment(self):
        self._treat(
            disease_name="اللفحة المتأخرة - الطماطم",
            cause="مرض اللفحة المتأخرة في الطماطم يُسببه الفطر Phytophthora infestans.",
            steps=[
                "إزالة الأجزاء المصابة فورًا",
                "رش مبيد فطري مثل Mancozeb أو Chlorothalonil",
                "تكرار الرش كل 7 أيام في حال استمرار الظروف الرطبة",
                "تجنب ري الأوراق مباشرة وتحسين التهوية بين النباتات",
            ],
        )

    # ── الذبول البكتيري ─────────────────────────────────────────────────────

    @Rule(
        Symptom(name="ذبول مفاجئ دون اصفرار", cf=MATCH.cf1),
        Symptom(name="لا يظهر تعفن على الساق", cf=MATCH.cf2),
        Symptom(name="إفرازات مخاطية من قاعدة الساق", cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60),
    )
    def bacterial_wilt_full(self, cf1, cf2, cf3):
        self._diagnose_full("الذبول البكتيري", cf1, cf2, cf3)

    @Rule(
        OR(
            AND(Symptom(name="ذبول مفاجئ دون اصفرار", cf=MATCH.cf1),
                Symptom(name="لا يظهر تعفن على الساق", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="ذبول مفاجئ دون اصفرار", cf=MATCH.cf1),
                Symptom(name="إفرازات مخاطية من قاعدة الساق", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="لا يظهر تعفن على الساق", cf=MATCH.cf1),
                Symptom(name="إفرازات مخاطية من قاعدة الساق", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
        )
    )
    def bacterial_wilt_partial(self, cf1, cf2):
        self._diagnose_partial("الذبول البكتيري", cf1, cf2)

    @Rule(
        OR(
            Symptom(name="ذبول مفاجئ دون اصفرار", cf=MATCH.cf1),
            Symptom(name="لا يظهر تعفن على الساق", cf=MATCH.cf1),
            Symptom(name="إفرازات مخاطية من قاعدة الساق", cf=MATCH.cf1),
        ),
        TEST(lambda cf1: cf1 >= 60),
    )
    def bacterial_wilt_weak(self, cf1):
        self._diagnose_weak("الذبول البكتيري", cf1)

    @Rule(Fact(disease="الذبول البكتيري"))
    def bacterial_wilt_treatment(self):
        self._treat(
            disease_name="الذبول البكتيري - الطماطم",
            cause=(
                "مرض الذبول البكتيري في الطماطم يُسببه "
                "البكتيريا Ralstonia solanacearum."
            ),
            steps=[
                "إزالة النباتات المصابة فورًا لمنع الانتشار",
                "تعقيم التربة وتجنب الزراعة في نفس المكان",
                "زراعة أصناف مقاومة إن توفرت",
                "تجنب الجروح أثناء الزراعة وتقليل الري الزائد",
            ],
        )

    # ── تبقع الأوراق البكتيري ───────────────────────────────────────────────

    @Rule(
        Symptom(name="بقع بنية مائية على الأوراق", cf=MATCH.cf1),
        Symptom(name="تشقق الجلد على الثمار", cf=MATCH.cf2),
        Symptom(name="تساقط الأوراق", cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60),
    )
    def bacterial_spot_full(self, cf1, cf2, cf3):
        self._diagnose_full("تبقع الأوراق البكتيري", cf1, cf2, cf3)

    @Rule(
        OR(
            AND(Symptom(name="بقع بنية مائية على الأوراق", cf=MATCH.cf1),
                Symptom(name="تشقق الجلد على الثمار", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="بقع بنية مائية على الأوراق", cf=MATCH.cf1),
                Symptom(name="تساقط الأوراق", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="تشقق الجلد على الثمار", cf=MATCH.cf1),
                Symptom(name="تساقط الأوراق", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
        )
    )
    def bacterial_spot_partial(self, cf1, cf2):
        self._diagnose_partial("تبقع الأوراق البكتيري", cf1, cf2)

    @Rule(
        OR(
            Symptom(name="بقع بنية مائية على الأوراق", cf=MATCH.cf1),
            Symptom(name="تشقق الجلد على الثمار", cf=MATCH.cf1),
            Symptom(name="تساقط الأوراق", cf=MATCH.cf1),
        ),
        TEST(lambda cf1: cf1 >= 60),
    )
    def bacterial_spot_weak(self, cf1):
        self._diagnose_weak("تبقع الأوراق البكتيري", cf1)

    @Rule(Fact(disease="تبقع الأوراق البكتيري"))
    def bacterial_spot_treatment(self):
        self._treat(
            disease_name="تبقع الأوراق البكتيري - الطماطم",
            cause=(
                "مرض تبقّع الأوراق البكتيري في الطماطم يُسببه "
                "البكتيريا Xanthomonas vesicatoria."
            ),
            steps=[
                "إزالة الأوراق المصابة فورًا لمنع الانتشار",
                "استخدام مبيدات نحاسية (Copper-based sprays) كل 7 أيام",
                "تجنب رش المياه على الأوراق",
                "زراعة أصناف مقاومة إن أمكن",
            ],
        )

    # ── عفن الطرف الزهري ────────────────────────────────────────────────────

    @Rule(
        Symptom(name="بقعة سوداء غائرة في أسفل الثمرة", cf=MATCH.cf1),
        Symptom(name="تصبح قاسية وجافة", cf=MATCH.cf2),
        TEST(lambda cf1, cf2: min(cf1, cf2) >= 60),
    )
    def blossom_end_rot_full(self, cf1, cf2):
        self._diagnose_full("عفن الطرف الزهري", cf1, cf2, multiplier=CF_MED_HIGH)

    @Rule(
        OR(
            Symptom(name="بقعة سوداء غائرة في أسفل الثمرة", cf=MATCH.cf1),
            Symptom(name="تصبح قاسية وجافة", cf=MATCH.cf1),
        ),
        TEST(lambda cf1: cf1 >= 60),
    )
    def blossom_end_rot_weak(self, cf1):
        self._diagnose_weak(
            "عفن الطرف الزهري", cf1,
            hint="يُفضل إدخال العرض الثاني لتأكيد التشخيص.",
        )

    @Rule(Fact(disease="عفن الطرف الزهري"))
    def blossom_end_rot_treatment(self):
        self._treat(
            disease_name="عفن الطرف الزهري - الطماطم",
            cause=(
                "عفن الطرف الزهري اضطراب فسيولوجي ناتج عن "
                "نقص الكالسيوم في الثمار خلال مرحلة النمو، وليس مرضاً فطرياً أو بكتيرياً."
            ),
            steps=[
                "إضافة مصدر كالسيوم إلى التربة (مثل نترات الكالسيوم)",
                "الحفاظ على رطوبة منتظمة في التربة (تجنب الجفاف المفاجئ)",
                "تجنب التسميد الزائد بالنيتروجين",
                "رش ورقي بكالسيوم في حال النقص الحاد",
            ],
        )

    # ── موزاييك الطماطم ─────────────────────────────────────────────────────

    @Rule(
        Symptom(name="تبرقش في لون الأوراق (أخضر فاتح/غامق)", cf=MATCH.cf1),
        Symptom(name="تشوه شكل الأوراق", cf=MATCH.cf2),
        Symptom(name="صغر حجم الثمار", cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60),
    )
    def tomato_mosaic_full(self, cf1, cf2, cf3):
        self._diagnose_full("موزاييك الطماطم", cf1, cf2, cf3)

    @Rule(
        OR(
            AND(Symptom(name="تبرقش في لون الأوراق (أخضر فاتح/غامق)", cf=MATCH.cf1),
                Symptom(name="تشوه شكل الأوراق", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="تبرقش في لون الأوراق (أخضر فاتح/غامق)", cf=MATCH.cf1),
                Symptom(name="صغر حجم الثمار", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name="تشوه شكل الأوراق", cf=MATCH.cf1),
                Symptom(name="صغر حجم الثمار", cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
        )
    )
    def tomato_mosaic_partial(self, cf1, cf2):
        self._diagnose_partial("موزاييك الطماطم", cf1, cf2)

    @Rule(
        OR(
            Symptom(name="تبرقش في لون الأوراق (أخضر فاتح/غامق)", cf=MATCH.cf1),
            Symptom(name="تشوه شكل الأوراق", cf=MATCH.cf1),
            Symptom(name="صغر حجم الثمار", cf=MATCH.cf1),
        ),
        TEST(lambda cf1: cf1 >= 60),
    )
    def tomato_mosaic_weak(self, cf1):
        self._diagnose_weak("موزاييك الطماطم", cf1)

    @Rule(Fact(disease="موزاييك الطماطم"))
    def tomato_mosaic_treatment(self):
        self._treat(
            disease_name="موزاييك الطماطم - ToMV",
            cause="فيروس موزاييك الطماطم (Tomato Mosaic Virus) - ToMV.",
            steps=[
                "لا يوجد علاج مباشر، يُنصح بإزالة النباتات المصابة",
                "استخدام بذور مقاومة للفيروس عند الزراعة",
                "تعقيم الأدوات وتجنب ملامسة النباتات بأيدي ملوثة",
                "مكافحة الحشرات الناقلة مثل المنّ",
            ],
        )
