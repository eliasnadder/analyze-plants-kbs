from experta import Rule, Fact, MATCH, TEST, OR, AND
from core import Symptom, PlantDiagnosisEngine

class CitrusRules(PlantDiagnosisEngine):

    #   مرض مالسيكو
    @Rule(
        Symptom(name='اصفرار وتمدد للأوراق والشعيرات الخشبية', cf=MATCH.cf1),
        Symptom(name='ذبول وفناء أجزاء من الفروع', cf=MATCH.cf2),
        Symptom(name='إفرازات صمغية وردية أو رمادية في الجذوع', cf=MATCH.cf3),
        Symptom(name='بقع داكنة أو تكاثف للنسيج الخشبي تحت اللحاء', cf=MATCH.cf4),
        TEST(lambda cf1, cf2, cf3, cf4: min(cf1, cf2, cf3, cf4) >= 60)
    ,
        salience=30
    )
    def mal_secco_full_4(self, cf1, cf2, cf3, cf4):
        final = round(min(cf1, cf2, cf3, cf4) * 0.9)
        print(f"\n✅ التشخيص: مرض مالسيكو (الحمضيات) (درجة الثقة: {final}/100)")
        self.declare(Fact(disease="مالسيكو"))

    @Rule(
        OR(
            AND(Symptom(name='اصفرار وتمدد للأوراق والشعيرات الخشبية', cf=MATCH.cf1),
                Symptom(name='ذبول وفناء أجزاء من الفروع', cf=MATCH.cf2),
                Symptom(name='إفرازات صمغية وردية أو رمادية في الجذوع', cf=MATCH.cf3)),
            AND(Symptom(name='ذبول وفناء أجزاء من الفروع', cf=MATCH.cf1),
                Symptom(name='إفرازات صمغية وردية أو رمادية في الجذوع', cf=MATCH.cf2),
                Symptom(name='بقع داكنة أو تكاثف للنسيج الخشبي تحت اللحاء', cf=MATCH.cf3)),
            AND(Symptom(name='اصفرار وتمدد للأوراق والشعيرات الخشبية', cf=MATCH.cf1),
                Symptom(name='إفرازات صمغية وردية أو رمادية في الجذوع', cf=MATCH.cf2),
                Symptom(name='بقع داكنة أو تكاثف للنسيج الخشبي تحت اللحاء', cf=MATCH.cf3)),
            AND(Symptom(name='اصفرار وتمدد للأوراق والشعيرات الخشبية', cf=MATCH.cf1),
                Symptom(name='ذبول وفناء أجزاء من الفروع', cf=MATCH.cf2),
                Symptom(name='بقع داكنة أو تكاثف للنسيج الخشبي تحت اللحاء', cf=MATCH.cf3))
        ),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60)
    ,
        salience=20
    )
    def mal_secco_partial_strong(self, cf1, cf2, cf3):
        final = round(min(cf1, cf2, cf3) * 0.8)
        print(f"\n⚠️ تشخيص مؤكد جزئيًا: مرض مالسيكو (الحمضيات) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتأكيد التشخيص.")
        self.declare(Fact(disease="مالسيكو"))

    @Rule(
        OR(
            AND(Symptom(name='اصفرار وتمدد للأوراق والشعيرات الخشبية', cf=MATCH.cf1),
                Symptom(name='ذبول وفناء أجزاء من الفروع', cf=MATCH.cf2)),
            AND(Symptom(name='إفرازات صمغية وردية أو رمادية في الجذوع', cf=MATCH.cf1),
                Symptom(name='بقع داكنة أو تكاثف للنسيج الخشبي تحت اللحاء', cf=MATCH.cf2)),
            AND(Symptom(name='اصفرار وتمدد للأوراق والشعيرات الخشبية', cf=MATCH.cf1),
                Symptom(name='بقع داكنة أو تكاثف للنسيج الخشبي تحت اللحاء', cf=MATCH.cf2)),
        ),
        TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)
    ,
        salience=20
    )
    def mal_secco_partial_basic(self, cf1, cf2):
        final = round(min(cf1, cf2) * 0.6)
        print(f"\n⚠️ تشخيص مبدئي: مرض مالسيكو (الحمضيات) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتأكيد التشخيص.")
        self.declare(Fact(disease="مالسيكو"))

    @Rule(
        OR(
            Symptom(name='اصفرار وتمدد للأوراق والشعيرات الخشبية', cf=MATCH.cf1),
            Symptom(name='ذبول وفناء أجزاء من الفروع', cf=MATCH.cf1),
            Symptom(name='إفرازات صمغية وردية أو رمادية في الجذوع', cf=MATCH.cf1),
            Symptom(name='بقع داكنة أو تكاثف للنسيج الخشبي تحت اللحاء', cf=MATCH.cf1)
        ),
        TEST(lambda cf1: cf1 >= 60)
    ,
        salience=10
    )
    def mal_secco_weak(self, cf1):
        final = round(cf1 * 0.5)
        print(f"\n❗ احتمال ضعيف: مرض مالسيكو (الحمضيات) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتأكيد التشخيص.")
        self.declare(Fact(disease="مالسيكو"))

    @Rule(Fact(disease="مالسيكو"), salience=5)
    def mal_secco_treatment(self):
        print("\n📌 المسبب: مرض مالسيكو في الحمضيات يُسببه الفطر Plenodomus tracheiphilus.")
        print("\n💡 العلاج (مرض مالسيكو - الحمضيات):")
        print("- تقليم الأفرع المصابة فورًا والتخلص منها بالحرق.")
        print("- تطهير أدوات التقليم لمنع الانتشار.")
        print("- رش مبيد فطري نحاسي بعد التقليم.")
        print("- زراعة أصناف مقاومة وتحسين صرف التربة.")
        self.halt()


    #عفن الجذور
    @Rule(
        Symptom(name='إفرازات صمغية سوداء أو بنية عند قاعدة الجذع', cf=MATCH.cf1),
        Symptom(name='تقرحات أو تصدعات في اللحاء بالقرب من سطح التربة', cf=MATCH.cf2),
        Symptom(name='ذبول الأصناف وضعف نمو الأوراق', cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60)
    ,
        salience=30
    )
    def gummosis_full_3(self, cf1, cf2, cf3):
        final = round(min(cf1, cf2, cf3) * 0.85)
        print(f"\n✅ التشخيص: مرض عفن الجذور / الصمغ (درجة الثقة: {final}/100)")
        self.declare(Fact(disease="عفن الجذور والصمغ"))

    @Rule(
        OR(
            AND(Symptom(name='إفرازات صمغية سوداء أو بنية عند قاعدة الجذع', cf=MATCH.cf1),
                Symptom(name='تقرحات أو تصدعات في اللحاء بالقرب من سطح التربة', cf=MATCH.cf2)),
            AND(Symptom(name='إفرازات صمغية سوداء أو بنية عند قاعدة الجذع', cf=MATCH.cf1),
                Symptom(name='ذبول الأصناف وضعف نمو الأورقات', cf=MATCH.cf2)),
            AND(Symptom(name='تقرحات أو تصدعات في اللحاء بالقرب من سطح التربة', cf=MATCH.cf1),
                Symptom(name='ذبول الأصناف وضعف نمو الأورقات', cf=MATCH.cf2))
        ),
        TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)
    ,
        salience=20
    )
    def gummosis_partial_strong(self, cf1, cf2):
        final = round(min(cf1, cf2) * 0.65)
        print(f"\n⚠️ تشخيص مبدئي : مرض عفن الجذور / الصمغ (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتأكيد التشخيص.")
        self.declare(Fact(disease="عفن الجذور والصمغ"))

    @Rule(
        OR(
            Symptom(name='إفرازات صمغية سوداء أو بنية عند قاعدة الجذع', cf=MATCH.cf1),
            Symptom(name='تقرحات أو تصدعات في اللحاء بالقرب من سطح التربة', cf=MATCH.cf1),
            Symptom(name='ذبول الأصناف وضعف نمو الأورقات', cf=MATCH.cf1)
        ),
        TEST(lambda cf1: cf1 >= 60)
    ,
        salience=10
    )
    def gummosis_weak(self, cf1):
        final = round(cf1 * 0.45)
        print(f"\n❗ احتمال ضعيف: مرض عفن الجذور / الصمغ (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتأكيد التشخيص.")
        self.declare(Fact(disease="عفن الجذور والصمغ"))

    @Rule(Fact(disease="عفن الجذور والصمغ"), salience=5)
    def gummosis_treatment(self):
        print("\n📌 المسبب: مرض عفن الجذور في الحمضيات يُسببه الفطر Phytophthora spp.")
        print("\n💡 العلاج (مرض عفن الجذور / الصمغ - الحمضيات):")
        print("- تحسين تصريف التربة وتقليل الري.")
        print("- رش أو تطهير الجذوع بمبيدات فطرية مضادة لـ Phytophthora (مثل فوندازول).")
        print("- معالجة التربة بمبيد فطري عند الزراعة.")
        print("- زراعة أشجار على تلال مرتفعة لتقليل تجمع المياه.")
        print("- التخلص من الأشجار الشديدة الإصابة.")
        self.halt()


    #فيروس ترايستيزا
    @Rule(
        Symptom(name='اختناق النسيج الوعائي وموت الفروع', cf=MATCH.cf1),
        Symptom(name='تجعد أو تساقط الأوراق', cf=MATCH.cf2),
        Symptom(name='ضعف في النمو، وقلة الإنتاجية', cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60)
    ,
        salience=30
    )
    def tristeza_full_3(self, cf1, cf2, cf3):
        final = round(min(cf1, cf2, cf3) * 0.85)
        print(f"\n✅ التشخيص: مرض ترايستيزا الفيروسي (درجة الثقة: {final}/100)")
        self.declare(Fact(disease="ترايستيزا"))

    @Rule(
        OR(
            AND(Symptom(name='اختناق النسيج الوعائي وموت الفروع', cf=MATCH.cf1),
                Symptom(name='تجعد أو تساقط الأوراق', cf=MATCH.cf2)),
            AND(Symptom(name='اختناق النسيج الوعائي وموت الفروع', cf=MATCH.cf1),
                Symptom(name='ضعف في النمو، وقلة الإنتاجية', cf=MATCH.cf2)),
            AND(Symptom(name='تجعد أو تساقط الأوراق', cf=MATCH.cf1),
                Symptom(name='ضعف في النمو، وقلة الإنتاجية', cf=MATCH.cf2))
        ),
        TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)
    ,
        salience=20
    )
    def tristeza_partial_strong(self, cf1, cf2):
        final = round(min(cf1, cf2) * 0.65)
        print(f"\n⚠️  تشخيص مبدئي: مرض ترايستيزا الفيروسي (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتأكيد التشخيص.")
        self.declare(Fact(disease="ترايستيزا"))

    @Rule(
        OR(
            Symptom(name='اختناق النسيج الوعائي وموت الفروع', cf=MATCH.cf1),
            Symptom(name='تجعد أو تساقط الأوراق', cf=MATCH.cf1),
            Symptom(name='ضعف في النمو، وقلة الإنتاجية', cf=MATCH.cf1)
        ),
        TEST(lambda cf1: cf1 >= 60),
        salience=10,
    )
    def tristeza_weak(self, cf1):
        final = round(cf1 * 0.45)
        print(f"\n❗ احتمال ضعيف: مرض ترايستيزا الفيروسي (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتحسين التشخيص بسبب التشابه مع مرض اخر ")
        self.declare(Fact(disease="ترايستيزا"))

    @Rule(Fact(disease="ترايستيزا"), salience=5)
    def tristeza_treatment(self):
        print("\n📌 المسبب: فيروس ترايستيزا (Citrus Tristeza Virus) - CTV")
        print("\n💡 العلاج (مرض ترايستيزا الفيروسي - الحمضيات):")
        print("- زراعة أصناف مقاومة للفيروس.")
        print("- مكافحة حشرات المن ناقل الفيروس باستخدام مبيدات حشرية.")
        print("- إزالة الأشجار المصابة فورًا ومنع انتشارها.")
        print("- استخدام تطعيمات خالية من الفيروس عند الزراعة الجديدة.")
        print("- تعقيم أدوات العمل بين الأشجار.")
        self.halt()


    #التبقع الأسود
    @Rule(
        Symptom(name='بقع داكنة غائرة على الثمار', cf=MATCH.cf1),
        Symptom(name='تساقط مبكر للثمار', cf=MATCH.cf2),
        Symptom(name='بقع صغيرة على الأوراق في بعض الحالات', cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60)
    ,
        salience=30
    )
    def black_spot_full_3(self, cf1, cf2, cf3):
        final = round(min(cf1, cf2, cf3) * 0.85)
        print(f"\n✅ التشخيص: مرض التبقّع الأسود (درجة الثقة: {final}/100)")
        self.declare(Fact(disease="التبقّع الأسود"))

    @Rule(
        OR(
            AND(Symptom(name='بقع داكنة غائرة على الثمار', cf=MATCH.cf1),
                Symptom(name='تساقط مبكر للثمار', cf=MATCH.cf2)),
            AND(Symptom(name='بقع داكنة غائرة على الثمار', cf=MATCH.cf1),
                Symptom(name='بقع صغيرة على الأوراق في بعض الحالات', cf=MATCH.cf2)),
            AND(Symptom(name='تساقط مبكر للثمار', cf=MATCH.cf1),
                Symptom(name='بقع صغيرة على الأوراق في بعض الحالات', cf=MATCH.cf2))
        ),
        TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)
    ,
        salience=20
    )
    def black_spot_partial_strong(self, cf1, cf2):
        final = round(min(cf1, cf2) * 0.65)
        print(f"\n⚠️ تشخيص مبدئي: مرض التبقّع الأسود (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتأكيد التشخيص.")
        self.declare(Fact(disease="التبقّع الأسود"))

    @Rule(
        OR(
            Symptom(name='بقع داكنة غائرة على الثمار', cf=MATCH.cf1),
            Symptom(name='تساقط مبكر للثمار', cf=MATCH.cf1),
            Symptom(name='بقع صغيرة على الأوراق في بعض الحالات', cf=MATCH.cf1)
        ),
        TEST(lambda cf1: cf1 >= 60)
    ,
        salience=10
    )
    def black_spot_weak(self, cf1):
        final = round(cf1 * 0.45)
        print(f"\n❗ احتمال ضعيف: مرض التبقّع الأسود (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتحسين التشخيص.")
        self.declare(Fact(disease="التبقّع الأسود"))

    @Rule(Fact(disease="التبقّع الأسود"), salience=5)
    def black_spot_treatment(self):
        print("\n📌 المسبب: مرض التبقّع الأسود في الحمضيات يُسببه البكتيريا Xanthomonas citri subsp. citri.")
        print("\n💡 العلاج (مرض التبقّع الأسود - الحمضيات):")
        print("- رش الأشجار بمبيدات فطرية تحتوي على النحاس (مثل بوردو ميكس).")
        print("- تقليم الأفرع المصابة وإزالة الثمار الساقطة والتالفة.")
        print("- تحسين التهوية بين الأشجار وتقليل الرطوبة.")
        print("- مراقبة البؤر المرضية والحد من انتشارها.")
        print("- زراعة أصناف مقاومة إن أمكن.")
        self.halt()


    #الحصف البكتيري
    @Rule(
        Symptom(name='تقرحات مائية على الأوراق والسيقان والثمار', cf=MATCH.cf1),
        Symptom(name='يحيط بها هالة صفراء', cf=MATCH.cf2),
        TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)
    ,
        salience=30
    )
    def bacterial_canker_full(self, cf1, cf2):
        final = round(min(cf1, cf2) * 0.7)
        print(f"\n✅ التشخيص: مرض الحصف البكتيري (درجة الثقة: {final}/100)")
        self.declare(Fact(disease="الحصف البكتيري"))

    @Rule(
        OR(
            Symptom(name='تقرحات مائية على الأوراق والسيقان والثمار', cf=MATCH.cf1),
            Symptom(name='يحيط بها هالة صفراء', cf=MATCH.cf1)
        ),
        TEST(lambda cf1: cf1 >= 60)
    ,
        salience=10
    )
    def bacterial_canker_weak(self, cf1):
        final = round(cf1 * 0.4)
        print(f"\n❗ احتمال ضعيف: مرض الحصف البكتيري (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتحسين التشخيص.")
        self.declare(Fact(disease="الحصف البكتيري"))

    @Rule(Fact(disease="الحصف البكتيري"), salience=5)
    def bacterial_canker_treatment(self):
        print("\n📌 المسبب: مرض الحصف البكتيري في الحمضيات يُسببه البكتيريا Xanthomonas citri subsp. citri.")
        print("\n💡 العلاج (مرض الحصف البكتيري - الحمضيات):")
        print("- إزالة وتدمير الأجزاء المصابة بالمرض (حرق أو دفن عميق).")
        print("- رش الأشجار بمحلول نحاسي (مثل أوكسي كلوريد النحاس أو بوردو ميكس).")
        print("- تقليم الأشجار لتحسين التهوية وتقليل الرطوبة.")
        print("- منع انتقال البكتيريا عبر المياه أو أدوات التقليم دون تعقيم.")
        print("- زراعة أصناف مقاومة للمرض إن أمكن.")
        self.halt()


    #البقعة الدهنية
    @Rule(
        Symptom(name='بقع صفراء-بنية لامعة على السطح السفلي للأوراق', cf=MATCH.cf1),
        Symptom(name='تجعد أو تساقط الأوراق', cf=MATCH.cf2),
        TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)
    ,
        salience=30
    )
    def greasy_spot_full(self, cf1, cf2):
        final = round(min(cf1, cf2) * 0.7)
        print(f"\n✅ التشخيص: مرض البقعة الدهنية (درجة الثقة: {final}/100)")
        self.declare(Fact(disease="البقعة الدهنية"))

    @Rule(
        OR(
            Symptom(name='بقع صفراء-بنية لامعة على السطح السفلي للأوراق', cf=MATCH.cf1),
            Symptom(name='تجعد أو تساقط الأوراق', cf=MATCH.cf1)
        ),
        TEST(lambda cf1: cf1 >= 60),
        salience=10,
    )
    def greasy_spot_weak(self, cf1):
        final = round(cf1 * 0.4)
        print(f"\n❗ احتمال ضعيف: مرض البقعة الدهنية (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتحسين التشخيص بسبب التشابه مع مرض اخر")
        self.declare(Fact(disease="البقعة الدهنية"))

    @Rule(Fact(disease="البقعة الدهنية"), salience=5)
    def greasy_spot_treatment(self):
        print("\n📌 المسبب: مرض البقعة الدهنية في الحمضيات يُسببه الفطر Alternaria citri أو Alternaria alternata.")
        print("\n💡 العلاج (مرض البقعة الدهنية - الحمضيات):")
        print("- رش الأشجار بمبيد فطري نحاسي أو مبيد يحتوي على الكبريت.")
        print("- تقليم الأوراق المصابة وإزالة بقايا الأوراق الساقطة من حول الشجرة.")
        print("- تحسين التهوية بين الأشجار وتقليل الرطوبة.")
        print("- تكرار الرش الوقائي خاصة في فترات الرطوبة العالية.")
        self.halt()