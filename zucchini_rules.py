from experta import Rule, Fact, MATCH, TEST, OR, AND
from core import Symptom, PlantDiagnosisEngine

class ZucchiniRules(PlantDiagnosisEngine):

    #فيروس موزاييك الكوسا
    @Rule(
        Symptom(name='فسيفساء (mosaic) وتبقع أصفر على الأوراق', cf=MATCH.cf1),
        Symptom(name='تشوه وتقزز أوراق الكوسا', cf=MATCH.cf2),
        Symptom(name='ثمار مشوّهة أو ملوّنة وغير منتظمة', cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60)
    ,
        salience=30
    )
    def zymv_full_3(self, cf1, cf2, cf3):
        final = round(min(cf1, cf2, cf3) * 0.85)
        print(f"\n✅ التشخيص: فيروس موزاييك الكوسا الأصفر (ZYMV) (درجة الثقة: {final}/100)")
        self.declare(Fact(disease="ZYMV"))



    @Rule(
        OR(
            AND(Symptom(name='فسيفساء (mosaic) وتبقع أصفر على الأوراق', cf=MATCH.cf1),
                Symptom(name='تشوه وتقزز أوراق الكوسا', cf=MATCH.cf2)),
            AND(Symptom(name='فسيفساء (mosaic) وتبقع أصفر على الأوراق', cf=MATCH.cf1),
                Symptom(name='ثمار مشوّهة أو ملوّنة وغير منتظمة', cf=MATCH.cf2)),
            AND(Symptom(name='تشوه وتقزز أوراق الكوسا', cf=MATCH.cf1),
                Symptom(name='ثمار مشوّهة أو ملوّنة وغير منتظمة', cf=MATCH.cf2))
        ),
        TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)
    ,
        salience=20
    )
    def zymv_partial_strong(self, cf1, cf2):
        final = round(min(cf1, cf2) * 0.65)
        print(f"\n⚠️  تشخيص مبدئي: فيروس موزاييك الكوسا الأصفر (ZYMV) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتأكيد التشخيص.")
        self.declare(Fact(disease="ZYMV"))


    @Rule(
        OR(
            Symptom(name='فسيفساء (mosaic) وتبقع أصفر على الأوراق', cf=MATCH.cf1),
            Symptom(name='تشوه وتقزز أوراق الكوسا', cf=MATCH.cf1),
            Symptom(name='ثمار مشوّهة أو ملوّنة وغير منتظمة', cf=MATCH.cf1)
        ),
        TEST(lambda cf1: cf1 >= 60)
    ,
        salience=10
    )
    def zymv_weak(self, cf1):
        final = round(cf1 * 0.45)
        print(f"\n❗ احتمال ضعيف: فيروس موزاييك الكوسا الأصفر (ZYMV) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتحسين التشخيص.")
        self.declare(Fact(disease="ZYMV"))


    @Rule(Fact(disease="ZYMV"), salience=5)
    def zymv_treatment(self):
        print("\n📌 المسبب: فيروس موزاييك الكوسا (Zucchini Yellow Mosaic Virus) - ZYMV")
        print("\n💡 العلاج (فيروس موزاييك الكوسا الأصفر - ZYMV):")
        print("- إزالة وإتلاف النباتات المصابة فورًا.")
        print("- مكافحة الحشرات الناقلة (خاصة المن) بمبيدات حشرية.")
        print("- استخدام أصناف مقاومة أو مطعّمة.")
        print("- تجنب زراعة الكوسا بالقرب من المحاصيل المصابة.")
        print("- استخدام بذور خالية من الفيروس.")
        self.halt()




    #البياض البودري

    @Rule(
        Symptom(name='مسحوق أبيض رمادي يغطي السطح العلوي أو السفلي للأوراق', cf=MATCH.cf1),
        Symptom(name='اصفرار وتجعيد الأوراق مسبقًا', cf=MATCH.cf2),
        Symptom(name='تباطؤ نمو النبات وجفاف الأوراق المتقدمة', cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60)
    ,
        salience=30
    )
    def powdery_mildew_full_3(self, cf1, cf2, cf3):
        final = round(min(cf1, cf2, cf3) * 0.85)
        print(f"\n✅ التشخيص: مرض البياض البودري (درجة الثقة: {final}/100)")
        self.declare(Fact(disease="البياض البودري"))


    @Rule(
        OR(
            AND(Symptom(name='مسحوق أبيض رمادي يغطي السطح العلوي أو السفلي للأوراق', cf=MATCH.cf1),
                Symptom(name='اصفرار وتجعيد الأوراق مسبقًا', cf=MATCH.cf2)),
            AND(Symptom(name='مسحوق أبيض رمادي يغطي السطح العلوي أو السفلي للأوراق', cf=MATCH.cf1),
                Symptom(name='تباطؤ نمو النبات وجفاف الأوراق المتقدمة', cf=MATCH.cf2)),
            AND(Symptom(name='اصفرار وتجعيد الأوراق مسبقًا', cf=MATCH.cf1),
                Symptom(name='تباطؤ نمو النبات وجفاف الأوراق المتقدمة', cf=MATCH.cf2))
        ),
        TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)
    ,
        salience=20
    )
    def powdery_mildew_partial_strong(self, cf1, cf2):
        final = round(min(cf1, cf2) * 0.65)
        print(f"\n⚠️  تشخيص مبدئي: مرض البياض البودري (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتأكيد التشخيص.")
        self.declare(Fact(disease="البياض البودري"))


    @Rule(
        OR(
            Symptom(name='مسحوق أبيض رمادي يغطي السطح العلوي أو السفلي للأوراق', cf=MATCH.cf1),
            Symptom(name='اصفرار وتجعيد الأوراق مسبقًا', cf=MATCH.cf1),
            Symptom(name='تباطؤ نمو النبات وجفاف الأوراق المتقدمة', cf=MATCH.cf1)
        ),
        TEST(lambda cf1: cf1 >= 60)
    ,
        salience=10
    )
    def powdery_mildew_weak(self, cf1):
        final = round(cf1 * 0.45)
        print(f"\n❗ احتمال ضعيف: مرض البياض البودري (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتحسين التشخيص.")
        self.declare(Fact(disease="البياض البودري"))


    @Rule(Fact(disease="البياض البودري"), salience=5)
    def powdery_mildew_treatment(self):
        print("\n📌 المسبب: مرض البياض البودري في الكوسا يُسببه الفطر Podosphaera xanthii.")
        print("\n💡 العلاج (مرض البياض البودري):")
        print("- رش النبات بمبيد فطري مخصص للبياض البودري (مثل الكبريت الميكروني أو محلول بوردو).")
        print("- تحسين التهوية وتقليل الرطوبة داخل البيوت المحمية.")
        print("- إزالة الأوراق المصابة فورًا ومنع تراكم بقايا النباتات.")
        print("- تجنب الري بالرش ويفضل الري الجذري.")
        print("- زراعة أصناف مقاومة للمرض.")
        self.halt()




    #الذبول البكتيري
    @Rule(
        Symptom(name='ذبول فوري للنبات بدون اصفرار سابق', cf=MATCH.cf1),
        Symptom(name='أوراق قد تتحوّل إلى لون أخضر داكن ممل أو باهت', cf=MATCH.cf2),
        Symptom(name='سوائل مخاطية على جذع النبات عند القطع', cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60)
    ,
        salience=30
    )
    def bacterial_wilt_full_3(self, cf1, cf2, cf3):
        final = round(min(cf1, cf2, cf3) * 0.85)
        print(f"\n✅ التشخيص: مرض الذبول البكتيري (درجة الثقة: {final}/100)")
        self.declare(Fact(disease="الذبول البكتيري"))


    @Rule(
        OR(
            AND(Symptom(name='ذبول فوري للنبات بدون اصفرار سابق', cf=MATCH.cf1),
                Symptom(name='أوراق قد تتحوّل إلى لون أخضر داكن ممل أو باهت', cf=MATCH.cf2)),
            AND(Symptom(name='ذبول فوري للنبات بدون اصفرار سابق', cf=MATCH.cf1),
                Symptom(name='سوائل مخاطية على جذع النبات عند القطع', cf=MATCH.cf2)),
            AND(Symptom(name='أوراق قد تتحوّل إلى لون أخضر داكن ممل أو باهت', cf=MATCH.cf1),
                Symptom(name='سوائل مخاطية على جذع النبات عند القطع', cf=MATCH.cf2))
        ),
        TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)
    ,
        salience=20
    )
    def bacterial_wilt_partial_strong(self, cf1, cf2):
        final = round(min(cf1, cf2) * 0.65)
        print(f"\n⚠️  تشخيص مبدئي: مرض الذبول البكتيري (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتأكيد التشخيص.")
        self.declare(Fact(disease="الذبول البكتيري"))



    @Rule(
        OR(
            Symptom(name='ذبول فوري للنبات بدون اصفرار سابق', cf=MATCH.cf1),
            Symptom(name='أوراق قد تتحوّل إلى لون أخضر داكن ممل أو باهت', cf=MATCH.cf1),
            Symptom(name='سوائل مخاطية على جذع النبات عند القطع', cf=MATCH.cf1)
        ),
        TEST(lambda cf1: cf1 >= 60)
    ,
        salience=10
    )
    def zucchini_bacterial_wilt_weak(self, cf1):
        final = round(cf1 * 0.45)
        print(f"\n❗ احتمال ضعيف: مرض الذبول البكتيري (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتحسين التشخيص.")
        self.declare(Fact(disease="الذبول البكتيري"))


    @Rule(Fact(disease="الذبول البكتيري"), salience=5)
    def zucchini_bacterial_wilt_treatment(self):
        print(
            "\n📌 المسبب: مرض الذبول البكتيري في الكوسا يُسببه البكتيريا Erwinia tracheiphila")
        print("\n💡 العلاج (مرض الذبول البكتيري):")
        print("- إزالة النباتات المصابة فورًا والتخلص منها (لا تُعيد استخدامها كسماد).")
        print("- تعقيم أدوات الزراعة بعد كل استخدام.")
        print("- مكافحة الخنافس (خاصة خنفساء الخيار) الناقلة للبكتيريا باستخدام مبيدات حشرية.")
        print("- تجنب زراعة الكوسا في نفس التربة التي سبق إصابة نباتات فيها بالمرض.")
        print("- لا توجد علاج كيميائي فعّال، لذا يُركز على الوقاية فقط.")
        self.halt()



    #عفن الجذع اللزج

    @Rule(
        Symptom(name='بقع دائرية مائية على الأوراق', cf=MATCH.cf1),
        Symptom(name='تقرحات وسوائل بنية/لزجة تنطلق من الساق', cf=MATCH.cf2),
        Symptom(name='تعفن الثمار أو صدأ على الثمار', cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60)
    ,
        salience=30
    )
    def gummy_stem_blight_full_3(self, cf1, cf2, cf3):
        final = round(min(cf1, cf2, cf3) * 0.85)
        print(f"\n✅ التشخيص: مرض عفن الجذع اللزج (درجة الثقة: {final}/100)")
        self.declare(Fact(disease="عفن الجذع اللزج"))


    @Rule(
        OR(
            AND(Symptom(name='بقع دائرية مائية على الأوراق', cf=MATCH.cf1),
                Symptom(name='تقرحات وسوائل بنية/لزجة تنطلق من الساق', cf=MATCH.cf2)),
            AND(Symptom(name='بقع دائرية مائية على الأوراق', cf=MATCH.cf1),
                Symptom(name='تعفن الثمار أو صدأ على الثمار', cf=MATCH.cf2)),
            AND(Symptom(name='تقرحات وسوائل بنية/لزجة تنطلق من الساق', cf=MATCH.cf1),
                Symptom(name='تعفن الثمار أو صدأ على الثمار', cf=MATCH.cf2))
        ),
        TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)
    ,
        salience=20
    )
    def gummy_stem_blight_partial_strong(self, cf1, cf2):
        final = round(min(cf1, cf2) * 0.65)
        print(f"\n⚠️  تشخيص مبدئي: مرض عفن الجذع اللزج (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتأكيد التشخيص.")
        self.declare(Fact(disease="عفن الجذع اللزج"))


    @Rule(
        OR(
            Symptom(name='بقع دائرية مائية على الأوراق', cf=MATCH.cf1),
            Symptom(name='تقرحات وسوائل بنية/لزجة تنطلق من الساق', cf=MATCH.cf1),
            Symptom(name='تعفن الثمار أو صدأ على الثمار', cf=MATCH.cf1)
        ),
        TEST(lambda cf1: cf1 >= 60)
    ,
        salience=10
    )
    def gummy_stem_blight_weak(self, cf1):
        final = round(cf1 * 0.45)
        print(f"\n❗ احتمال ضعيف: مرض عفن الجذع اللزج (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتحسين التشخيص.")
        self.declare(Fact(disease="عفن الجذع اللزج"))


    @Rule(Fact(disease="عفن الجذع اللزج"), salience=5)
    def gummy_stem_blight_treatment(self):
        print("\n📌 المسبب: مرض عفن الجذع اللزج في الكوسا يُسببه البكتيريا Pectobacterium carotovorum")
        print("\n💡 العلاج (مرض عفن الجذع اللزج):")
        print("- رش النبات بمبيد فطري وقائي مثل مبيدات النحاس أو البنزيميدازول.")
        print("- إزالة وإتلاف الأجزاء المصابة فورًا.")
        print("- تجنب الري بالرش لتفادي زيادة الرطوبة والانتشار.")
        print("- تعقيم أدوات العمل بين النباتات.")
        print("- تجنب الزراعة الكثيفة وتحسين التهوية بين النباتات.")
        self.halt()