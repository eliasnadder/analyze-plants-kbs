from experta import Rule, Fact, MATCH, TEST, OR, AND
from core import Symptom, PlantDiagnosisEngine

class OnionRules(PlantDiagnosisEngine):

    #البياض الزغبي
    @Rule(
        Symptom(name='بقع صفراء باهتة أو بنية طويلة على الأوراق الخارجية قد تتحول إلى نمو رمادي-بنفسجي تحت الرطوبة',
                cf=MATCH.cf1),
        Symptom(name='ذبول الأوراق المصابة وانحناؤها أو تساقطها', cf=MATCH.cf2),
        Symptom(name='البصليات تصبح طرية ومائية بسبب المرض', cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60)
    ,
        salience=30
    )
    def peronospora_destructor_full_3(self, cf1, cf2, cf3):
        final = round(min(cf1, cf2, cf3) * 0.85)
        print(f"\n✅ التشخيص: مرض البيرونوسبورا (Peronospora destructor) (درجة الثقة: {final}/100)")
        self.declare(Fact(disease="البيرونوسبورا"))


    @Rule(
        OR(
            AND(Symptom(
                name='بقع صفراء باهتة أو بنية طويلة على الأوراق الخارجية قد تتحول إلى نمو رمادي-بنفسجي تحت الرطوبة',
                cf=MATCH.cf1),
                Symptom(name='ذبول الأوراق المصابة وانحناؤها أو تساقطها', cf=MATCH.cf2)),
            AND(Symptom(
                name='بقع صفراء باهتة أو بنية طويلة على الأوراق الخارجية قد تتحول إلى نمو رمادي-بنفسجي تحت الرطوبة',
                cf=MATCH.cf1),
                Symptom(name='البصليات تصبح طرية ومائية بسبب المرض', cf=MATCH.cf2)),
            AND(Symptom(name='ذبول الأوراق المصابة وانحناؤها أو تساقطها', cf=MATCH.cf1),
                Symptom(name='البصليات تصبح طرية ومائية بسبب المرض', cf=MATCH.cf2))
        ),
        TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)
    ,
        salience=20
    )
    def peronospora_destructor_partial_strong(self, cf1, cf2):
        final = round(min(cf1, cf2) * 0.65)
        print(f"\n⚠️  تشخيص مبدئي: مرض البيرونوسبورا (Peronospora destructor) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتحسين التشخيص.")
        self.declare(Fact(disease="البيرونوسبورا"))


    @Rule(
        OR(
            Symptom(name='بقع صفراء باهتة أو بنية طويلة على الأوراق الخارجية قد تتحول إلى نمو رمادي-بنفسجي تحت الرطوبة',
                    cf=MATCH.cf1),
            Symptom(name='ذبول الأوراق المصابة وانحناؤها أو تساقطها', cf=MATCH.cf1),
            Symptom(name='البصليات تصبح طرية ومائية بسبب المرض', cf=MATCH.cf1)
        ),
        TEST(lambda cf1: cf1 >= 60)
    ,
        salience=10
    )
    def peronospora_destructor_weak(self, cf1):
        final = round(cf1 * 0.45)
        print(f"\n❗ احتمال ضعيف: مرض البيرونوسبورا (Peronospora destructor) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتحسين التشخيص.")
        self.declare(Fact(disease="البيرونوسبورا"))


    @Rule(Fact(disease="البيرونوسبورا"), salience=5)
    def peronospora_destructor_treatment(self):
        print("\n💡 العلاج (مرض البياض الزغبي - البصل):")
        print("\n📌 المسبب: مرض البياض الزغبي في البصل يُسببه الفطر Peronospora destructor.")
        print("- رش النبات بمبيد فطري وقائي مثل مبيدات النحاس أو مبيدات مانكوزيب.")
        print("- تحسين التهوية وتقليل الرطوبة حول النباتات.")
        print("- تجنب الزراعة الكثيفة وتحسين تباعد النباتات.")
        print("- إزالة وإتلاف الأجزاء المصابة فورًا.")
        print("- تجنب ري الأوراق بالرش، ويفضل الري الجذري.")
        self.halt()





    #بقعة البنفسج
    @Rule(
        Symptom(name='بقعة مائية صغيرة تتحول إلى بقعة داكنة ذات هالة صفراء', cf=MATCH.cf1),
        Symptom(name='تظهر بقعة هدف بنية-أرجوانية على الأوراق', cf=MATCH.cf2),
        Symptom(name='انتشار البقع وقت المطر أو الرذاذ', cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60)
    ,
        salience=30
    )
    def purple_blotch_full_3(self, cf1, cf2, cf3):
        final = round(min(cf1, cf2, cf3) * 0.85)
        print(f"\n✅ التشخيص: مرض بقعة البنفسج (Alternaria porri) (درجة الثقة: {final}/100)")
        self.declare(Fact(disease="بقعة البنفسج"))


    @Rule(
        OR(
            AND(Symptom(name='بقعة مائية صغيرة تتحول إلى بقعة داكنة ذات هالة صفراء', cf=MATCH.cf1),
                Symptom(name='تظهر بقعة هدف بنية-أرجوانية على الأوراق', cf=MATCH.cf2)),
            AND(Symptom(name='بقعة مائية صغيرة تتحول إلى بقعة داكنة ذات هالة صفراء', cf=MATCH.cf1),
                Symptom(name='انتشار البقع وقت المطر أو الرذاذ', cf=MATCH.cf2)),
            AND(Symptom(name='تظهر بقعة هدف بنية-أرجوانية على الأوراق', cf=MATCH.cf1),
                Symptom(name='انتشار البقع وقت المطر أو الرذاذ', cf=MATCH.cf2))
        ),
        TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)
    ,
        salience=20
    )
    def purple_blotch_partial_strong(self, cf1, cf2):
        final = round(min(cf1, cf2) * 0.65)
        print(f"\n⚠️  تشخيص مبدئي: مرض بقعة البنفسج (Alternaria porri) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتحسين التشخيص.")
        self.declare(Fact(disease="بقعة البنفسج"))


    @Rule(
        OR(
            Symptom(name='بقعة مائية صغيرة تتحول إلى بقعة داكنة ذات هالة صفراء', cf=MATCH.cf1),
            Symptom(name='تظهر بقعة هدف بنية-أرجوانية على الأوراق', cf=MATCH.cf1),
            Symptom(name='انتشار البقع وقت المطر أو الرذاذ', cf=MATCH.cf1)
        ),
        TEST(lambda cf1: cf1 >= 60)
    ,
        salience=10
    )
    def purple_blotch_weak(self, cf1):
        final = round(cf1 * 0.45)
        print(f"\n❗ احتمال ضعيف: مرض بقعة البنفسج (Alternaria porri) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتحسين التشخيص.")
        self.declare(Fact(disease="بقعة البنفسج"))


    @Rule(Fact(disease="بقعة البنفسج"), salience=5)
    def purple_blotch_treatment(self):
        print("\n📌 المسبب: مرض بقعة البنفسج في البصل يُسببه الفطر Alternaria porri.")
        print("\n💡 العلاج (مرض بقعة البنفسج - البصل):")
        print("- رش النبات بمبيد فطري وقائي مثل مبيدات تحتوي على مانكوزيب أو ديتمان أو النحاس.")
        print("- تجنب الري بالرش ويفضل الري الجذري لتقليل الرطوبة على الأوراق.")
        print("- إزالة وإتلاف الأجزاء المصابة فورًا.")
        print("- تحسين التهوية وتقليل كثافة الزراعة.")
        print("- زراعة أصناف مقاومة للمرض إن أمكن.")
        self.halt()



    #عفن الجذور الوردي
    @Rule(
        Symptom(name='جذور مصابة تصبح وردية أولاً، ثم تتحول إلى حمراء أو أرجوانية', cf=MATCH.cf1),
        Symptom(name='الجذور تصبح مائية وقابلة للتفتت', cf=MATCH.cf2),
        Symptom(name='ضعف نمو النبات وجفافه حتى قبل إنضاج البصلية', cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60)
    ,
        salience=30
    )
    def pink_root_rot_full_3(self, cf1, cf2, cf3):
        final = round(min(cf1, cf2, cf3) * 0.85)
        print(f"\n✅ التشخيص: مرض عفن الجذور الوردي (Pink Root Rot) (درجة الثقة: {final}/100)")
        self.declare(Fact(disease="عفن الجذور الوردي"))


    @Rule(
        OR(
            AND(Symptom(name='جذور مصابة تصبح وردية أولاً، ثم تتحول إلى حمراء أو أرجوانية', cf=MATCH.cf1),
                Symptom(name='الجذور تصبح مائية وقابلة للتفتت', cf=MATCH.cf2)),
            AND(Symptom(name='جذور مصابة تصبح وردية أولاً، ثم تتحول إلى حمراء أو أرجوانية', cf=MATCH.cf1),
                Symptom(name='ضعف نمو النبات وجفافه حتى قبل إنضاج البصلية', cf=MATCH.cf2)),
            AND(Symptom(name='الجذور تصبح مائية وقابلة للتفتت', cf=MATCH.cf1),
                Symptom(name='ضعف نمو النبات وجفافه حتى قبل إنضاج البصلية', cf=MATCH.cf2))
        ),
        TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)
    ,
        salience=20
    )
    def pink_root_rot_partial_strong(self, cf1, cf2):
        final = round(min(cf1, cf2) * 0.65)
        print(f"\n⚠️  تشخيص مبدئي: مرض عفن الجذور الوردي (Pink Root Rot) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتحسين التشخيص.")
        self.declare(Fact(disease="عفن الجذور الوردي"))


    @Rule(
        OR(
            Symptom(name='جذور مصابة تصبح وردية أولاً، ثم تتحول إلى حمراء أو أرجوانية', cf=MATCH.cf1),
            Symptom(name='الجذور تصبح مائية وقابلة للتفتت', cf=MATCH.cf1),
            Symptom(name='ضعف نمو النبات وجفافه حتى قبل إنضاج البصلية', cf=MATCH.cf1)
        ),
        TEST(lambda cf1: cf1 >= 60)
    ,
        salience=10
    )
    def pink_root_rot_weak(self, cf1):
        final = round(cf1 * 0.45)
        print(f"\n❗ احتمال ضعيف: مرض عفن الجذور الوردي (Pink Root Rot) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتحسين التشخيص.")
        self.declare(Fact(disease="عفن الجذور الوردي"))


    @Rule(Fact(disease="عفن الجذور الوردي"), salience=5)
    def pink_root_rot_treatment(self):
        print("\n📌 المسبب: مرض عفن الجذور الوردي في البصل يُسببه الفطر Fusarium oxysporum f. sp. cepae.")
        print("\n💡 العلاج (مرض عفن الجذور الوردي - البصل):")
        print("- زراعة أصناف مقاومة للمرض (إن وُجدت).")
        print("- تدوير المحاصيل وعدم زراعة البصل في نفس التربة لمدة 3-4 سنوات.")
        print("- تحسين تصريف التربة وتقليل الرطوبة الزائدة.")
        print("- تعقيم التربة قبل الزراعة (إذا أمكن).")
        print("- تجنب استخدام بذور أو شتلات ملوثة.")
        self.halt()





    #مرض الياقة

    @Rule(
        Symptom(name='طرى ورخاوة في قاعدة رقبة البصلة (الياقة)', cf=MATCH.cf1),
        Symptom(name='ظهور نمو فطري رمادي أو زغب أسود على الياقة أو بين القشور', cf=MATCH.cf2),
        Symptom(name='تعفن البصلة من الأعلى باتجاه الداخل أثناء التخزين', cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60)
    ,
        salience=30
    )
    def botrytis_neck_rot_full_3(self, cf1, cf2, cf3):
        final = round(min(cf1, cf2, cf3) * 0.85)
        print(f"\n✅ التشخيص: مرض عفن الياقة (Botrytis Neck Rot) (درجة الثقة: {final}/100)")
        self.declare(Fact(disease="عفن الياقة"))


    @Rule(
        OR(
            AND(Symptom(name='طرى ورخاوة في قاعدة رقبة البصلة (الياقة)', cf=MATCH.cf1),
                Symptom(name='ظهور نمو فطري رمادي أو زغب أسود على الياقة أو بين القشور', cf=MATCH.cf2)),
            AND(Symptom(name='طرى ورخاوة في قاعدة رقبة البصلة (الياقة)', cf=MATCH.cf1),
                Symptom(name='تعفن البصلة من الأعلى باتجاه الداخل أثناء التخزين', cf=MATCH.cf2)),
            AND(Symptom(name='ظهور نمو فطري رمادي أو زغب أسود على الياقة أو بين القشور', cf=MATCH.cf1),
                Symptom(name='تعفن البصلة من الأعلى باتجاه الداخل أثناء التخزين', cf=MATCH.cf2))
        ),
        TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)
    ,
        salience=20
    )
    def botrytis_neck_rot_partial_strong(self, cf1, cf2):
        final = round(min(cf1, cf2) * 0.65)
        print(f"\n⚠️  تشخيص مبدئي: مرض عفن الياقة (Botrytis Neck Rot) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتحسين التشخيص.")
        self.declare(Fact(disease="عفن الياقة"))


    @Rule(
        OR(
            Symptom(name='طرى ورخاوة في قاعدة رقبة البصلة (الياقة)', cf=MATCH.cf1),
            Symptom(name='ظهور نمو فطري رمادي أو زغب أسود على الياقة أو بين القشور', cf=MATCH.cf1),
            Symptom(name='تعفن البصلة من الأعلى باتجاه الداخل أثناء التخزين', cf=MATCH.cf1)
        ),
        TEST(lambda cf1: cf1 >= 60)
    ,
        salience=10
    )
    def botrytis_neck_rot_weak(self, cf1):
        final = round(cf1 * 0.45)
        print(f"\n❗ احتمال ضعيف: مرض عفن الياقة (Botrytis Neck Rot) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتحسين التشخيص.")
        self.declare(Fact(disease="عفن الياقة"))


    @Rule(Fact(disease="عفن الياقة"), salience=5)
    def botrytis_neck_rot_treatment(self):
        print("\n📌 المسبب: مرض الياقة في البصل يُسببه الفطر Phytophthora nicotianae.")
        print("\n💡 العلاج (مرض عفن الياقة - Botrytis Neck Rot):")
        print("- تجنب الإفراط في الري قبل الحصاد لتجنب ترطيب الأعناق.")
        print("- تجفيف البصليات جيدًا قبل التخزين.")
        print("- تخزين البصل في مكان جيد التهوية ومنخفض الرطوبة.")
        print("- رش النباتات قبل الحصاد بمبيد فطري وقائي (مثل مبيدات تحتوي على مانكوزيب أو فولبيك).")
        print("- إزالة وإتلاف البصليات المصابة قبل التخزين.")
        self.halt()






    #مرض دودة جذع البصل

    @Rule(
        Symptom(name='تضخم في الجذوع السفلية وتعفن جزئي', cf=MATCH.cf1),
        Symptom(name='أوراق ملتفة، صفراء وسريعة الذبول', cf=MATCH.cf2),
        Symptom(name='البصليات مشوهة أو ناعمة، غير قابلة للبيع', cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60)
    ,
        salience=30
    )
    def stem_bulb_nematode_full_3(self, cf1, cf2, cf3):
        final = round(min(cf1, cf2, cf3) * 0.85)
        print(f"\n✅ التشخيص: مرض دودة جذع البصل (Ditylenchus dipsaci) (درجة الثقة: {final}/100)")
        self.declare(Fact(disease="دودة جذع البصل"))


    @Rule(
        OR(
            AND(Symptom(name='تضخم في الجذوع السفلية وتعفن جزئي', cf=MATCH.cf1),
                Symptom(name='أوراق ملتفة، صفراء وسريعة الذبول', cf=MATCH.cf2)),
            AND(Symptom(name='تضخم في الجذوع السفلية وتعفن جزئي', cf=MATCH.cf1),
                Symptom(name='البصليات مشوهة أو ناعمة، غير قابلة للبيع', cf=MATCH.cf2)),
            AND(Symptom(name='أوراق ملتفة، صفراء وسريعة الذبول', cf=MATCH.cf1),
                Symptom(name='البصليات مشوهة أو ناعمة، غير قابلة للبيع', cf=MATCH.cf2))
        ),
        TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)
    ,
        salience=20
    )
    def stem_bulb_nematode_partial_strong(self, cf1, cf2):
        final = round(min(cf1, cf2) * 0.65)
        print(f"\n⚠️  تشخيص مبدئي: مرض دودة جذع البصل (Ditylenchus dipsaci) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتحسين التشخيص.")
        self.declare(Fact(disease="دودة جذع البصل"))


    @Rule(
        OR(
            Symptom(name='تضخم في الجذوع السفلية وتعفن جزئي', cf=MATCH.cf1),
            Symptom(name='أوراق ملتفة، صفراء وسريعة الذبول', cf=MATCH.cf1),
            Symptom(name='البصليات مشوهة أو ناعمة، غير قابلة للبيع', cf=MATCH.cf1)
        ),
        TEST(lambda cf1: cf1 >= 60)
    ,
        salience=10
    )
    def stem_bulb_nematode_weak(self, cf1):
        final = round(cf1 * 0.45)
        print(f"\n❗ احتمال ضعيف: مرض دودة جذع البصل (Ditylenchus dipsaci) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتحسين التشخيص.")
        self.declare(Fact(disease="دودة جذع البصل"))


    @Rule(Fact(disease="دودة جذع البصل"), salience=5)
    def stem_bulb_nematode_treatment(self):
        print("\n📌 المسبب: يرقات حشرة ذبابة جذع البصل (Delia antiqua)")
        print("\n💡 العلاج (مرض دودة جذع البصل - Nematode):")
        print("- زراعة أصناف مقاومة للديدان الخيطية (إن وُجدت).")
        print("- تدوير المحاصيل وعدم زراعة البصل في نفس التربة لمدة 3-4 سنوات.")
        print("- تعقيم التربة بالبخار أو مواد كيميائية قبل الزراعة.")
        print("- إزالة وإتلاف النباتات المصابة والبصليات التالفة.")
        print("- غمر التربة بالماء قبل الزراعة لقتل النيماتودا (في بعض الحالات).")
        self.halt()