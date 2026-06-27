from experta import Rule, Fact, MATCH, TEST, OR, AND
from core import Symptom, PlantDiagnosisEngine

class PotatoRules(PlantDiagnosisEngine):

    #  اللفحة المتأخرة
    @Rule(
        Symptom(name='بقع مائية داكنة على الأوراق', cf=MATCH.cf1),
        Symptom(name='هالات خضراء إلى بنية على الساق', cf=MATCH.cf2),
        Symptom(name='تعفن بني على الدرنات', cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60)
    ,
        salience=30
    )
    def potato_late_blight_full(self, cf1, cf2, cf3):
        final = round(min(cf1, cf2, cf3) * 0.85)
        print(f"\n✅ التشخيص: اللفحة المتأخرة (درجة الثقة: {final}/100)")
        self.declare(Fact(disease="اللفحة المتأخرة"))

    @Rule(
        OR(
            AND(Symptom(name='بقع مائية داكنة على الأوراق', cf=MATCH.cf1), Symptom(name='هالات خضراء إلى بنية على الساق', cf=MATCH.cf2), TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name='بقع مائية داكنة على الأوراق', cf=MATCH.cf1), Symptom(name='تعفن بني على الدرنات', cf=MATCH.cf2), TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name='هالات خضراء إلى بنية على الساق', cf=MATCH.cf1), Symptom(name='تعفن بني على الدرنات', cf=MATCH.cf2), TEST(lambda cf1, cf2: min(cf1, cf2) >= 60))
        )
    ,
        salience=20
    )
    def potato_late_blight_partial(self, cf1=0, cf2=0):
        final = round(min(cf1, cf2) * 0.65)
        print(f"\n⚠️ تشخيص مبدئي: اللفحة المتأخرة (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتحسين التشخيص.")
        self.declare(Fact(disease="اللفحة المتأخرة"))

    @Rule(
        OR(
            Symptom(name='بقع مائية داكنة على الأوراق', cf=MATCH.cf1),
            Symptom(name='هالات خضراء إلى بنية على الساق', cf=MATCH.cf1),
            Symptom(name='تعفن بني على الدرنات', cf=MATCH.cf1)
        ),
        TEST(lambda cf1: cf1 >= 60)
    ,
        salience=10
    )
    def potato_late_blight_weak(self, cf1):
        final = round(cf1 * 0.45)
        print(f"\n❗ احتمال ضعيف: اللفحة المتأخرة (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتحسين التشخيص.")
        self.declare(Fact(disease="اللفحة المتأخرة"))

    @Rule(Fact(disease="اللفحة المتأخرة"), salience=5)
    def potato_late_blight_treatment(self):
        print("\n📌 المسبب: مرض اللفحة المتأخرة في البطاطا يُسببه الفطر Phytophthora infestans.")
        print("\n💡 العلاج (اللفحة المتأخرة - البطاطا):")
        print("- استخدام مبيد فطري مثل Mancozeb أو Cymoxanil")
        print("- رش عند بداية ظهور الأعراض مع تكرار كل 7-10 أيام")
        self.halt()





    #  فيروس PVY
    @Rule(
        Symptom(name='ورقة ناصعة اللون أو موزاييك مصفر', cf=MATCH.cf1),
        Symptom(name='تشوه أو تجعد الأوراق', cf=MATCH.cf2),
        Symptom(name='صغر حجم الدرنات', cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60)
    ,
        salience=30
    )
    def pvy_full(self, cf1, cf2, cf3):
        final = round(min(cf1, cf2, cf3) * 0.85)
        print(f"\n✅ التشخيص: فيروس PVY (درجة الثقة: {final}/100)")
        self.declare(Fact(disease="PVY"))

    @Rule(
        OR(
            AND(Symptom(name='ورقة ناصعة اللون أو موزاييك مصفر', cf=MATCH.cf1), Symptom(name='تشوه أو تجعد الأوراق', cf=MATCH.cf2), TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name='تشوه أو تجعد الأوراق', cf=MATCH.cf1), Symptom(name='صغر حجم الدرنات', cf=MATCH.cf2), TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name='ورقة ناصعة اللون أو موزاييك مصفر', cf=MATCH.cf1), Symptom(name='صغر حجم الدرنات', cf=MATCH.cf2), TEST(lambda cf1, cf2: min(cf1, cf2) >= 60))
        )
    ,
        salience=20
    )
    def pvy_partial(self, cf1=0, cf2=0):
        final = round(min(cf1, cf2) * 0.65)
        print(f"\n⚠️ تشخيص مبدئي: فيروس PVY (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتحسين التشخيص.")
        self.declare(Fact(disease="PVY"))

    @Rule(
        OR(
            Symptom(name='ورقة ناصعة اللون أو موزاييك مصفر', cf=MATCH.cf1),
            Symptom(name='تشوه أو تجعد الأوراق', cf=MATCH.cf1),
            Symptom(name='صغر حجم الدرنات', cf=MATCH.cf1)
        ),
        TEST(lambda cf1: cf1 >= 60)
    ,
        salience=10
    )
    def pvy_weak(self, cf1):
        final = round(cf1 * 0.45)
        print(f"\n❗ احتمال ضعيف: فيروس PVY (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتحسين التشخيص.")
        self.declare(Fact(disease="PVY"))

    @Rule(Fact(disease="PVY"), salience=5)
    def pvy_treatment(self):
        print("\n📌 المسبب: فيروس اللفحة العصوية للبطاطا (Potato Virus Y) - PVY")
        print("\n💡 العلاج (فيروس PVY - البطاطا):")
        print("- لا يوجد علاج مباشر، يفضل استخدام درنات خالية من الفيروس")
        print("- السيطرة على حشرات المن (ناقل رئيسي)")
        print("- التخلص من النباتات المصابة")
        self.halt()






    #  Black Scurf
    @Rule(
        Symptom(name='بقع سوداء صلبة على الدرنات', cf=MATCH.cf1),
        Symptom(name='آفات في الساق عند القاعدة', cf=MATCH.cf2),
        TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)
    ,
        salience=30
    )
    def black_scurf_full(self, cf1, cf2):
        final = round(min(cf1, cf2) * 0.85)
        print(f"\n✅ التشخيص: عفن القشرة السوداء (Black Scurf) (درجة الثقة: {final}/100)")
        self.declare(Fact(disease="Black Scurf"))

    @Rule(
        OR(
            Symptom(name='بقع سوداء صلبة على الدرنات', cf=MATCH.cf1),
            Symptom(name='آفات في الساق عند القاعدة', cf=MATCH.cf1)
        ),
        TEST(lambda cf1: cf1 >= 60)
    ,
        salience=10
    )
    def black_scurf_weak(self, cf1):
        final = round(cf1 * 0.45)
        print(f"\n❗ احتمال ضعيف: عفن القشرة السوداء (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتحسين التشخيص.")
        self.declare(Fact(disease="Black Scurf"))

    @Rule(Fact(disease="Black Scurf"), salience=5)
    def black_scurf_treatment(self):
        print("\n📌 المسبب: مرض القشرة السوداء (Black Scurf) في البطاطا يُسببه الفطر Rhizoctonia solani.")
        print("\n💡 العلاج (عفن القشرة السوداء - البطاطا):")
        print("- الزراعة في تربة جيدة التصريف وتغيير الدورة الزراعية")
        print("- معالجة الدرنات قبل الزراعة بمبيد مناسب مثل flutolanil")
        self.halt()





        # عفن القروح الجذري
        @Rule(
            Symptom(name='ظهور بثور صغيرة بيضاء أو بنية على الدرنات', cf=MATCH.cf1),
            Symptom(name='تشوه سطح الدرنات', cf=MATCH.cf2),
            Symptom(name='تندّب أو تقشير جلدي في منطقة القروح', cf=MATCH.cf3),
            TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60)
        ,
            salience=30
        )
        def powdery_scab_full(self, cf1, cf2, cf3):
            final = round(min(cf1, cf2, cf3) * 0.85)
            print(f"\n✅ التشخيص: عفن القروح الجذري (البطاطا) (درجة الثقة: {final}/100)")
            self.declare(Fact(disease="عفن القروح الجذري"))

        @Rule(
            OR(
                AND(Symptom(name='ظهور بثور صغيرة بيضاء أو بنية على الدرنات', cf=MATCH.cf1),
                    Symptom(name='تشوه سطح الدرنات', cf=MATCH.cf2),
                    TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
                AND(Symptom(name='تشوه سطح الدرنات', cf=MATCH.cf1),
                    Symptom(name='تندّب أو تقشير جلدي في منطقة القروح', cf=MATCH.cf2),
                    TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
                AND(Symptom(name='ظهور بثور صغيرة بيضاء أو بنية على الدرنات', cf=MATCH.cf1),
                    Symptom(name='تندّب أو تقشير جلدي في منطقة القروح', cf=MATCH.cf2),
                    TEST(lambda cf1, cf2: min(cf1, cf2) >= 60))
            )
        ,
            salience=20
        )
        def powdery_scab_partial(self, cf1=0, cf2=0):
            final = round(min(cf1, cf2) * 0.65)
            print(f"\n⚠️ تشخيص مبدئي: عفن القروح الجذري (البطاطا) (درجة الثقة: {final}/100)")
            print("⚠️ يُفضل إدخال المزيد من الأعراض لتحسين التشخيص.")
            self.declare(Fact(disease="عفن القروح الجذري"))

        @Rule(
            OR(
                Symptom(name='ظهور بثور صغيرة بيضاء أو بنية على الدرنات', cf=MATCH.cf1),
                Symptom(name='تشوه سطح الدرنات', cf=MATCH.cf1),
                Symptom(name='تندّب أو تقشير جلدي في منطقة القروح', cf=MATCH.cf1)
            ),
            TEST(lambda cf1: cf1 >= 60)
        ,
            salience=10
        )
        def powdery_scab_weak(self, cf1):
            final = round(cf1 * 0.45)
            print(f"\n❗ احتمال ضعيف: عفن القروح الجذري (البطاطا) (درجة الثقة: {final}/100)")
            print("⚠️ يُنصح بإدخال المزيد من الأعراض لتحسين دقة التشخيص.")
            self.declare(Fact(disease="عفن القروح الجذري"))

        @Rule(Fact(disease="عفن القروح الجذري"), salience=5)
        def powdery_scab_treatment(self):
            print(
                "\n📌 المسبب: مرض عفن القروح الجذري في البطاطا يُسببه الفطر Fusarium solani، وقد تشاركه فطريات أخرى مثل Rhizoctonia solani و Pythium spp.")
            print("\n💡 العلاج (عفن القروح الجذري - البطاطا):")
            print("- لا يوجد علاج فعال، لكن يمكن اتخاذ إجراءات وقائية:")
            print("- زراعة درنات خالية من الإصابة")
            print("- تجنّب التربة الثقيلة والرطبة")
            print("- تطبيق دورات زراعية وعدم زراعة البطاطا في نفس المكان لعدة مواسم")
            self.halt()