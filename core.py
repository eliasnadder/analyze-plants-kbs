from __future__ import annotations

from experta import Fact, KnowledgeEngine

# ── ثوابت معاملات درجة الثقة ──────────────────────────────────────────────
CF_VERY_HIGH = 0.90   # 4 أعراض أو ثقة عالية جداً
CF_FULL      = 0.85   # 3 أعراض (القاعدة العامة)
CF_HIGH_3    = 0.80   # 3 أعراض من 4 مطلوبة
CF_MED_HIGH  = 0.70   # حالتا عرضَين (ثقة فوق المتوسط)
CF_PARTIAL   = 0.65   # 2 أعراض (القاعدة العامة)
CF_MEDIUM    = 0.60   # 2 أعراض (ثقة متوسطة)
CF_MED_LOW   = 0.50   # عرض واحد (ثقة متوسطة)
CF_WEAK      = 0.45   # عرض واحد (القاعدة العامة)
CF_LOW       = 0.40   # عرض واحد من اثنين فقط

# ── ثوابت النصوص المساعدة ──────────────────────────────────────────────────
HINT_MORE_SYMPTOMS   = "يُفضل إدخال المزيد من الأعراض لتأكيد التشخيص."
HINT_SIMILAR_DISEASE = "يُفضل إدخال المزيد من الأعراض لتحسين التشخيص بسبب التشابه مع مرض آخر."


class Symptom(Fact):
    pass


class PlantDiagnosisEngine(KnowledgeEngine):

    # ── مساعدات التشخيص ────────────────────────────────────────────────────

    def _diagnose(
        self,
        disease: str,
        *cfs: int,
        multiplier: float,
        label: str,
        hint: str = "",
    ) -> None:
        final = round(min(cfs) * multiplier)
        print(f"\n {label}: {disease} (درجة الثقة: {final}/100)")
        if hint:
            print(f" {hint}")
        self.declare(Fact(disease=disease))

    def _diagnose_full(
        self, disease: str, *cfs: int, multiplier: float = CF_FULL
    ) -> None:
        self._diagnose(disease, *cfs, multiplier=multiplier, label="التشخيص")

    def _diagnose_partial(
        self,
        disease: str,
        *cfs: int,
        multiplier: float = CF_PARTIAL,
        hint: str = HINT_MORE_SYMPTOMS,
    ) -> None:
        self._diagnose(
            disease, *cfs, multiplier=multiplier, label="تشخيص مبدئي", hint=hint
        )

    def _diagnose_weak(
        self,
        disease: str,
        cf: int,
        multiplier: float = CF_WEAK,
        hint: str = HINT_MORE_SYMPTOMS,
    ) -> None:
        self._diagnose(
            disease, cf, multiplier=multiplier, label="احتمال ضعيف", hint=hint
        )

    # ── مساعدات العلاج ─────────────────────────────────────────────────────

    def _treat(
        self, disease_name: str, cause: str, steps: list[str]
    ) -> None:
        print(f"\n المسبب: {cause}")
        print(f"\n العلاج ({disease_name}):")
        for step in steps:
            print(f"- {step}")
        self.halt()
