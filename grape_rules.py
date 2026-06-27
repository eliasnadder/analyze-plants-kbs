from experta import Rule, Fact, MATCH, TEST, OR, AND
from core import Symptom, PlantDiagnosisEngine

class GrapeRules(PlantDiagnosisEngine):

    #البياض الزغبي
    @Rule(
        Symptom(name='بقع صفراء على الأوراق', cf=MATCH.cf1),
        Symptom(name='نمو أبيض قطني تحت الأوراق', cf=MATCH.cf2),
        Symptom(name='ذبول الأوراق وسقوطها', cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60),

    )
    def downy_mildew_full(self, cf1, cf2, cf3):
        final = round(min(cf1, cf2, cf3) * 0.85)
        print(f"\n✅ التشخيص: البياض الزغبي (العنب) (درجة الثقة: {final}/100)")
        self.declare(Fact(disease="البياض الزغبي"))

    @Rule(
        OR(
            AND(Symptom(name='بقع صفراء على الأوراق', cf=MATCH.cf1),
                Symptom(name='نمو أبيض قطني تحت الأوراق', cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name='بقع صفراء على الأوراق', cf=MATCH.cf1),
                Symptom(name='ذبول الأوراق وسقوطها', cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name='نمو أبيض قطني تحت الأوراق', cf=MATCH.cf1),
                Symptom(name='ذبول الأوراق وسقوطها', cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),

        ),
        salience=11

    )
    def downy_mildew_partial(self, cf1=0, cf2=0):
        final = round(min(cf1, cf2) * 0.65)
        print(f"\n⚠️ تشخيص مبدئي: البياض الزغبي (العنب) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتحسين التشخيص بسبب التشابه مع مرض اخر")
        self.declare(Fact(disease="البياض الزغبي"))
        self.halt()



    @Rule(
        OR(
            Symptom(name='بقع صفراء على الأوراق', cf=MATCH.cf1),
            Symptom(name='نمو أبيض قطني تحت الأوراق', cf=MATCH.cf1),
            Symptom(name='ذبول الأوراق وسقوطها', cf=MATCH.cf1)
        ),
        TEST(lambda cf1: cf1 >= 60),
        salience=10

    )
    def downy_mildew_weak(self, cf1):
        final = round(cf1 * 0.45)
        print(f"\n❗ احتمال ضعيف: البياض الزغبي (العنب) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتحسين التشخيص بسبب التشابه مع مرض اخر")
        self.declare(Fact(disease="البياض الزغبي"))
        self.halt()


    @Rule(Fact(disease="البياض الزغبي"))
    def downy_mildew_treatment(self):
        print("\n📌 المسبب: مرض البياض الزغبي في العنب يُسببه الفطر Plasmopara viticola.")
        print("\n💡 العلاج (البياض الزغبي - العنب):")
        print("- رش مبيد فطري يحتوي على Metalaxyl أو Mancozeb")
        print("- تكرار الرش كل 7–10 أيام حسب الظروف الجوية")
        print("- تحسين التهوية والتخلص من الأجزاء المصابة")
        self.halt()



    #  العفن الرمادي
    @Rule(
        Symptom(name='بقع رمادية على العناقيد', cf=MATCH.cf1),
        Symptom(name='تعفن طري على الثمار', cf=MATCH.cf2),
        Symptom(name='وجود زغب رمادي اللون', cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60)
    )
    def gray_mold_full(self, cf1, cf2, cf3):
        final = round(min(cf1, cf2, cf3) * 0.85)
        print(f"\n✅ التشخيص: العفن الرمادي (العنب) (درجة الثقة: {final}/100)")
        self.declare(Fact(disease="العفن الرمادي"))

    @Rule(
        OR(
            AND(Symptom(name='بقع رمادية على العناقيد', cf=MATCH.cf1),
                Symptom(name='تعفن طري على الثمار', cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name='بقع رمادية على العناقيد', cf=MATCH.cf1),
                Symptom(name='وجود زغب رمادي اللون', cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name='تعفن طري على الثمار', cf=MATCH.cf1),
                Symptom(name='وجود زغب رمادي اللون', cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60))
        )
    )
    def gray_mold_partial(self, cf1=0, cf2=0):
        final = round(min(cf1, cf2) * 0.65)
        print(f"\n⚠️ تشخيص مبدئي: العفن الرمادي (العنب) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتحسين التشخيص.")
        self.declare(Fact(disease="العفن الرمادي"))

    @Rule(
        OR(
            Symptom(name='بقع رمادية على العناقيد', cf=MATCH.cf1),
            Symptom(name='تعفن طري على الثمار', cf=MATCH.cf1),
            Symptom(name='وجود زغب رمادي اللون', cf=MATCH.cf1)
        ),
        TEST(lambda cf1: cf1 >= 60)
    )
    def gray_mold_weak(self, cf1):
        final = round(cf1 * 0.45)
        print(f"\n❗ احتمال ضعيف: العفن الرمادي (العنب) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتحسين التشخيص.")
        self.declare(Fact(disease="العفن الرمادي"))

    @Rule(Fact(disease="العفن الرمادي"))
    def gray_mold_treatment(self):
        print("\n📌 المسبب: مرض العفن الرمادي في العنب يُسببه الفطر Botrytis cinerea.")
        print("\n💡 العلاج (العفن الرمادي - العنب):")
        print("- إزالة العناقيد والثمار المصابة فورًا")
        print("- تحسين التهوية والتعرض لأشعة الشمس بالتقليم")
        print("- استخدام مبيدات فطرية مثل: iprodione أو fenhexamid قبل الإزهار وبعده")
        print("- تجنب الرطوبة الزائدة وري النباتات في الصباح الباكر")
        self.halt()




    #  البياض الدقيقي
    @Rule(
        Symptom(name='مسحوق أبيض على سطح الأوراق والثمار', cf=MATCH.cf1),
        Symptom(name='تشوه الثمار وتوقف نموها', cf=MATCH.cf2),
        Symptom(name='تشقق الثمار وتلفها', cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60)
    )
    def grape_powdery_mildew_full(self, cf1, cf2, cf3):
        final = round(min(cf1, cf2, cf3) * 0.85)
        print(f"\n✅ التشخيص: البياض الدقيقي (العنب) (درجة الثقة: {final}/100)")
        self.declare(Fact(disease="البياض الدقيقي - العنب"))

    @Rule(
        OR(
            AND(Symptom(name='مسحوق أبيض على سطح الأوراق والثمار', cf=MATCH.cf1),
                Symptom(name='تشوه الثمار وتوقف نموها', cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name='مسحوق أبيض على سطح الأوراق والثمار', cf=MATCH.cf1),
                Symptom(name='تشقق الثمار وتلفها', cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name='تشوه الثمار وتوقف نموها', cf=MATCH.cf1),
                Symptom(name='تشقق الثمار وتلفها', cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60))
        )
    )
    def grape_powdery_mildew_partial(self, cf1=0, cf2=0):
        final = round(min(cf1, cf2) * 0.65)
        print(f"\n⚠️ تشخيص مبدئي: البياض الدقيقي (العنب) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتحسين التشخيص.")
        self.declare(Fact(disease="البياض الدقيقي - العنب"))

    @Rule(
        OR(
            Symptom(name='مسحوق أبيض على سطح الأوراق والثمار', cf=MATCH.cf1),
            Symptom(name='تشوه الثمار وتوقف نموها', cf=MATCH.cf1),
            Symptom(name='تشقق الثمار وتلفها', cf=MATCH.cf1)
        ),
        TEST(lambda cf1: cf1 >= 60)
    )
    def grape_powdery_mildew_weak(self, cf1):
        final = round(cf1 * 0.45)
        print(f"\n❗ احتمال ضعيف: البياض الدقيقي (العنب) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتحسين التشخيص.")
        self.declare(Fact(disease="البياض الدقيقي - العنب"))

    @Rule(Fact(disease="البياض الدقيقي - العنب"))
    def grape_powdery_mildew_treatment(self):
        print("\n📌 المسبب: مرض البياض الدقيقي في العنب يُسببه الفطر Erysiphe necator.")
        print("\n💡 العلاج (البياض الدقيقي - العنب):")
        print("- رش الكبريت القابل للبلل أو مبيدات تحتوي على Myclobutanil")
        print("- التكرار كل 10 أيام خلال الفترة الحساسة (قبل الإزهار وحتى نضج الثمار)")
        print("- تقليل الرطوبة وتحسين التهوية بالتقليم")
        print("- إزالة الأجزاء المصابة وتقليل التزاحم بين العناقيد")
        self.halt()



    #عفن الحذور
    @Rule(
        Symptom(name='ذبول الأوراق وسقوطها', cf=MATCH.cf1),
        Symptom(name='بقع صفراء على الأوراق', cf=MATCH.cf2),
        Symptom(name='توقف نمو النبات أو موته المفاجئ', cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60),
    )
    def root_rot_full(self, cf1, cf2, cf3):
        final = round(min(cf1, cf2, cf3) * 0.9)
        print(f"\n✅ تشخيص دقيق: عفن الجذور (العنب) (درجة الثقة: {final}/100)")
        self.declare(Fact(disease="عفن الجذور"))

    @Rule(
        OR(
            AND(Symptom(name='ذبول الأوراق وسقوطها', cf=MATCH.cf1),
                Symptom(name='بقع صفراء على الأوراق', cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name='ذبول الأوراق وسقوطها', cf=MATCH.cf1),
                Symptom(name='توقف نمو النبات أو موته المفاجئ', cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name='بقع صفراء على الأوراق', cf=MATCH.cf1),
                Symptom(name='توقف نمو النبات أو موته المفاجئ', cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
        ),

        salience = 6

    )
    def root_rot_partial(self, cf1=0, cf2=0):
        final = round(min(cf1, cf2) * 0.65)
        print(f"\n⚠️ تشخيص مبدئي: عفن الجذور (العنب) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتحسين التشخيص بسبب التشابه مع مرض اخر")
        self.declare(Fact(disease="عفن الجذور"))
        self.halt()


    @Rule(
        OR(
            Symptom(name='ذبول الأوراق وسقوطها', cf=MATCH.cf1),
            Symptom(name='بقع صفراء على الأوراق', cf=MATCH.cf1),
            Symptom(name='توقف نمو النبات أو موته المفاجئ', cf=MATCH.cf1)
        ),
        TEST(lambda cf1: cf1 >= 60),
        salience=5
    )
    def root_rot_weak(self, cf1):
        final = round(cf1 * 0.45)
        print(f"\n❗ احتمال ضعيف: عفن الجذور (العنب) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتحسين التشخيص بسبب التشابه مع مرض اخر")
        self.declare(Fact(disease="عفن الجذور"))
        self.halt()


    @Rule(Fact(disease="عفن الجذور"))
    def root_rot_treatment(self):
        print("\n📌 المسبب: مرض عفن الجذور في العنب يُسببه الفطر Phytophthora spp.")
        print("\n💡 العلاج (عفن الجذور - العنب):")
        print("- تحسين صرف التربة لتجنب تجمع المياه")
        print("- تقليل الري في التربة الطينية الثقيلة")
        print("- إزالة النباتات المصابة بالكامل لمنع الانتشار")
        print("- يمكن استخدام مبيدات فطرية مثل Metalaxyl حسب توصيات المختصين")
        self.halt()