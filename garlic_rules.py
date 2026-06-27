from experta import Rule, Fact, MATCH, TEST, OR, AND
from core import Symptom, PlantDiagnosisEngine

class GarlicRules(PlantDiagnosisEngine):

    #البياض الزعبي
    @Rule(
        Symptom(name='اصفرار الأوراق من الأطراف نحو القاعدة', cf=MATCH.cf1),
        Symptom(name='ظهور نمو رمادي مزرق على السطح السفلي للأوراق', cf=MATCH.cf2),
        Symptom(name='تدهور مبكر للنباتات وسقوط الأوراق', cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60)
    ,
        salience=30
    )
    def downy_mildew_full_3(self, cf1, cf2, cf3):
        final = round(min(cf1, cf2, cf3) * 0.85)
        print(f"\n✅ التشخيص: مرض البياض الزغبي (Peronospora destructor) (درجة الثقة: {final}/100)")
        self.declare(Fact(disease="البياض الزغبي"))


    @Rule(
        OR(
            AND(Symptom(name='اصفرار الأوراق من الأطراف نحو القاعدة', cf=MATCH.cf1),
                Symptom(name='ظهور نمو رمادي مزرق على السطح السفلي للأوراق', cf=MATCH.cf2)),
            AND(Symptom(name='اصفرار الأوراق من الأطراف نحو القاعدة', cf=MATCH.cf1),
                Symptom(name='تدهور مبكر للنباتات وسقوط الأوراق', cf=MATCH.cf2)),
            AND(Symptom(name='ظهور نمو رمادي مزرق على السطح السفلي للأوراق', cf=MATCH.cf1),
                Symptom(name='تدهور مبكر للنباتات وسقوط الأوراق', cf=MATCH.cf2))
        ),
        TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)
    ,
        salience=20
    )
    def downy_mildew_partial_strong(self, cf1, cf2):
        final = round(min(cf1, cf2) * 0.65)
        print(f"\n⚠️ تشخيص مبدئي: مرض البياض الزغبي (Peronospora destructor) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتأكيد التشخيص.")
        self.declare(Fact(disease="البياض الزغبي"))


    @Rule(
        OR(
            Symptom(name='اصفرار الأوراق من الأطراف نحو القاعدة', cf=MATCH.cf1),
            Symptom(name='ظهور نمو رمادي مزرق على السطح السفلي للأوراق', cf=MATCH.cf1),
            Symptom(name='تدهور مبكر للنباتات وسقوط الأوراق', cf=MATCH.cf1)
        ),
        TEST(lambda cf1: cf1 >= 60)
    ,
        salience=10
    )
    def downy_mildew_weak(self, cf1):
        final = round(cf1 * 0.45)
        print(f"\n❗ احتمال ضعيف: مرض البياض الزغبي (Peronospora destructor) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتحسين التشخيص.")
        self.declare(Fact(disease="البياض الزغبي"))


    @Rule(Fact(disease="البياض الزغبي"), salience=5)
    def garlic_downy_mildew_treatment(self):
        print("\n📌 المسبب: مرض البياض الزغبي في الثوم يُسببه الفطر Peronospora destructor.")
        print("\n💡 العلاج (مرض البياض الزغبي - Peronospora destructor):")
        print("- رش النبات بمبيد فطري وقائي مثل مبيدات النحاس أو مانكوزيب.")
        print("- تجنب الري بالرش ويفضل الري الجذري لتقليل الرطوبة على الأوراق.")
        print("- تحسين التهوية وتقليل كثافة الزراعة.")
        print("- إزالة وإتلاف الأجزاء المصابة فورًا.")
        print("- زراعة أصناف مقاومة للمرض إن أمكن.")
        self.halt()




       #العفن الرمادي
    @Rule(
        Symptom(name='رقّة قاعدة الساق (العنق) وتلونها بلون بني رمادي', cf=MATCH.cf1),
        Symptom(name='ظهور زغب رمادي على العنق أثناء التخزين', cf=MATCH.cf2),
        Symptom(name='تفكك أنسجة العنق وتعفن البصلة من الأعلى', cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60)
    ,
        salience=30
    )
    def gray_neck_rot_full_3(self, cf1, cf2, cf3):
        final = round(min(cf1, cf2, cf3) * 0.85)
        print(f"\n✅ التشخيص: مرض عفن العنق الرمادي (Botrytis allii) (درجة الثقة: {final}/100)")
        self.declare(Fact(disease="عفن العنق الرمادي"))



    @Rule(
        OR(
            AND(Symptom(name='رقّة قاعدة الساق (العنق) وتلونها بلون بني رمادي', cf=MATCH.cf1),
                Symptom(name='ظهور زغب رمادي على العنق أثناء التخزين', cf=MATCH.cf2)),
            AND(Symptom(name='رقّة قاعدة الساق (العنق) وتلونها بلون بني رمادي', cf=MATCH.cf1),
                Symptom(name='تفكك أنسجة العنق وتعفن البصلة من الأعلى', cf=MATCH.cf2)),
            AND(Symptom(name='ظهور زغب رمادي على العنق أثناء التخزين', cf=MATCH.cf1),
                Symptom(name='تفكك أنسجة العنق وتعفن البصلة من الأعلى', cf=MATCH.cf2))
        ),
        TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)
    ,
        salience=20
    )
    def gray_neck_rot_partial_strong(self, cf1, cf2):
        final = round(min(cf1, cf2) * 0.65)
        print(f"\n⚠️  تشخيص مبدئي: مرض عفن العنق الرمادي (Botrytis allii) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتأكيد التشخيص.")
        self.declare(Fact(disease="عفن العنق الرمادي"))



    @Rule(
        OR(
            Symptom(name='رقّة قاعدة الساق (العنق) وتلونها بلون بني رمادي', cf=MATCH.cf1),
            Symptom(name='ظهور زغب رمادي على العنق أثناء التخزين', cf=MATCH.cf1),
            Symptom(name='تفكك أنسجة العنق وتعفن البصلة من الأعلى', cf=MATCH.cf1)
        ),
        TEST(lambda cf1: cf1 >= 60)
    ,
        salience=10
    )
    def gray_neck_rot_weak(self, cf1):
        final = round(cf1 * 0.45)
        print(f"\n❗ احتمال ضعيف: مرض عفن العنق الرمادي (Botrytis allii) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتحسين التشخيص.")
        self.declare(Fact(disease="عفن العنق الرمادي"))



    @Rule(Fact(disease="عفن العنق الرمادي"), salience=5)
    def gray_neck_rot_treatment(self):
        print("\n📌 المسبب: مرض العفن الرمادي في الثوم يُسببه الفطر Botrytis allii.")
        print("\n💡 العلاج (مرض عفن العنق الرمادي - Botrytis allii):")
        print("- تجنب الإفراط في الري قبل الحصاد لتجنب ترطيب الأعناق.")
        print("- تجفيف البصليات جيدًا قبل التخزين.")
        print("- تخزين البصل في مكان جيد التهوية ومنخفض الرطوبة.")
        print("- رش النباتات قبل الحصاد بمبيد فطري وقائي (مثل مبيدات تحتوي على مانكوزيب أو فولبيك).")
        print("- إزالة وإتلاف البصليات المصابة قبل التخزين.")
        self.halt()





    #عفن الزرقاء

    @Rule(
        Symptom(name='بقع مائية على البصلة تبدأ من الجروح', cf=MATCH.cf1),
        Symptom(name='نمو فطري أزرق مخضر على سطح البصلة', cf=MATCH.cf2),
        Symptom(name='رائحة عفن نفاذة عند شق البصلة', cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60)
    ,
        salience=30
    )
    def blue_mold_full_3(self, cf1, cf2, cf3):
        final = round(min(cf1, cf2, cf3) * 0.85)
        print(f"\n✅ التشخيص: مرض عفن الزُرقاء (Penicillium hirsutum) (درجة الثقة: {final}/100)")
        self.declare(Fact(disease="عفن الزُرقاء"))


    @Rule(
        OR(
            AND(Symptom(name='بقع مائية على البصلة تبدأ من الجروح', cf=MATCH.cf1),
                Symptom(name='نمو فطري أزرق مخضر على سطح البصلة', cf=MATCH.cf2)),
            AND(Symptom(name='بقع مائية على البصلة تبدأ من الجروح', cf=MATCH.cf1),
                Symptom(name='رائحة عفن نفاذة عند شق البصلة', cf=MATCH.cf2)),
            AND(Symptom(name='نمو فطري أزرق مخضر على سطح البصلة', cf=MATCH.cf1),
                Symptom(name='رائحة عفن نفاذة عند شق البصلة', cf=MATCH.cf2))
        ),
        TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)
    ,
        salience=20
    )
    def blue_mold_partial_strong(self, cf1, cf2):
        final = round(min(cf1, cf2) * 0.65)
        print(f"\n⚠️  تشخيص مبدئي: مرض عفن الزُرقاء (Penicillium hirsutum) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتأكيد التشخيص.")
        self.declare(Fact(disease="عفن الزُرقاء"))


    @Rule(
        OR(
            Symptom(name='بقع مائية على البصلة تبدأ من الجروح', cf=MATCH.cf1),
            Symptom(name='نمو فطري أزرق مخضر على سطح البصلة', cf=MATCH.cf1),
            Symptom(name='رائحة عفن نفاذة عند شق البصلة', cf=MATCH.cf1)
        ),
        TEST(lambda cf1: cf1 >= 60)
    ,
        salience=10
    )
    def blue_mold_weak(self, cf1):
        final = round(cf1 * 0.45)
        print(f"\n❗ احتمال ضعيف: مرض عفن الزُرقاء (Penicillium hirsutum) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتحسين التشخيص.")
        self.declare(Fact(disease="عفن الزُرقاء"))


    @Rule(Fact(disease="عفن الزُرقاء"), salience=5)
    def blue_mold_treatment(self):
        print("\n📌 المسبب: مرض عفن الزرقاء في الثوم يُسببه الفطر Penicillium allii.")
        print("\n💡 العلاج (مرض عفن الزُرقاء - Penicillium hirsutum):")
        print("- تجنب إحداث جروح في البصل أثناء الحصاد.")
        print("- تجفيف البصل جيدًا قبل التخزين.")
        print("- تخزين البصل في مكان جيد التهوية ومنخفض الرطوبة.")
        print("- فرز البصل بعناية وإزالة المصابة قبل التخزين.")
        print("- تعقيم أدوات الحصاد وأماكن التخزين.")
        self.halt()


    #العفن الابيض
    @Rule(
        Symptom(name='اصفرار الأوراق وذبول مفاجئ للنبات', cf=MATCH.cf1),
        Symptom(name='نمو أبيض قطني كثيف على قاعدة النبات', cf=MATCH.cf2),
        Symptom(name='ظهور أجسام سوداء صغيرة (سكليروشيا) في التربة حول الجذور', cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60)
    ,
        salience=30
    )
    def white_rot_full_3(self, cf1, cf2, cf3):
        final = round(min(cf1, cf2, cf3) * 0.85)
        print(f"\n✅ التشخيص: مرض العفن الأبيض (Stromatinia cepivora) (درجة الثقة: {final}/100)")
        self.declare(Fact(disease="العفن الأبيض"))


    @Rule(
        OR(
            AND(Symptom(name='اصفرار الأوراق وذبول مفاجئ للنبات', cf=MATCH.cf1),
                Symptom(name='نمو أبيض قطني كثيف على قاعدة النبات', cf=MATCH.cf2)),
            AND(Symptom(name='اصفرار الأوراق وذبول مفاجئ للنبات', cf=MATCH.cf1),
                Symptom(name='ظهور أجسام سوداء صغيرة (سكليروشيا) في التربة حول الجذور', cf=MATCH.cf2)),
            AND(Symptom(name='نمو أبيض قطني كثيف على قاعدة النبات', cf=MATCH.cf1),
                Symptom(name='ظهور أجسام سوداء صغيرة (سكليروشيا) في التربة حول الجذور', cf=MATCH.cf2))
        ),
        TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)
    ,
        salience=20
    )
    def white_rot_partial_strong(self, cf1, cf2):
        final = round(min(cf1, cf2) * 0.65)
        print(f"\n⚠️ تشخيص مبدئي: مرض العفن الأبيض (Stromatinia cepivora) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتأكيد التشخيص.")
        self.declare(Fact(disease="العفن الأبيض"))


    @Rule(
        OR(
            Symptom(name='اصفرار الأوراق وذبول مفاجئ للنبات', cf=MATCH.cf1),
            Symptom(name='نمو أبيض قطني كثيف على قاعدة النبات', cf=MATCH.cf1),
            Symptom(name='ظهور أجسام سوداء صغيرة (سكليروشيا) في التربة حول الجذور', cf=MATCH.cf1)
        ),
        TEST(lambda cf1: cf1 >= 60)
    ,
        salience=10
    )
    def white_rot_weak(self, cf1):
        final = round(cf1 * 0.45)
        print(f"\n❗ احتمال ضعيف: مرض العفن الأبيض (Stromatinia cepivora) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتحسين التشخيص.")
        self.declare(Fact(disease="العفن الأبيض"))


    @Rule(Fact(disease="العفن الأبيض"), salience=5)
    def white_rot_treatment(self):
        print("\n📌 المسبب: مرض العفن الأبيض في الثوم يُسببه الفطر Sclerotium cepivorum.")
        print("\n💡 العلاج (مرض العفن الأبيض - Stromatinia cepivora):")
        print("- تجنب زراعة البصل أو الثوم في نفس التربة المصابة لمدة 4-5 سنوات.")
        print("- تعقيم التربة بالبخار أو مواد كيميائية قبل الزراعة.")
        print("- إزالة وإتلاف النباتات المصابة مع التربة المحيطة بها.")
        print("- زراعة أصناف مقاومة إن أمكن.")
        print("- تجنب الرطوبة العالية وتحسين تصريف التربة.")
        self.halt()





    @Rule(
        Symptom(name='تبرقش أصفر أو أخضر فاتح على الأوراق الطرية', cf=MATCH.cf1),
        Symptom(name='تقزم النبات وضعف في تكوين الأبصال', cf=MATCH.cf2),
        Symptom(name='تشوه في شكل الأوراق وتأخر في النمو', cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60)
    ,
        salience=30
    )
    def viral_complex_full_3(self, cf1, cf2, cf3):
        final = round(min(cf1, cf2, cf3) * 0.85)
        print(f"\n✅ التشخيص: الذبول الفيروسي المشترك (OYDV – GCLV – LYSV – SLV) (درجة الثقة: {final}/100)")
        self.declare(Fact(disease="الذبول الفيروسي المشترك"))


    @Rule(
        OR(
            AND(Symptom(name='تبرقش أصفر أو أخضر فاتح على الأوراق الطرية', cf=MATCH.cf1),
                Symptom(name='تقزم النبات وضعف في تكوين الأبصال', cf=MATCH.cf2)),
            AND(Symptom(name='تبرقش أصفر أو أخضر فاتح على الأوراق الطرية', cf=MATCH.cf1),
                Symptom(name='تشوه في شكل الأوراق وتأخر في النمو', cf=MATCH.cf2)),
            AND(Symptom(name='تقزم النبات وضعف في تكوين الأبصال', cf=MATCH.cf1),
                Symptom(name='تشوه في شكل الأوراق وتأخر في النمو', cf=MATCH.cf2))
        ),
        TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)
    ,
        salience=20
    )
    def viral_complex_partial_strong(self, cf1, cf2):
        final = round(min(cf1, cf2) * 0.65)
        print(f"\n⚠️ تشخيص مبدئي: الذبول الفيروسي المشترك (OYDV – GCLV – LYSV – SLV) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتأكيد التشخيص.")
        self.declare(Fact(disease="الذبول الفيروسي المشترك"))


    @Rule(
        OR(
            Symptom(name='تبرقش أصفر أو أخضر فاتح على الأوراق الطرية', cf=MATCH.cf1),
            Symptom(name='تقزم النبات وضعف في تكوين الأبصال', cf=MATCH.cf1),
            Symptom(name='تشوه في شكل الأوراق وتأخر في النمو', cf=MATCH.cf1)
        ),
        TEST(lambda cf1: cf1 >= 60)
    ,
        salience=10
    )
    def viral_complex_weak(self, cf1):
        final = round(cf1 * 0.45)
        print(f"\n❗ احتمال ضعيف: الذبول الفيروسي المشترك (OYDV – GCLV – LYSV – SLV) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتحسين التشخيص.")
        self.declare(Fact(disease="الذبول الفيروسي المشترك"))


    @Rule(Fact(disease="الذبول الفيروسي المشترك"), salience=5)
    def viral_complex_treatment(self):
        print("\n📌 المسبب: فيروس الذبول المشترك للثوم (Garlic Common Yellowing Virus) - GCLYV")
        print("\n💡 العلاج (الذبول الفيروسي المشترك ):")
        print("- لا يوجد علاج فعّال للعدوى الفيروسية.")
        print("- إزالة وإتلاف النباتات المصابة فورًا لتجنب انتشار الفيروس.")
        print("- مكافحة الآفات الناقلة (خاصة المن) باستخدام مبيدات حشرية.")
        print("- استخدام بذور أو شتلات خالية من الفيروس.")
        print("- زراعة أصناف مقاومة أو مطعّمة.")
        print("- تجنب زراعة البصل بالقرب من محاصيل مصابة (مثل الثوم أو الكزبرة).")
        self.halt()