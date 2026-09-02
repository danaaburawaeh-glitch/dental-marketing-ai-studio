---
document: portability
type: GOVERNANCE
version: 1.0.0
status: ACTIVE
applies_to: ALL_ASSISTANTS
---

# قواعد النقل — Portability Rules v1.0.0

هذا المستند يفرض القواعد التقنية التي تجعل `governance/standalone-guarantee.md` قابلاً للتحقق آلياً، لا مجرد نية معلنة. `tests/dependency-scan.py` يطبّق كل قاعدة هنا آلياً على كل ملف في الحزمة.

## القواعد الإلزامية

### ١. مسارات نسبية فقط — Relative Paths Only

كل مسار داخل أي `SKILL.md` أو ملف Governance أو Script يبدأ من جذر الحزمة أو من `${CLAUDE_PLUGIN_ROOT}` — أبداً من جذر نظام ملفات مطلق.

```
✔ knowledge/shared/brand-voice.md
✔ ${CLAUDE_PLUGIN_ROOT}/knowledge/
✘ /home/<user>/...
✘ /Users/<user>/...
✘ C:\Users\...
```

### ٢. لا مسارات جهاز محلي — No Local Machine Paths

لا إشارة إلى مسار خاص بجهاز أو بيئة عمل مُنشئ الحزمة الأصلي. المسارات الأربعة عشر التاريخية في `governance/migration-spec.yaml` (`source:`) استثناء موثَّق صراحة: بيانات منشأ (provenance) جامدة عن كيفية الترحيل، لا تُقرأ في وقت التشغيل من أي Skill أو Script — انظر الملاحظة أعلى ذلك الملف.

### ٣. لا معرّفات حساب شخصية — No Personal Account IDs

لا اسم حقيقي، لا معرّف مستخدم، لا رقم حساب. الحقل `owner:` في كل `SKILL.md` وملف Governance يحمل دوراً عاماً (`clinic-owner`) لا اسماً — هذا هو نمط المشروع الأصلي منذ v1.2.0، وأُكمل تعميمه في v1.3.0 (انظر `DEPENDENCIES.md` جدول التدقيق).

### ٤. لا روابط خاصة — No Private URLs

لا رابط Instagram أو WhatsApp أو Drive حقيقي مضمَّن في أي ملف. كل مرجع لرابط في `identity/house-rules.md §١` هو حقل `⟨fill-in⟩` يُعبَّأ من قِبَل كل مستخدم جديد لحسابه هو.

### ٥. لا إشارات لمساعدين خاصين — No Private Assistant References

لا `route_to` ولا `can_delegate_to` ولا `skill_dependencies` يشير إلى معرّف غير موجود فعلياً داخل مجلد `skills/` لهذه الحزمة. `governance/routing-policy.md § القاعدة ٤` يفترض أن كل `route_to` قابل للحل داخلياً؛ `tests/dependency-scan.py` يفشل البناء عند أي خرق.

### ٦. لا اعتماديات مخفية — No Hidden Dependencies

كل اعتمادية (Skill، ملف معرفة، أداة خارجية) مُعلَنة صراحة في `metadata` الخاصة بها (`skill_dependencies`، `knowledge_dependencies`، `tool_dependencies`) — لا اعتماد ضمني يُكتشف فقط بقراءة الجسم النثري.

### ٧. لا افتراضات بيئة ضمنية — No Implicit Environment Assumptions

لا Skill تفترض:

- وجود متغير بيئة (`os.environ`) لا يُعلَن في `config.example`
- وجود MCP أو Connector أو API متصل قبل التحقق منه فعلياً (انظر `governance/capability-detection.md`)
- تشغيل النظام من جهاز أو نظام تشغيل بعينه
- وجود ملفات أُنشئت من جلسة سابقة (كل ملف `knowledge/*` يبدأ DRAFT بحقول `⟨fill-in⟩`، لا بيانات مفترَضة)

## الاستثناءات الموثَّقة

| الاستثناء | لماذا مقبول |
|---|---|
| `governance/migration-spec.yaml` — حقول `source:` التاريخية | بيانات منشأ جامدة، لا تُقرأ وقت التشغيل، موثَّقة صراحةً في رأس الملف |
| `DEPENDENCIES.md`، `RELEASE-AUDIT-v1.3.0.md` | تقارير تدقيق تُسمّي المشكلات المكتشَفة والمُصلَحة عمداً — تسمية المشكلة جزء من إثبات إصلاحها، لا تسريب |
| أسماء أدوات خارجية في النثر (مثال: «Canva»، «Google Calendar») | اسم منتج عام لا معرّف حساب — كل استخدام فعلي يمر عبر اكتشاف قدرة أولاً |
| `skills/system-update-checker/SKILL.md` و`scripts/check_update.py` — رابط `danaaburawaeh-glitch/dental-marketing-ai-studio` | نقطة توزيع **عامة للمنتج** وليست بيانات حساب مستخدم أو اعتماداً خاصاً بمالك النسخة؛ مطلوبة فقط لاكتشاف الإصدارات المنشورة، والفحص يفشل بأمان إذا تغير المصدر أو غاب الإنترنت |
| `governance/assistant-id-migration-map.md`، `README.md` و`CHANGELOG.md` (سجل التغييرات التاريخي)، `governance/evals/exclusions-golden-set.yaml`، `governance/evals/regression-baseline.yaml` — إشارات نصية لمعرّفات مساعدين خارجيين (`dana-instagram-growth-director` وغيرها) | سجل هندسي تاريخي أو بيانات اختبار إقصاء (`expect: EXTERNAL:...`) تُثبت أن الموجّه **لا** يستدعيها — لا `route_to`/`can_delegate_to`/`skill_dependencies` فعلي يعتمد عليها؛ مصنَّفة Type D في `DEPENDENCIES.md` |
| `tests/dependency-scan.py` — نص الأنماط (regex) في الملف نفسه | الماسح يستثني مصدره من فحص المسارات المطلقة؛ بادئات مسارات الجذر المكتوبة داخل تعريف النمط نفسه جزء من الفحص لا بيانات مسرَّبة |
| `governance/foundation-validation-report.md`، `governance/proposals/2026-08-28-standalone-external-reference-removal.md`، `governance/routing-tests.yaml`، `knowledge/assistants-registry.md`، هذا الملف نفسه (`governance/portability.md`) — إشارات نصية لمعرّفات مساعدين خارجيين (`dana-instagram-growth-director` وغيرها) | تقارير تدقيق/ACP تاريخية، تعليقات توضيحية في ملف اختبار، أو دليل مُولَّد آلياً من `migration-spec.yaml § deferred` — لا `route_to`/`can_delegate_to`/`skill_dependencies` فعلي يعتمد عليها؛ نفس تصنيف Type D في `DEPENDENCIES.md` |

## آلية الفحص

`tests/dependency-scan.py` يبحث آلياً عن: مسارات مطلقة (`/home/`, `/Users/`, `C:\`)، أسماء مساعدين غير مُرحَّلين (route_to لا يقابله assistant_id حقيقي)، معرّفات شخصية معروفة (نمط `owner: <اسم>` بدل دور)، روابط خاصة (أنماط `instagram.com/<حساب>`, `wa.me/<رقم>`), وأسرار/مفاتيح API. النتيجة المطلوبة: **Required unresolved dependencies: 0**.

## العلاقة بالوثائق الأخرى

```
governance/standalone-guarantee.md ← الالتزام المعماري الذي تخدمه هذه القواعد التقنية
DEPENDENCIES.md                    ← نتيجة تطبيق هذه القواعد على الحزمة الحالية
tests/dependency-scan.py           ← التطبيق الآلي لكل قاعدة أعلاه
```

## سجل التحديث

| التاريخ | ما تغيّر |
|---|---|
| 2026-08-28 | إنشاء الملف — v1.3.0 Standalone Edition |
