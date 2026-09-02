---
document: evaluation-policy
type: GOVERNANCE
version: 1.0.0
status: ACTIVE
applies_to: ALL_ASSISTANTS
---

# سياسة التقييم — Evaluation Policy v1.0.0

يحدد هذا الملف بنية `governance/evals/` ودور كل مجموعة اختبار فيها، ويُرجَع إليه من `release-policy.md § البوابة ٣، ٤، ٥، ٦، ٧`.

## البنية

```
governance/evals/
  routing-golden-set.yaml         إصابة أحادية المساعد — عبارة واحدة، مساعد واحد متوقَّع
  exclusions-golden-set.yaml      إقصاء — عبارة قريبة يجب ألا تصيب الجار
  orchestration-golden-set.yaml   قرار Single vs Multi-Agent + تفكيك المهمة + DAG
  handoff-golden-set.yaml         صلاحية عقد التسليم بين مساعدَين
  safety-golden-set.yaml          نية سريرية · طوارئ · بيانات مرضى · ادعاء غير مسموح
  regression-baseline.yaml        كل حالة كانت تعمل صحيحة سابقاً — يُمنع الانحدار عنها
  edge-cases.yaml                 حالات حدّية: alias قديم، مدخل ناقص، تفويض دائري صناعي
```

`governance/routing-tests.yaml` الحالي (29 حالة) هو **أول** مجموعة فعلية ويُعامَل كنواة لـ `routing-golden-set.yaml` + `exclusions-golden-set.yaml` مجتمعتين (فيه النوعان معاً بحقل `rule`). لا يُعاد إنشاؤه من الصفر؛ يُستخدم كما هو بواسطة `routing_tests.py`، والملفات الجديدة تُضيف تغطية لا تُكرره.

## عدد السيناريوهات — واقعي لا شكلي

**لا تُملأ الملفات باختبارات صورية.** كل ملف يبدأ بعدد يغطي الأنماط الفعلية المذكورة في §14 من طلب Hardening (مساعد واحد، متعدد المساعدين، توجيه غامض، توجيه سالب، alias مهجور، مدخل ناقص، تفويض دائري، سلامة) — لا أقل، ولا حشو لأجل الرقم.

## أنواع السيناريوهات الإلزامية لكل ملف جديد

| الملف | الحد الأدنى من الأنماط |
|---|---|
| `orchestration-golden-set.yaml` | مساعد واحد كافٍ (لا orchestration) · متعدد بترتيب DAG واضح · تعارض توجيه (`ROUTING_CONFLICT`) · مدخل ناقص (`NEEDS_INPUT`) |
| `handoff-golden-set.yaml` | handoff صالح كامل الحقول · handoff بحقل ناقص (`SCHEMA_INVALID`) · handoff بـ `safety.status: SAFETY_BLOCK` يوقف السلسلة |
| `safety-golden-set.yaml` | نية سريرية غير طارئة تُحال · طارئ يوقف كل شيء · طلب بيانات مريض يُرفض · ادعاء علمي بلا مصدر |
| `edge-cases.yaml` | `legacy_alias` قديم يُقبل ويُوجَّه لصاحبه الكانوني · تفويض دائري صناعي (A→B→A) يُكتشف ولا يُنفَّذ · استدعاء متكرر لنفس المساعد بلا سبب جديد يُرفض |

## القياس

- **Routing accuracy** = نجاح `routing-golden-set` ÷ الإجمالي.
- **Exclusion accuracy** = نجاح `exclusions-golden-set` ÷ الإجمالي.
- **Orchestration decision accuracy** = نجاح `orchestration-golden-set` ÷ الإجمالي (يشمل: هل قرَّر صح Single vs Multi-Agent، لا فقط هل اختار المساعد الصح).
- **Regression** = مقارنة حرفية بنتيجة `regression-baseline.yaml` من آخر إصدار مستقر؛ أي حالة كانت PASS وأصبحت FAIL = انحدار، يوقف البناء بصرف النظر عن باقي الأرقام.

القياس يُنتَج من `scripts/routing_tests.py` (أحادي/إقصاء) و`scripts/orchestration_tests.py` (تفكيك ومسار) معاً — كل سكربت يقرأ مجموعته المعنية، والتقرير المُجمَّع في `scripts/studio_health.py`.

## من يحدّث الـ Golden Sets

كل حالة اختبار جديدة تُضاف فقط بعد ملاحظة سلوك حقيقي (فشل تشغيلة، غموض تم حسمه، حالة حدّية اكتُشفت أثناء الاستخدام) — لا اختباراً افتراضياً. هذا يطابق ما فعلته `routing-tests.yaml` مع "أرقام الحساب" في مرحلة سابقة: خطأ حقيقي أُصلح ثم قُفل بحالة اختبار.
