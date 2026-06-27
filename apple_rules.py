from experta import Rule, Fact, MATCH, TEST, OR, AND
from core import Symptom, PlantDiagnosisEngine

class AppleRules(PlantDiagnosisEngine):

    # ---------------- جرب التفاح ----------------
    @Rule(
        Symptom(name='بقع زيتية على الأوراق', cf=MATCH.cf1),
        Symptom(name='تشوه الثمار', cf=MATCH.cf2),
        Symptom(name='تقشر لون الأوراق', cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60)
    ,
        salience=30
    )
    def diagnose_apple_scab_full(self, cf1, cf2, cf3):
        final_cf = round(min(cf1, cf2, cf3) * 0.85)
        print(f"\n✅ التشخيص: جرب التفاح (درجة الثقة: {final_cf}/100)")
        self.declare(Fact(disease="جرب التفاح"))

    @Rule(
        OR(
            AND(Symptom(name='بقع زيتية على الأوراق', cf=MATCH.cf1),
                Symptom(name='تشوه الثمار', cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),

            AND(Symptom(name='بقع زيتية على الأوراق', cf=MATCH.cf1),
                Symptom(name='تقشر لون الأوراق', cf=MATCH.cf3),
                TEST(lambda cf1, cf3: min(cf1, cf3) >= 60)),

            AND(Symptom(name='تشوه الثمار', cf=MATCH.cf2),
                Symptom(name='تقشر لون الأوراق', cf=MATCH.cf3),
                TEST(lambda cf2, cf3: min(cf2, cf3) >= 60))
        )
    ,
        salience=20
    )
    def diagnose_apple_scab_partial(self, cf1=0, cf2=0, cf3=0):
        final_cf = round(min(v for v in [cf1, cf2, cf3] if v > 0) * 0.65)
        print(f"\n⚠️ تشخيص مبدئي: جرب التفاح (درجة الثقة: {final_cf}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتأكيد التشخيص.")
        self.declare(Fact(disease="جرب التفاح"))

    @Rule(
        OR(
            Symptom(name='بقع زيتية على الأوراق', cf=MATCH.cf1),
            Symptom(name='تشوه الثمار', cf=MATCH.cf1),
            Symptom(name='تقشر لون الأوراق', cf=MATCH.cf1)
        ),
        TEST(lambda cf1: cf1 >= 60)
    ,
        salience=10
    )
    def diagnose_apple_scab_weak(self, cf1):
        final_cf = round(cf1 * 0.45)
        print(f"\n❕ احتمال ضعيف: جرب التفاح (درجة الثقة: {final_cf}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتأكيد التشخيص.")
        self.declare(Fact(disease="جرب التفاح"))

    @Rule(Fact(disease='جرب التفاح'), salience=5)
    def treatment_apple_scab(self):
        print("\n📌 المسبب: مرض جرب التفاح يُسببه الفطر Venturia inaequalis.")
        print("\n💡 العلاج (جرب التفاح):")
        print("- رش Captan أو Kumulus كل 7–14 يوم لمدة 2–3 شهور")
        print("- رش علاجي بعد الأعراض خلال 48 ساعة")
        print("- إزالة الأوراق/الثمار المصابة باستمرار")
        print("- تقليم الأغصان سنويًا")
        self.halt()

        # ______ العفن الأسود _______

    @Rule(
        Symptom(name='بقع بنفسجية على الأوراق', cf=MATCH.cf1),
        Symptom(name='تقرحات على الأغصان', cf=MATCH.cf2),
        Symptom(name='تعفن بني على الثمار', cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60)
    ,
        salience=30
    )
    def br_full(self, cf1, cf2, cf3):
        final = round(min(cf1, cf2, cf3) *  0.85)
        print(f"\n✅ تشخيص : العفن الأسود (درجة الثقة: {final}/100)")
        self.declare(Fact(disease="العفن الأسود"))

    @Rule(
        OR(
            AND(Symptom(name='بقع بنفسجية على الأوراق', cf=MATCH.cf1),
                Symptom(name='تقرحات على الأغصان', cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name='بقع بنفسجية على الأوراق', cf=MATCH.cf1),
                Symptom(name='تعفن بني على الثمار', cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name='تقرحات على الأغصان', cf=MATCH.cf1),
                Symptom(name='تعفن بني على الثمار', cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60))
        )
    ,
        salience=20
    )
    def br_partial(self, cf1=0, cf2=0):
        final = round(min(cf1, cf2) * 0.65)
        print(f"\n⚠️ تشخيص مبدئي: العفن الأسود (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتأكيد التشخيص.")
        self.declare(Fact(disease="العفن الأسود"))

    @Rule(
        OR(
            Symptom(name='بقع بنفسجية على الأوراق', cf=MATCH.cf1),
            Symptom(name='تقرحات على الأغصان', cf=MATCH.cf1),
            Symptom(name='تعفن بني على الثمار', cf=MATCH.cf1)
        ),
        TEST(lambda cf1: cf1 >= 60)
    ,
        salience=10
    )
    def br_weak(self, cf1):
        final = round(cf1 * 0.45 )
        print(f"\n❗ احتمال ضعيف: العفن الأسود (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتأكيد التشخيص.")
        self.declare(Fact(disease="العفن الأسود"))

    # --- العلاج ---
    @Rule(Fact(disease="العفن الأسود"), salience=5)
    def br_treatment(self):
        print("\n📌 المسبب: مرض العفن الأسود في التفاح يُسببه الفطر Botryosphaeria obtusa.")
        print("\n💡 العلاج (العفن الأسود):")
        print("- تقليم وإزالة الثمار/الأغصان المصابة طوال السنة")
        print("- رش Captan أو Polyram كل 10‑14 يوم لمدة 4–6 أسابيع")
        print("- بديل بيولوجي: Trianum Shield حسب الحاجة")
        print("- تقليم Cankers 15 سم تحت الأنسجة المريضة")
        self.halt()


    # ---------------- صدأ التفاح الصنوبري ----------------
    @Rule(
        Symptom(name='بقع صفراء على الأوراق', cf=MATCH.cf1),
        Symptom(name='أورام برتقالية', cf=MATCH.cf2),
        Symptom(name='تورم الأوراق من الأسفل', cf=MATCH.cf3),
        TEST(lambda cf1, cf2, cf3: min(cf1, cf2, cf3) >= 60)
    ,
        salience=30
    )
    def cedar_rust_full(self, cf1, cf2, cf3):
        final = round(min(cf1, cf2, cf3) *  0.85)
        print(f"\n✅ تشخيص : صدأ التفاح الصنوبري (درجة الثقة: {final}/100)")
        self.declare(Fact(disease="صدأ التفاح الصنوبري"))

    @Rule(
        OR(
            AND(Symptom(name='بقع صفراء على الأوراق', cf=MATCH.cf1),
                Symptom(name='أورام برتقالية', cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name='بقع صفراء على الأوراق', cf=MATCH.cf1),
                Symptom(name='تورم الأوراق من الأسفل', cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60)),
            AND(Symptom(name='أورام برتقالية', cf=MATCH.cf1),
                Symptom(name='تورم الأوراق من الأسفل', cf=MATCH.cf2),
                TEST(lambda cf1, cf2: min(cf1, cf2) >= 60))
        )
    ,
        salience=20
    )
    def cedar_rust_partial(self, cf1=0, cf2=0):
        final = round(min(cf1, cf2) * 0.65)
        print(f"\n⚠️ تشخيص مبدئي: صدأ التفاح الصنوبري (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتأكيد التشخيص.")
        self.declare(Fact(disease="صدأ التفاح الصنوبري"))

    @Rule(
        OR(
            Symptom(name='بقع صفراء على الأوراق', cf=MATCH.cf1),
            Symptom(name='أورام برتقالية', cf=MATCH.cf1),
            Symptom(name='تورم الأوراق من الأسفل', cf=MATCH.cf1)
        ),
        TEST(lambda cf1: cf1 >= 60)
    ,
        salience=10
    )
    def cedar_rust_weak(self, cf1):
        final = round(cf1 * 0.45)
        print(f"\n❗ احتمال ضعيف: صدأ التفاح الصنوبري (درجة الثقة: {final}/100)")
        print("⚠️ يُفضل إدخال المزيد من الأعراض لتأكيد التشخيص.")
        self.declare(Fact(disease="صدأ التفاح الصنوبري"))

    @Rule(Fact(disease="صدأ التفاح الصنوبري"), salience=5)
    def cedar_rust_treatment(self):
        print("\n📌 المسبب: مرض صدأ التفاح يُسببه الفطر Gymnosporangium juniperi-virginianae.")
        print("\n💡 العلاج (صدأ التفاح الصنوبري):")
        print("- رش مبيدات فطرية تحتوي على Myclobutanil أو Mancozeb كل 7–10 أيام أثناء الربيع")
        print("- إزالة أوراق العرعر القريبة إن أمكن (ناقل المرض)")
        print("- تقليم الأغصان المصابة وتحسين التهوية")
        print("- زراعة أصناف مقاومة للمرض في المستقبل")
        self.halt()