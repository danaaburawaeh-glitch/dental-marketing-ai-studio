# اقتراح تغيير معماري — وسم الحالة داخل description

---

## Problem

فشل حقيقي مرصود أثناء تدقيق مستقل للإضافة (٢٨ أغسطس ٢٠٢٦): محرّك التوجيه الفعلي في بيئة التشغيل الحقيقية (Cowork/Claude) لا يقرأ `metadata.status` عند اختيار مهارة — يقرأ فقط حقل `description` في الـ frontmatter. تم التحقق من هذا مباشرة: استدعاء `content-case-post-reviewer` (وحالته الرسمية يومها `TESTING`، أي "لا يدخل التوجيه التلقائي" حرفياً وفق `lifecycle-versioning.md`) نُفِّذ فوراً وبلا أي تمييز عن مساعد `ACTIVE`. نفس الفحص أُجري على `system-assistant-orchestrator` بنفس النتيجة.

الأثر: قفل "لا اعتماد بلا اختبار" (`last_tested_version == version` لـ `ACTIVE`) يعمل فعلياً وفق الفحص الآلي (`validate_system.py`)، لكنه **لا يصل لنقطة القرار الفعلية وقت الاستخدام الحي** — الحوكمة صحيحة على الورق وغير مُنفَّذة عند التشغيل الحقيقي. هذا ليس تحسيناً نظرياً؛ هو فجوة إنفاذ مُثبَتة بالتجربة المباشرة.

## Proposed Change

كل مساعد بحالة غير `ACTIVE` يجب أن يبدأ حقل `description` (نص الـ frontmatter الذي يقرأه محرّك التوجيه الفعلي، لا `metadata.status` وحده) بوسم صريح:

| الحالة | الوسم الإلزامي في بداية description |
|---|---|
| `TESTING` / `PILOT` / `DRAFT` | `[STATUS: <الحالة>]` |
| `DEPRECATED` | `[STATUS: DEPRECATED → <deprecated_by>]` |
| `ARCHIVED` | `[STATUS: ARCHIVED]` |
| `ACTIVE` | بلا وسم — description نظيف كما كان |

الوسم يُتبَع بجملة توضيحية قصيرة (سبب الحالة، ومتى يُستخدَم المساعد رغم ذلك) قبل استئناف الوصف الأصلي حرفياً — لا حذف ولا إعادة صياغة لعبارات التشغيل المقتبسة القائمة.

فحص جديد `description_reflects_status` أُضيف إلى `scripts/validate_system.py` (بعد `description_routable` مباشرة) يفشل البناء عند غياب الوسم الصحيح — بنفس منطق `active_version_tested`: لا اعتماد على الالتزام اليدوي.

## Reason

يحقق ثلاثة من مبادئ §١: **منع فشل حقيقي** (مُثبَت بالتجربة لا مُتوقَّع)، **تحسين سلامة** (أخطر مهارة CRITICAL في النظام كانت التي كشفت الفجوة)، و**قابلية اختبار** (الفحص الجديد يمنع تكرار هذا الخطأ تلقائياً لأي مساعد مستقبلي يتحول عن `ACTIVE`).

## Affected Components

- `governance/assistant-schema.md` — تفسير إضافي لحقل `description` (لا تغيير في اسم/نوع الحقل، فقط قيد محتوى إضافي عند status ≠ ACTIVE).
- `scripts/validate_system.py` — فحص جديد `description_reflects_status`.
- المهارتان الوحيدتان غير `ACTIVE` حالياً: `content-case-post-reviewer`، `system-assistant-orchestrator` — description مُحدَّث، PATCH version (1.1.0→1.1.1 و1.0.0→1.0.1 على التوالي)، أُعيد الاختبار والختم.
- `knowledge/assistants-registry.md` — أُعيد توليده.

## Backward Compatibility

لا كسر: لا `legacy_alias` تأثر، لا `route_to` تغيّر، عبارات التشغيل المقتبسة في كلا الوصفين بقيت حرفياً كما كانت — `routing_tests.py` (الذي لا يقرأ `description` أصلاً، فقط `metadata.triggers`) أثبت ٢٩/٢٩ بلا انحدار. أي مساعد `ACTIVE` مستقبلي غير متأثر؛ القيد يُفعَّل فقط عند الخروج من `ACTIVE`.

## Migration

لا ترحيل بيانات مطلوب — القيد يُفحص عند كل تشغيلة `validate_system.py` القادمة تلقائياً. أي مساعد يتحول لاحقاً إلى `TESTING`/`PILOT`/`DEPRECATED`/`ARCHIVED` عبر `system-assistant-tuner` يجب أن يضيف الوسم في نفس الخطوة، وإلا يفشل الفحص فوراً.

## Tests

`validate_system.py` (بوابة ١-٢ في `release-policy.md`) أُعيد تشغيله كاملاً: **قبل** التعديل — فشل بخطأين حقيقيين (`description_reflects_status` على المساعدين). **بعد** التعديل: `PASS WITH WARNINGS` (نفس ١١ تنبيهاً المعروفة سلفاً، صفر خطأ جديد). `routing_tests.py`: 29/29، بلا تغيير. لم تُضَف حالة إلى `governance/evals/` بعد — يُوصى بإضافة حالة `description_reflects_status` إلى `edge-cases.yaml` في دورة الصيانة القادمة.

## Rollback

عكس التغيير: إزالة الوسم من بداية الوصفين، حذف كتلة الفحص من `validate_system.py`، إعادة `version`/`last_tested_version` للقيمتين السابقتين (1.1.0/1.0.0) وإعادة تشغيل `stamp_tested.py`. لا فقد بيانات — كل التعديلات نصية قابلة للعكس الكامل.

## Approval

| الحقل | القيمة |
|---|---|
| مُقدِّم المقترح | تدقيق مستقل (جلسة Cowork) |
| التاريخ | 2026-08-28 |
| موافقة الطبيب/ة | APPROVED — 2026-08-28 |
| تاريخ التنفيذ الفعلي | 2026-08-28 |
