from experta import Rule, Fact, MATCH, TEST, OR, AND
from core import Symptom, PlantDiagnosisEngine

class EggplantRules(PlantDiagnosisEngine):

    #الذبول البكتيري
    @Rule(
        Symptom(name='ذبول مفاجئ للنبات بدون اصفرار سابق', cf=MATCH.cf1),
        Symptom(name='تحول الساق الداخلي إلى اللون البني – يظهر عند قطع الجذع انسياب سائل مخاطي', cf=MATCH.cf2),
        Symptom(name='موت النبات بالكامل، خصوصًا في الطقس الدافئ والرطب', cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60)
    ,
        salience=30
    )
    def bacterial_wilt_eggplant_full_3(self, cf1, cf2, cf3):
        final = round(min(cf1, cf2, cf3) * 0.85)
        print(f"\n✅ التشخيص: مرض الذبول البكتيري (الباذنجان) (درجة الثقة: {final}/100)")
        self.declare(Fact(disease="الذبول البكتيري"))

    @Rule(
        OR(
            AND(Symptom(name='ذبول مفاجئ للنبات بدون اصفرار سابق', cf=MATCH.cf1),
                Symptom(name='تحول الساق الداخلي إلى اللون البني – يظهر عند قطع الجذع انسياب سائل مخاطي',
                        cf=MATCH.cf2)),
            AND(Symptom(name='ذبول مفاجئ للنبات بدون اصفرار سابق', cf=MATCH.cf1),
                Symptom(name='موت النبات بالكامل، خصوصًا في الطقس الدافئ والرطب', cf=MATCH.cf2)),
            AND(Symptom(name='تحول الساق الداخلي إلى اللون البني – يظهر عند قطع الجذع انسياب سائل مخاطي', cf=MATCH.cf1),
                Symptom(name='موت النبات بالكامل، خصوصًا في الطقس الدافئ والرطب', cf=MATCH.cf2))
        ),
        TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)
    ,
        salience=20
    )
    def bacterial_wilt_eggplant_partial_strong(self, cf1, cf2):
        final = round(min(cf1, cf2) * 0.65)
        print(f"\n⚠️  تشخيص مبدئي: مرض الذبول البكتيري (الباذنجان) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتأكيد التشخيص.")
        self.declare(Fact(disease="الذبول البكتيري"))

    @Rule(
        OR(
            Symptom(name='ذبول مفاجئ للنبات بدون اصفرار سابق', cf=MATCH.cf1),
            Symptom(name='تحول الساق الداخلي إلى اللون البني – يظهر عند قطع الجذع انسياب سائل مخاطي', cf=MATCH.cf1),
            Symptom(name='موت النبات بالكامل، خصوصًا في الطقس الدافئ والرطب', cf=MATCH.cf1)
        ),
        TEST(lambda cf1: cf1 >= 60)
    ,
        salience=10
    )
    def bacterial_wilt_eggplant_weak(self, cf1):
        final = round(cf1 * 0.45)
        print(f"\n❗ احتمال ضعيف: مرض الذبول البكتيري (الباذنجان) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتحسين التشخيص.")
        self.declare(Fact(disease="الذبول البكتيري"))

    @Rule(Fact(disease="الذبول البكتيري"), salience=5)
    def bacterial_wilt_eggplant_treatment(self):
        print("\n📌 المسبب: مرض الذبول البكتيري في الباذنجان يُسببه البكتيريا Ralstonia solanacearum.")
        print("\n💡 العلاج (مرض الذبول البكتيري - الباذنجان):")
        print("- إزالة النباتات المصابة فورًا والتخلص منها (لا تُعاد كسماد).")
        print("- تجنب زراعة الباذنجان أو البطاطا في نفس التربة المصابة لمدة 2-3 سنوات.")
        print("- تعقيم أدوات العمل بين النباتات.")
        print("- تحسين تصريف التربة وتقليل الرطوبة حول الجذور.")
        print("- لا يوجد علاج فعّال، لذا يُركز على الوقاية فقط.")
        self.halt()


    #الذبول الفيوزاريومي
    @Rule(
        Symptom(name='اصفرار الأوراق السفلية تدريجيًا، ثم ذبولها', cf=MATCH.cf1),
        Symptom(name='تظهر بقع بنية على الأوعية الوعائية داخل الساق عند تقطيعها', cf=MATCH.cf2),
        Symptom(name='ضعف النمو وتراجع إنتاج الثمار', cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60)
    ,
        salience=30
    )
    def verticillium_wilt_full_3(self, cf1, cf2, cf3):
        final = round(min(cf1, cf2, cf3) * 0.85)
        print(f"\n✅ التشخيص: مرض الذبول الفيوزاريومي (الباذنجان) (درجة الثقة: {final}/100)")
        self.declare(Fact(disease="الذبول الفيوزاريومي"))

    @Rule(
        OR(
            AND(Symptom(name='اصفرار الأوراق السفلية تدريجيًا، ثم ذبولها', cf=MATCH.cf1),
                Symptom(name='تظهر بقع بنية على الأوعية الوعائية داخل الساق عند تقطيعها', cf=MATCH.cf2)),
            AND(Symptom(name='اصفرار الأوراق السفلية تدريجيًا، ثم ذبولها', cf=MATCH.cf1),
                Symptom(name='ضعف النمو وتراجع إنتاج الثمار', cf=MATCH.cf2)),
            AND(Symptom(name='تظهر بقع بنية على الأوعية الوعائية داخل الساق عند تقطيعها', cf=MATCH.cf1),
                Symptom(name='ضعف النمو وتراجع إنتاج الثمار', cf=MATCH.cf2))
        ),
        TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)
    ,
        salience=20
    )
    def verticillium_wilt_partial_strong(self, cf1, cf2):
        final = round(min(cf1, cf2) * 0.65)
        print(f"\n⚠️  تشخيص مبدئي: مرض الذبول الفيوزاريومي (الباذنجان) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتأكيد التشخيص.")
        self.declare(Fact(disease="الذبول الفيوزاريومي"))

    @Rule(
        OR(
            Symptom(name='اصفرار الأوراق السفلية تدريجيًا، ثم ذبولها', cf=MATCH.cf1),
            Symptom(name='تظهر بقع بنية على الأوعية الوعائية داخل الساق عند تقطيعها', cf=MATCH.cf1),
            Symptom(name='ضعف النمو وتراجع إنتاج الثمار', cf=MATCH.cf1)
        ),
        TEST(lambda cf1: cf1 >= 60),
        salience=10
    )
    def verticillium_wilt_weak(self, cf1):
        final = round(cf1 * 0.45)
        print(f"\n❗ احتمال ضعيف: مرض الذبول الفيوزاريومي (الباذنجان) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتحسين التشخيص بسبب التشابه مع مرض اخر")
        self.declare(Fact(disease="الذبول الفيوزاريومي"))

    @Rule(Fact(disease="الذبول الفيوزاريومي"), salience=5)
    def verticillium_wilt_treatment(self):
        print("\n📌 المسبب: مرض الذبول الفيوزاريومي في الباذنجان يُسببه الفطر Fusarium oxysporum f. sp. melongenae.")
        print("\n💡 العلاج (مرض الذبول الفيوزاريومي - الباذنجان):")
        print("- زراعة أصناف مقاومة للمرض (معتمدة).")
        print("- تدوير المحاصيل وعدم زراعة الباذنجان أو البطاطا أو الطماطم في نفس التربة لمدة 3-4 سنوات.")
        print("- تعقيم التربة بالبخار أو المواد الكيميائية (مثل الميثيل برومايد أو البديل الآمن).")
        print("- تحسين تصريف التربة وتقليل الري الزائد.")
        print("- إزالة وإتلاف النباتات المصابة.")
        self.halt()


    #مرض عفن الفاكهة والفيوغثور
    @Rule(
        Symptom(name='بقع بنية مائية على الثمار، خاصة في النبات السفلي', cf=MATCH.cf1),
        Symptom(name='تعفن الساقين عند قاعدة النبات، مع ظهور طبقة بيضاء زغبية', cf=MATCH.cf2),
        Symptom(name='ضعف النمو وتراجع إنتاج الثمار', cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60)
    ,
        salience=30
    )
    def phytophthora_blight_full_3(self, cf1, cf2, cf3):
        final = round(min(cf1, cf2, cf3) * 0.85)
        print(f"\n✅ التشخيص: مرض عفن الفاكهة والفيوغثور (الباذنجان) (درجة الثقة: {final}/100)")
        self.declare(Fact(disease="عفن الفاكهة والفيوغثور"))

    @Rule(
        OR(
            AND(Symptom(name='بقع بنية مائية على الثمار، خاصة في النبات السفلي', cf=MATCH.cf1),
                Symptom(name='تعفن الساقين عند قاعدة النبات، مع ظهور طبقة بيضاء زغبية', cf=MATCH.cf2)),
            AND(Symptom(name='بقع بنية مائية على الثمار، خاصة في النبات السفلي', cf=MATCH.cf1),
                Symptom(name='ضعف النمو وتراجع إنتاج الثمار', cf=MATCH.cf2)),
            AND(Symptom(name='تعفن الساقين عند قاعدة النبات، مع ظهور طبقة بيضاء زغبية', cf=MATCH.cf1),
                Symptom(name='ضعف النمو وتراجع إنتاج الثمار', cf=MATCH.cf2))
        ),
        TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)
    ,
        salience=20
    )
    def phytophthora_blight_partial_strong(self, cf1, cf2):
        final = round(min(cf1, cf2) * 0.65)
        print(f"\n⚠️  تشخيص مبدئي: مرض عفن الفاكهة والفيوغثور (الباذنجان) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتأكيد التشخيص.")
        self.declare(Fact(disease="عفن الفاكهة والفيوغثور"))

    @Rule(
        OR(
            Symptom(name='بقع بنية مائية على الثمار، خاصة في النبات السفلي', cf=MATCH.cf1),
            Symptom(name='تعفن الساقين عند قاعدة النبات، مع ظهور طبقة بيضاء زغبية', cf=MATCH.cf1),
            Symptom(name='ضعف النمو وتراجع إنتاج الثمار', cf=MATCH.cf1)
        ),
        TEST(lambda cf1: cf1 >= 60),
        salience=10
    )
    def phytophthora_blight_weak(self, cf1):
        final = round(cf1 * 0.45)
        print(f"\n❗ احتمال ضعيف: مرض عفن الفاكهة والفيوغثور (الباذنجان) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتحسين التشخيص بسبب التشابه مع مرض اخر")
        self.declare(Fact(disease="عفن الفاكهة والفيوغثور"))

    @Rule(Fact(disease="عفن الفاكهة والفيوغثور"), salience=5)
    def phytophthora_blight_treatment(self):
        print("\n📌 المسبب: مرض عفن الفاكهة والفيوغثور في الباذنجان يُسببه الفطر Phytophthora capsici.")
        print("\n💡 العلاج (مرض عفن الفاكهة والفيوغثور - الباذنجان):")
        print("- تحسين تصريف التربة وتقليل الري الزائد.")
        print("- رش النبات بمبيد فطري مضاد للفيوغثور مثل مبيدات تحتوي على مانيتول أو ميتالاكسيل.")
        print("- إزالة وإتلاف النباتات المصابة فورًا.")
        print("- تعقيم التربة قبل الزراعة الجديدة.")
        print("- تجنب الزراعة الكثيفة وتحسين التهوية بين النباتات.")
        self.halt()


    #تبقع الأوراق
    @Rule(
        Symptom(name='بقع دائرية داكنة على الأوراق، غالبًا محاطة بهالة صفراء', cf=MATCH.cf1),
        Symptom(name='انثقاب البقع وتحولها إلى "ثقوب" عند تقدم الإصابة', cf=MATCH.cf2),
        Symptom(name='تساقط الأوراق وضعف التمثيل الضوئي', cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60)
    ,
        salience=30
    )
    def cercospora_leaf_spot_full_3(self, cf1, cf2, cf3):
        final = round(min(cf1, cf2, cf3) * 0.85)
        print(f"\n✅ التشخيص: مرض تبقّع الأوراق (Cercospora) (درجة الثقة: {final}/100)")
        self.declare(Fact(disease="تبقّع الأوراق"))

    @Rule(
        OR(
            AND(Symptom(name='بقع دائرية داكنة على الأوراق، غالبًا محاطة بهالة صفراء', cf=MATCH.cf1),
                Symptom(name='انثقاب البقع وتحولها إلى "ثقوب" عند تقدم الإصابة', cf=MATCH.cf2)),
            AND(Symptom(name='بقع دائرية داكنة على الأوراق، غالبًا محاطة بهالة صفراء', cf=MATCH.cf1),
                Symptom(name='تساقط الأوراق وضعف التمثيل الضوئي', cf=MATCH.cf2)),
            AND(Symptom(name='انثقاب البقع وتحولها إلى "ثقوب" عند تقدم الإصابة', cf=MATCH.cf1),
                Symptom(name='تساقط الأوراق وضعف التمثيل الضوئي', cf=MATCH.cf2))
        ),
        TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)
    ,
        salience=20
    )
    def cercospora_leaf_spot_partial_strong(self, cf1, cf2):
        final = round(min(cf1, cf2) * 0.65)
        print(f"\n⚠️  تشخيص مبدئي: مرض تبقّع الأوراق (Cercospora) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتأكيد التشخيص.")
        self.declare(Fact(disease="تبقّع الأوراق"))

    @Rule(
        OR(
            Symptom(name='بقع دائرية داكنة على الأوراق، غالبًا محاطة بهالة صفراء', cf=MATCH.cf1),
            Symptom(name='انثقاب البقع وتحولها إلى "ثقوب" عند تقدم الإصابة', cf=MATCH.cf1),
            Symptom(name='تساقط الأوراق وضعف التمثيل الضوئي', cf=MATCH.cf1)
        ),
        TEST(lambda cf1: cf1 >= 60)
    ,
        salience=10
    )
    def cercospora_leaf_spot_weak(self, cf1):
        final = round(cf1 * 0.45)
        print(f"\n❗ احتمال ضعيف: مرض تبقّع الأوراق (Cercospora) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتحسين التشخيص.")
        self.declare(Fact(disease="تبقّع الأوراق"))

    @Rule(Fact(disease="تبقّع الأوراق"), salience=5)
    def cercospora_leaf_spot_treatment(self):
        print("\n📌 المسبب: مرض تبقّع الأوراق في الباذنجان يُسببه الفطر Alternaria solani.")
        print("\n💡 العلاج (مرض تبقّع الأوراق - Cercospora):")
        print("- رش النبات بمبيد فطري وقائي مثل مبيدات تحتوي على النحاس أو البنزيميدازول.")
        print("- إزالة الأوراق المصابة فورًا ومنع تراكم بقايا النباتات حول الأشجار.")
        print("- تحسين التهوية وتقليل الرطوبة حول النباتات.")
        print("- تجنب الري بالرش والتركيز على الري الجذري.")
        print("- زراعة أصناف مقاومة للمرض إن أمكن.")
        self.halt()


    #عفن الساق
    @Rule(
        Symptom(name='إعوجاجات وتفحم في قاعدة الساق عند سطح التربة', cf=MATCH.cf1),
        Symptom(name='ظهور شبكة من الفطريات البيضاء وثم "جذور سوداء" (sclerotia)', cf=MATCH.cf2),
        Symptom(name='ذبول وموت مفاجئ للنبات حتى في الطقس المعتدل', cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60)
    ,
        salience=30
    )
    def sclerotium_rot_full_3(self, cf1, cf2, cf3):
        final = round(min(cf1, cf2, cf3) * 0.85)
        print(f"\n✅ التشخيص: مرض عفن الساق (Sclerotium Rot) (درجة الثقة: {final}/100)")
        self.declare(Fact(disease="عفن الساق"))

    @Rule(
        OR(
            AND(Symptom(name='إعوجاجات وتفحم في قاعدة الساق عند سطح التربة', cf=MATCH.cf1),
                Symptom(name='ظهور شبكة من الفطريات البيضاء وثم "جذور سوداء" (sclerotia)', cf=MATCH.cf2)),
            AND(Symptom(name='إعوجاجات وتفحم في قاعدة الساق عند سطح التربة', cf=MATCH.cf1),
                Symptom(name='ذبول وموت مفاجئ للنبات حتى في الطقس المعتدل', cf=MATCH.cf2)),
            AND(Symptom(name='ظهور شبكة من الفطريات البيضاء وثم "جذور سوداء" (sclerotia)', cf=MATCH.cf1),
                Symptom(name='ذبول وموت مفاجئ للنبات حتى في الطقس المعتدل', cf=MATCH.cf2))
        ),
        TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)
    ,
        salience=20
    )
    def sclerotium_rot_partial_strong(self, cf1, cf2):
        final = round(min(cf1, cf2) * 0.65)
        print(f"\n⚠️  تشخيص مبدئي: مرض عفن الساق (Sclerotium Rot) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتأكيد التشخيص.")
        self.declare(Fact(disease="عفن الساق"))

    @Rule(
        OR(
            Symptom(name='إعوجاجات وتفحم في قاعدة الساق عند سطح التربة', cf=MATCH.cf1),
            Symptom(name='ظهور شبكة من الفطريات البيضاء وثم "جذور سوداء" (sclerotia)', cf=MATCH.cf1),
            Symptom(name='ذبول وموت مفاجئ للنبات حتى في الطقس المعتدل', cf=MATCH.cf1)
        ),
        TEST(lambda cf1: cf1 >= 60)
    ,
        salience=10
    )
    def sclerotium_rot_weak(self, cf1):
        final = round(cf1 * 0.45)
        print(f"\n❗ احتمال ضعيف: مرض عفن الساق (Sclerotium Rot) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتحسين التشخيص.")
        self.declare(Fact(disease="عفن الساق"))

    @Rule(Fact(disease="عفن الساق"), salience=5)
    def sclerotium_rot_treatment(self):
        print("\n📌 المسبب: مرض عفن الساق في الباذنجان يُسببه الفطر Rhizoctonia solani.")
        print("\n💡 العلاج (مرض عفن الساق - Sclerotium Rot):")
        print("- إزالة وإتلاف النباتات المصابة فورًا (لا تُعاد كسماد).")
        print("- تعقيم التربة باستخدام البخار أو مبيدات الفطريات الوقائية.")
        print("- تحسين تصريف التربة وتقليل الرطوبة حول قاعدة النباتات.")
        print("- تجنب الزراعة الكثيفة وتحسين التهوية.")
        print("- استخدام أصناف مقاومة إن أمكن.")
        self.halt()