from experta import Rule, Fact, MATCH, TEST, OR, AND
from core import Symptom, PlantDiagnosisEngine

class CherryRules(PlantDiagnosisEngine):

    #البياض الدقيقي
    @Rule(
        Symptom(name='بقع بيضاء على سطح الأوراق', cf=MATCH.cf1),
        Symptom(name='تشوه الأوراق', cf=MATCH.cf2),
        Symptom(name='تبقع وتلف الثمار', cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60),
        salience=30
    )
    def full_diagnosis(self, cf1, cf2, cf3):
        final = round(min(cf1, cf2, cf3) * 0.85)
        print(f"\n✅ التشخيص: البياض الدقيقي (الكرز) (درجة الثقة: {final}/100)")
        self.declare(Fact(disease="البياض الدقيقي"))

    @Rule(
        OR(
            AND(Symptom(name='بقع بيضاء على سطح الأوراق', cf=MATCH.cf1),
                Symptom(name='تشوه الأوراق', cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name='بقع بيضاء على سطح الأوراق', cf=MATCH.cf1),
                Symptom(name='تبقع وتلف الثمار', cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name='تشوه الأوراق', cf=MATCH.cf1),
                Symptom(name='تبقع وتلف الثمار', cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60))
        )
    ,
        salience=20
    )
    def partial_diagnosis(self, cf1=0, cf2=0):
        final = round(min(cf1, cf2) * 0.65)
        print(f"\n⚠️ تشخيص مبدئي: البياض الدقيقي (الكرز) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتأكيد التشخيص.")
        self.declare(Fact(disease="البياض الدقيقي"))

    @Rule(
        OR(
            Symptom(name='بقع بيضاء على سطح الأوراق', cf=MATCH.cf1),
            Symptom(name='تشوه الأوراق', cf=MATCH.cf1),
            Symptom(name='تبقع وتلف الثمار', cf=MATCH.cf1)
        ),
        TEST(lambda cf1: cf1 >= 60),
        salience=10
    )
    def weak_diagnosis(self, cf1):
        final = round(cf1 * 0.45)
        print(f"\n❗ احتمال ضعيف: البياض الدقيقي (الكرز) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتأكيد التشخيص.")
        self.declare(Fact(disease="البياض الدقيقي"))

    @Rule(Fact(disease="البياض الدقيقي"), salience=5)
    def treatment(self):
        print("\n📌 المسبب: مرض البياض الدقيقي في الكرز يُسببه الفطر Podosphaera clandestina.")
        print("\n💡 العلاج (البياض الدقيقي - الكرز):")
        print("- رش الكبريت الميكروني أو Triadimefon عند ظهور أولى العلامات")
        print("- إعادة الرش كل 10–14 يوم عند الحاجة")
        print("- إزالة الأوراق المصابة لتحسين التهوية")
        print("- تقليم الفروع لتقليل الرطوبة حول النبات")
        self.halt()



    #تبقع الأوراق

    @Rule(
        Symptom(name='بقع أرجوانية أو حمراء على الأوراق', cf=MATCH.cf1),
        Symptom(name='ثقوب دائرية في الأوراق', cf=MATCH.cf2),
        Symptom(name='بقع داكنة على الثمار', cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60)
    ,
        salience=30
    )
    def shot_hole_full(self, cf1, cf2, cf3):
        final_cf = round(min(cf1, cf2, cf3) * 0.85)
        print(f"\n✅ التشخيص: تَبَقُّع الأوراق - الكرز (درجة الثقة: {final_cf}/100)")
        self.declare(Fact(disease="تَبَقُّع الأوراق"))

    @Rule(
        OR(
            AND(Symptom(name='بقع أرجوانية أو حمراء على الأوراق', cf=MATCH.cf1),
                Symptom(name='ثقوب دائرية في الأوراق', cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name='بقع أرجوانية أو حمراء على الأوراق', cf=MATCH.cf1),
                Symptom(name='بقع داكنة على الثمار', cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name='ثقوب دائرية في الأوراق', cf=MATCH.cf1),
                Symptom(name='بقع داكنة على الثمار', cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60))
        )
    ,
        salience=20
    )
    def shot_hole_partial(self, cf1=0, cf2=0):
        final = round(min(cf1, cf2) * 0.65)
        print(f"\n⚠️ تشخيص مبدئي: تَبَقُّع الأوراق (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتأكيد التشخيص.")
        self.declare(Fact(disease="تَبَقُّع الأوراق"))

    @Rule(
        OR(
            Symptom(name='بقع أرجوانية أو حمراء على الأوراق', cf=MATCH.cf1),
            Symptom(name='ثقوب دائرية في الأوراق', cf=MATCH.cf1),
            Symptom(name='بقع داكنة على الثمار', cf=MATCH.cf1)
        ),
        TEST(lambda cf1: cf1 >= 60)
    ,
        salience=10
    )
    def shot_hole_weak(self, cf1):
        final = round(cf1 * 0.45)
        print(f"\n❗ احتمال ضعيف: تَبَقُّع الأوراق (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتأكيد التشخيص.")
        self.declare(Fact(disease="تَبَقُّع الأوراق"))

    @Rule(Fact(disease="تَبَقُّع الأوراق"), salience=5)
    def treatment_shot_hole(self):
        print("\n📌 المسبب: مرض تبقّع الأوراق في الكرز يُسببه الفطر Blumeriella jaapii.")
        print("\n💡 العلاج (تَبَقُّع الأوراق - الكرز):")
        print("- رش مبيدات فطرية تحتوي على النحاس أو Captan خلال الخريف والربيع")
        print("- إزالة الأوراق والثمار المصابة وتقليل الرطوبة")
        print("- تحسين التهوية من خلال تقليم جيد")
        self.halt()




    #  عفن الثمار البني
    @Rule(
        Symptom(name='بقع بنية طرية على الثمار', cf=MATCH.cf1),
        Symptom(name='ظهور دوائر بيضاء من الأبواغ', cf=MATCH.cf2),
        Symptom(name='تعفن الثمار وتساقطها', cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60)
    ,
        salience=30
    )
    def cherry_brown_rot_full(self, cf1, cf2, cf3):
        final_cf = round(min(cf1, cf2, cf3) * 0.85)
        print(f"\n✅ التشخيص: عفن الثمار البني (الكرز) (درجة الثقة: {final_cf}/100)")
        self.declare(Fact(disease="عفن الثمار البني"))

    @Rule(
        OR(
            AND(Symptom(name='بقع بنية طرية على الثمار', cf=MATCH.cf1),
                Symptom(name='ظهور دوائر بيضاء من الأبواغ', cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name='بقع بنية طرية على الثمار', cf=MATCH.cf1),
                Symptom(name='تعفن الثمار وتساقطها', cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name='ظهور دوائر بيضاء من الأبواغ', cf=MATCH.cf1),
                Symptom(name='تعفن الثمار وتساقطها', cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60))
        )
    ,
        salience=20
    )
    def cherry_brown_rot_partial(self, cf1=0, cf2=0):
        final = round(min(cf1, cf2) * 0.65)
        print(f"\n⚠️ تشخيص مبدئي: عفن الثمار البني (الكرز) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتأكيد التشخيص.")
        self.declare(Fact(disease="عفن الثمار البني"))

    @Rule(
        OR(
            Symptom(name='بقع بنية طرية على الثمار', cf=MATCH.cf1),
            Symptom(name='ظهور دوائر بيضاء من الأبواغ', cf=MATCH.cf1),
            Symptom(name='تعفن الثمار وتساقطها', cf=MATCH.cf1)
        ),
        TEST(lambda cf1: cf1 >= 60)
    ,
        salience=10
    )
    def cherry_brown_rot_weak(self, cf1):
        final = round(cf1 * 0.45)
        print(f"\n❗ احتمال ضعيف: عفن الثمار البني (الكرز) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتأكيد التشخيص.")
        self.declare(Fact(disease="عفن الثمار البني"))

    @Rule(Fact(disease="عفن الثمار البني"), salience=5)
    def cherry_brown_rot_treatment(self):
        print("\n📌 المسبب: مرض عفن القمار البني في الكرز يُسببه الفطر Monilinia fructicola.")
        print("\n💡 العلاج (عفن الثمار البني - الكرز):")
        print("- إزالة الثمار المصابة وعدم تركها على الشجرة أو في الأرض")
        print("- الرش بمبيدات فطرية مثل Captan أو Myclobutanil في فترة الإزهار وقبل القطاف")
        print("- تقليم الفروع المصابة وتحسين التهوية")
        print("- تقليل الري وقت نضج الثمار لتقليل الرطوبة الزائدة")
        self.halt()




    #  سرطان اللحاء البكتيري
    @Rule(
        Symptom(name='تقرحات غائرة على الساق أو الأغصان', cf=MATCH.cf1),
        Symptom(name='تسرب صمغ من أماكن التقرحات', cf=MATCH.cf2),
        Symptom(name='ذبول مفاجئ للأوراق أو الأغصان', cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60)
    ,
        salience=30
    )
    def cherry_bacterial_canker_full(self, cf1, cf2, cf3):
        final_cf = round(min(cf1, cf2, cf3) * 0.85)
        print(f"\n✅ التشخيص: سرطان اللحاء البكتيري (الكرز) (درجة الثقة: {final_cf}/100)")
        self.declare(Fact(disease="سرطان اللحاء البكتيري"))

    @Rule(
        OR(
            AND(Symptom(name='تقرحات غائرة على الساق أو الأغصان', cf=MATCH.cf1),
                Symptom(name='تسرب صمغ من أماكن التقرحات', cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name='تقرحات غائرة على الساق أو الأغصان', cf=MATCH.cf1),
                Symptom(name='ذبول مفاجئ للأوراق أو الأغصان', cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name='تسرب صمغ من أماكن التقرحات', cf=MATCH.cf1),
                Symptom(name='ذبول مفاجئ للأوراق أو الأغصان', cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60))
        )
    ,
        salience=20
    )
    def cherry_bacterial_canker_partial(self, cf1=0, cf2=0):
        final = round(min(cf1, cf2) * 0.65)
        print(f"\n⚠️ تشخيص مبدئي: سرطان اللحاء البكتيري (الكرز) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتأكيد التشخيص.")
        self.declare(Fact(disease="سرطان اللحاء البكتيري"))

    @Rule(
        OR(
            Symptom(name='تقرحات غائرة على الساق أو الأغصان', cf=MATCH.cf1),
            Symptom(name='تسرب صمغ من أماكن التقرحات', cf=MATCH.cf1),
            Symptom(name='ذبول مفاجئ للأوراق أو الأغصان', cf=MATCH.cf1)
        ),
        TEST(lambda cf1: cf1 >= 60)
    ,
        salience=10
    )
    def cherry_bacterial_canker_weak(self, cf1):
        final = round(cf1 * 0.45)
        print(f"\n❗ احتمال ضعيف: سرطان اللحاء البكتيري (الكرز) (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتأكيد التشخيص.")
        self.declare(Fact(disease="سرطان اللحاء البكتيري"))

    @Rule(Fact(disease="سرطان اللحاء البكتيري"), salience=5)
    def cherry_bacterial_canker_treatment(self):
        print("\n📌 المسبب: مرض سرطان اللحاء البكتيري في الكرز يُسببه البكتيريا Pseudomonas syringae pv. syringae.")
        print("\n💡 العلاج (سرطان اللحاء البكتيري - الكرز):")
        print("- تقليم الأغصان المصابة في الصيف فقط (لتقليل انتشار البكتيريا)")
        print("- رش مضادات بكتيرية مثل أوكسي كلوريد النحاس بعد التقليم")
        print("- تطهير أدوات التقليم بمحلول كحولي أو مبيض مخفف")
        print("- زراعة أصناف مقاومة والابتعاد عن الزراعة في الأراضي المجهدة")
        self.halt()