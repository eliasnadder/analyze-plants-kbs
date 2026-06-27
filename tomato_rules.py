from experta import Rule, Fact, MATCH, TEST, OR, AND
from core import Symptom, PlantDiagnosisEngine

class TomatoRules(PlantDiagnosisEngine):

    # اللفحة المبكرة
    @Rule(
        Symptom(name='بقع بنية مائية على حواف الأوراق', cf=MATCH.cf1),
        Symptom(name='هالات صفراء حول البقع', cf=MATCH.cf2),
        Symptom(name='ذبول الأوراق السفلية', cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60)
    ,
        salience=30
    )
    def early_blight_full(self, cf1, cf2, cf3):
        final = round(min(cf1, cf2, cf3) * 0.85)
        print(f"\n✅ التشخيص: اللفحة المبكرة (الطماطم) (درجة الثقة: {final}/100)")
        self.declare(Fact(disease="اللفحة المبكرة"))

    @Rule(
        OR(
            AND(Symptom(name='بقع بنية مائية على حواف الأوراق', cf=MATCH.cf1),
                Symptom(name='هالات صفراء حول البقع', cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name='بقع بنية مائية على حواف الأوراق', cf=MATCH.cf1),
                Symptom(name='ذبول الأوراق السفلية', cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name='هالات صفراء حول البقع', cf=MATCH.cf1),
                Symptom(name='ذبول الأوراق السفلية', cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
        )
    ,
        salience=20
    )
    def early_blight_partial(self, cf1=0, cf2=0):
        final = round(min(cf1, cf2) * 0.65)
        print(f"\n⚠️ تشخيص مبدئي: اللفحة المبكرة (الطماطم) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتحسين التشخيص.")
        self.declare(Fact(disease="اللفحة المبكرة"))

    @Rule(
        OR(
            Symptom(name='بقع بنية مائية على حواف الأوراق', cf=MATCH.cf1),
            Symptom(name='هالات صفراء حول البقع', cf=MATCH.cf1),
            Symptom(name='ذبول الأوراق السفلية', cf=MATCH.cf1)
        ),
        TEST(lambda cf1: cf1 >= 60),
        salience=10,
    )
    def early_blight_weak(self, cf1):
        final = round(cf1 * 0.45)
        print(f"\n❗ احتمال ضعيف: اللفحة المبكرة (الطماطم) (درجة الثقة: {final}/100)")
        print("⚠️ يُنصح بإدخال المزيد من الأعراض لتأكيد التشخيص بسبب التشابه مع أعراض مرض آخر")
        self.declare(Fact(disease="اللفحة المبكرة"))

    @Rule(Fact(disease="اللفحة المبكرة"), salience=5)
    def early_blight_treatment(self):
        print("\n📌 المسبب: مرض اللفحة المبكرة في الطماطم يُسببه الفطر Alternaria solani.")
        print("\n💡 العلاج (اللفحة المبكرة - الطماطم):")
        print("- إزالة الأوراق المصابة وتحسين التهوية")
        print("- رش مبيدات فطرية تحتوي على Chlorothalonil أو Mancozeb")
        print("- تجنب الري فوق الأوراق")
        self.halt()




    #اللفحة المتأخرة
    @Rule(
        Symptom(name='بقع بنية مائية على حواف الأوراق', cf=MATCH.cf1),
        Symptom(name='تعفن بني على السيقان أو الثمار', cf=MATCH.cf2),
        Symptom(name='ظهور زغب رمادي أو أبيض تحت الأوراق', cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60)
    ,
        salience=30
    )
    def late_blight_full(self, cf1, cf2, cf3):
        final = round(min(cf1, cf2, cf3) * 0.85)
        print(f"\n✅ التشخيص: اللفحة المتأخرة (الطماطم) (درجة الثقة: {final}/100)")
        self.declare(Fact(disease="اللفحة المتأخرة"))

    @Rule(
        OR(
            AND(Symptom(name='بقع بنية مائية على حواف الأوراق', cf=MATCH.cf1),
                Symptom(name='تعفن بني على السيقان أو الثمار', cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name='بقع بنية مائية على حواف الأوراق', cf=MATCH.cf1),
                Symptom(name='ظهور زغب رمادي أو أبيض تحت الأوراق', cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name='تعفن بني على السيقان أو الثمار', cf=MATCH.cf1),
                Symptom(name='ظهور زغب رمادي أو أبيض تحت الأوراق', cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60))
        )
    ,
        salience=20
    )
    def late_blight_partial(self, cf1=0, cf2=0):
        final = round(min(cf1, cf2) * 0.65)
        print(f"\n⚠️ تشخيص مبدئي: اللفحة المتأخرة (الطماطم) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتحسين التشخيص.")
        self.declare(Fact(disease="اللفحة المتأخرة"))

    @Rule(
        OR(
            Symptom(name='بقع بنية مائية على حواف الأوراق', cf=MATCH.cf1),
            Symptom(name='تعفن بني على السيقان أو الثمار', cf=MATCH.cf1),
            Symptom(name='ظهور زغب رمادي أو أبيض تحت الأوراق', cf=MATCH.cf1)
        ),
        TEST(lambda cf1: cf1 >= 60),
        salience=10,
    )
    def late_blight_weak(self, cf1):
        final = round(cf1 * 0.45)
        print(f"\n❗ احتمال ضعيف: اللفحة المتأخرة (الطماطم) (درجة الثقة: {final}/100)")
        print("⚠️ يُنصح بإدخال المزيد من الأعراض لتأكيد التشخيص بسبب التشابه مع أعراض مرض آخر.")
        self.declare(Fact(disease="اللفحة المتأخرة"))

    @Rule(Fact(disease="اللفحة المتأخرة"), salience=5)
    def late_blight_treatment(self):
        print("\n📌 المسبب: مرض اللفحة المتأخرة في الطماطم يُسببه الفطر Phytophthora infestans.")
        print("\n💡 العلاج (اللفحة المتأخرة - الطماطم):")
        print("- إزالة الأجزاء المصابة فورًا")
        print("- رش مبيد فطري مثل Mancozeb أو Chlorothalonil")
        print("- تكرار الرش كل 7 أيام في حال استمرار الظروف الرطبة")
        print("- تجنب ري الأوراق مباشرة وتحسين التهوية بين النباتات")
        self.halt()


    #الذبول البكتيري
    @Rule(
        Symptom(name='ذبول مفاجئ دون اصفرار', cf=MATCH.cf1),
        Symptom(name='لا يظهر تعفن على الساق', cf=MATCH.cf2),
        Symptom(name='إفرازات مخاطية من قاعدة الساق', cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60)
    ,
        salience=30
    )
    def bacterial_wilt_full(self, cf1, cf2, cf3):
        final = round(min(cf1, cf2, cf3) * 0.85)
        print(f"\n✅ التشخيص: الذبول البكتيري (الطماطم) (درجة الثقة: {final}/100)")
        self.declare(Fact(disease="الذبول البكتيري"))

    @Rule(
        OR(
            AND(Symptom(name='ذبول مفاجئ دون اصفرار', cf=MATCH.cf1),
                Symptom(name='لا يظهر تعفن على الساق', cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name='ذبول مفاجئ دون اصفرار', cf=MATCH.cf1),
                Symptom(name='إفرازات مخاطية من قاعدة الساق', cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name='لا يظهر تعفن على الساق', cf=MATCH.cf1),
                Symptom(name='إفرازات مخاطية من قاعدة الساق', cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60))
        )
    ,
        salience=20
    )
    def bacterial_wilt_partial(self, cf1=0, cf2=0):
        final = round(min(cf1, cf2) * 0.65)
        print(f"\n⚠️ تشخيص مبدئي: الذبول البكتيري (الطماطم) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتحسين التشخيص.")
        self.declare(Fact(disease="الذبول البكتيري"))

    @Rule(
        OR(
            Symptom(name='ذبول مفاجئ دون اصفرار', cf=MATCH.cf1),
            Symptom(name='لا يظهر تعفن على الساق', cf=MATCH.cf1),
            Symptom(name='إفرازات مخاطية من قاعدة الساق', cf=MATCH.cf1)
        ),
        TEST(lambda cf1: cf1 >= 60)
    ,
        salience=10
    )
    def bacterial_wilt_weak(self, cf1):
        final = round(cf1 * 0.45)
        print(f"\n❗ احتمال ضعيف: الذبول البكتيري (الطماطم) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتحسين دقة التشخيص.")
        self.declare(Fact(disease="الذبول البكتيري"))

    @Rule(Fact(disease="الذبول البكتيري"), salience=5)
    def bacterial_wilt_treatment(self):
        print("\n📌 المسبب: مرض الذبول البكتيري في الطماطم يُسببه البكتيريا Ralstonia solanacearum.")
        print("\n💡 العلاج (الذبول البكتيري - الطماطم):")
        print("- إزالة النباتات المصابة فورًا لمنع الانتشار")
        print("- تعقيم التربة وتجنب الزراعة في نفس المكان")
        print("- زراعة أصناف مقاومة إن توفرت")
        print("- تجنب الجروح أثناء الزراعة وتقليل الري الزائد")
        self.halt()



    #  تبقع الأوراق البكتيري
    @Rule(
        Symptom(name='بقع بنية مائية على الأوراق', cf=MATCH.cf1),
        Symptom(name='تشقق الجلد على الثمار', cf=MATCH.cf2),
        Symptom(name='تساقط الأوراق', cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60)
    ,
        salience=30
    )
    def bacterial_spot_full(self, cf1, cf2, cf3):
        final = round(min(cf1, cf2, cf3) * 0.85)
        print(f"\n✅ التشخيص: تبقع الأوراق البكتيري (الطماطم) (درجة الثقة: {final}/100)")
        self.declare(Fact(disease="تبقع الأوراق البكتيري"))

    @Rule(
        OR(
            AND(Symptom(name='بقع بنية مائية على الأوراق', cf=MATCH.cf1),
                Symptom(name='تشقق الجلد على الثمار', cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name='بقع بنية مائية على الأوراق', cf=MATCH.cf1),
                Symptom(name='تساقط الأوراق', cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name='تشقق الجلد على الثمار', cf=MATCH.cf1),
                Symptom(name='تساقط الأوراق', cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60))
        )
    ,
        salience=20
    )
    def bacterial_spot_partial(self, cf1=0, cf2=0):
        final = round(min(cf1, cf2) * 0.65)
        print(f"\n⚠️ تشخيص مبدئي: تبقع الأوراق البكتيري (الطماطم) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتحسين التشخيص.")
        self.declare(Fact(disease="تبقع الأوراق البكتيري"))

    @Rule(
        OR(
            Symptom(name='بقع بنية مائية على الأوراق', cf=MATCH.cf1),
            Symptom(name='تشقق الجلد على الثمار', cf=MATCH.cf1),
            Symptom(name='تساقط الأوراق', cf=MATCH.cf1)
        ),
        TEST(lambda cf1: cf1 >= 60)
    ,
        salience=10
    )
    def bacterial_spot_weak(self, cf1):
        final = round(cf1 * 0.45)
        print(f"\n❗ احتمال ضعيف: تبقع الأوراق البكتيري (الطماطم) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتأكيد التشخيص.")
        self.declare(Fact(disease="تبقع الأوراق البكتيري"))

    @Rule(Fact(disease="تبقع الأوراق البكتيري"), salience=5)
    def bacterial_spot_treatment(self):
        print("\n📌 المسبب: مرض تبقّع الأوراق البكتيري في الطماطم يُسببه البكتيريا Xanthomonas vesicatoria.")
        print("\n💡 العلاج (تبقع الأوراق البكتيري - الطماطم):")
        print("- إزالة الأوراق المصابة فورًا لمنع الانتشار")
        print("- استخدام مبيدات نحاسية (Copper-based sprays) كل 7 أيام")
        print("- تجنب رش المياه على الأوراق")
        print("- زراعة أصناف مقاومة إن أمكن")
        self.halt()


    #  عفن الطرف الزهري
    @Rule(
        Symptom(name='بقعة سوداء غائرة في أسفل الثمرة', cf=MATCH.cf1),
        Symptom(name='تصبح قاسية وجافة', cf=MATCH.cf2),
        TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)
    ,
        salience=30
    )
    def blossom_end_rot_full(self, cf1, cf2):
        final = round(min(cf1, cf2) * 0.85)
        print(f"\n✅ التشخيص: عفن الطرف الزهري (الطماطم) – بسبب نقص الكالسيوم (درجة الثقة: {final}/100)")
        self.declare(Fact(disease="عفن الطرف الزهري"))


    @Rule(
        OR(
            Symptom(name='بقعة سوداء غائرة في أسفل الثمرة', cf=MATCH.cf1),
            Symptom(name='تصبح قاسية وجافة', cf=MATCH.cf1)
        ),
        TEST(lambda cf1: cf1 >= 60)
    ,
        salience=10
    )
    def blossom_end_rot_weak(self, cf1):
        final = round(cf1 * 0.45)
        print(f"\n❗ احتمال ضعيف: عفن الطرف الزهري (الطماطم) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال العرض الثاني لتأكيد التشخيص.")
        self.declare(Fact(disease="عفن الطرف الزهري"))

    @Rule(Fact(disease="عفن الطرف الزهري"), salience=5)
    def blossom_end_rot_treatment(self):
        print("\n📌 المسبب: مرض عفن الطرف الزهري في الطماطم يُسببه الفطر Botrytis cinerea.")
        print("\n💡 العلاج (عفن الطرف الزهري - الطماطم):")
        print("- إضافة مصدر كالسيوم إلى التربة (مثل نترات الكالسيوم)")
        print("- الحفاظ على رطوبة منتظمة في التربة (تجنب الجفاف المفاجئ)")
        print("- تجنب التسميد الزائد بالنيتروجين")
        print("- رش ورقي بكالسيوم في حال النقص الحاد")
        self.halt()




    #  موزاييك الطماطم
    @Rule(
        Symptom(name='تبرقش في لون الأوراق (أخضر فاتح/غامق)', cf=MATCH.cf1),
        Symptom(name='تشوه شكل الأوراق', cf=MATCH.cf2),
        Symptom(name='صغر حجم الثمار', cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60)
    ,
        salience=30
    )
    def tomato_mosaic_full(self, cf1, cf2, cf3):
        final = round(min(cf1, cf2, cf3) * 0.85)
        print(f"\n✅ التشخيص: فيروس موزاييك الطماطم (ToMV) (درجة الثقة: {final}/100)")
        self.declare(Fact(disease="موزاييك الطماطم"))

    @Rule(
        OR(
            AND(Symptom(name='تبرقش في لون الأوراق (أخضر فاتح/غامق)', cf=MATCH.cf1),
                Symptom(name='تشوه شكل الأوراق', cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name='تبرقش في لون الأوراق (أخضر فاتح/غامق)', cf=MATCH.cf1),
                Symptom(name='صغر حجم الثمار', cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name='تشوه شكل الأوراق', cf=MATCH.cf1),
                Symptom(name='صغر حجم الثمار', cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60))
        )
    ,
        salience=20
    )
    def tomato_mosaic_partial(self, cf1=0, cf2=0):
        final = round(min(cf1, cf2) * 0.65)
        print(f"\n⚠️ تشخيص مبدئي: موزاييك الطماطم (ToMV) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتحسين التشخيص.")
        self.declare(Fact(disease="موزاييك الطماطم"))

    @Rule(
        OR(
            Symptom(name='تبرقش في لون الأوراق (أخضر فاتح/غامق)', cf=MATCH.cf1),
            Symptom(name='تشوه شكل الأوراق', cf=MATCH.cf1),
            Symptom(name='صغر حجم الثمار', cf=MATCH.cf1)
        ),
        TEST(lambda cf1: cf1 >= 60)
    ,
        salience=10
    )
    def tomato_mosaic_weak(self, cf1):
        final = round(cf1 * 0.45)
        print(f"\n❗ احتمال ضعيف: موزاييك الطماطم (ToMV) (درجة الثقة: {final}/100)")
        print("⚠️ يُنصح بإدخال عرضين أو أكثر لتأكيد التشخيص.")
        self.declare(Fact(disease="موزاييك الطماطم"))

    @Rule(Fact(disease="موزاييك الطماطم"), salience=5)
    def tomato_mosaic_treatment(self):
        print("\n📌 المسبب: فيروس موزاييك الطماطم (Tomato Mosaic Virus) - ToMV")
        print("\n💡 العلاج (موزاييك الطماطم - ToMV):")
        print("- لا يوجد علاج مباشر، يُنصح بإزالة النباتات المصابة")
        print("- استخدام بذور مقاومة للفيروس عند الزراعة")
        print("- تعقيم الأدوات وتجنب ملامسة النباتات بأيدي ملوثة")
        print("- مكافحة الحشرات الناقلة مثل المنّ")
        self.halt()