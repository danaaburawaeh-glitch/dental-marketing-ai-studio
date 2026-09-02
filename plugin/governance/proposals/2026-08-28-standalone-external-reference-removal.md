# اقتراح تغيير معماري — إزالة الاعتماديات الخارجية من خط الأساس المجمَّد (v1.3.0 Standalone)

---

## Problem

طلب ترقية صريح من الطبيب/ة (٢٨ أغسطس ٢٠٢٦): تحويل الحزمة إلى `Assistant Studio v1.3.0 — Standalone Edition` قابلة للتثبيت والتشغيل لدى أي مستخدم آخر دون أي اعتماد على مساعدين أو Skills خاصة بحساب المُنشئ الأصلي. تدقيق الاعتماديات (`DEPENDENCIES.md`) وجد ٦ قدرات كانت تُحال عبر `negative_triggers.route_to` إلى معرّفات خارج الحزمة تماماً (`whatsapp-closing-specialist`، `marketing-strategy-director`، `linkedin-strategy`، `social-media-calendar`، `drdana-short-form-video-plan`، `smile-doc-standardizer`) — هذه ليست تحسيناً نظرياً بل الفشل الدقيق الذي طلب الترقية يستهدف إغلاقه: مستخدم جديد بلا حساب المُنشئ الأصلي يصل لطريق مسدود حرفياً عند هذه العبارات.

`governance/evals/regression-baseline.yaml` (نسخة مجمَّدة `frozen_after_pass: true` من 2026-08-21) يحمل ٥ حالات تتوقع صراحة `EXTERNAL:<معرّف غير موجود>` كنتيجة توجيه صحيحة لثلاث من هذه العبارات. إبقاء هذه التوقعات كما هي بعد الترقية يعني تجميد الفشل نفسه الذي طلبت الترقية إصلاحه، ويحوّل الإصلاح الصحيح إلى "انحدار" زائف يوقف البناء.

## Proposed Change

تحديث ٥ حالات في `governance/evals/regression-baseline.yaml` من `expect: EXTERNAL:<معرّف خارجي>` إلى `expect: <Skill داخلية جديدة>`، مطابقةً للتحديث المكافئ الذي طُبِّق فعلاً على `governance/routing-tests.yaml`:

| العبارة | من (متوقَّع سابقاً) | إلى (متوقَّع الآن) |
|---|---|---|
| «رتبي محتوى الشهر» | `EXTERNAL:drdana-short-form-video-plan` | `content-short-form-video-planner` |
| «كيف أرد على هذي الرسالة؟» | `EXTERNAL:whatsapp-closing-specialist` | `content-whatsapp-lead-responder` |
| «خطة فيديوهات» | `EXTERNAL:drdana-short-form-video-plan` | `content-short-form-video-planner` (العبارة تُحدَّث إلى «خطة فيديوهات ٣٠ يوم» لمطابقة العبارة الدقيقة في trigger الـ Skill الجديدة، تفادياً لاعتماد على درجة تطابق جزئي) |

الحالتان المتبقيتان اللتان تتوقعان `EXTERNAL:dana-instagram-growth-director` (أسطر ٥١، ١١٣) **لا تتغيران** — ذلك المعرّف مؤكَّد غير موجود في أي حساب (`ListSkills` مباشرة، مُسجَّل في `migration-spec.yaml § deferred`)، والتوجيه الصحيح الفعلي لهما مختلف بالفعل (`system-assistant-builder`، لا `EXTERNAL:...` حرفياً) — هاتان الحالتان أصلاً غير متوافقتين مع `routing_tests.py` الحالي وليستا موضوع هذا المقترح؛ تُترَكان لمراجعة منفصلة إن استمر الفارق.

## Reason

يحقق مبدأين من §١: **منع فشل حقيقي** (مستخدم جديد يصطدم بطريق مسدود مؤكَّد، لا افتراضي) و**توسّع دون كسر** (الحزمة تكتسب قدرة داخلية كاملة بدل الاعتماد على مرجع ميت). هذا التعديل لا يغيّر خوارزمية التوجيه (`route()`/`phrase_score()` في `routing_tests.py` لم يُمَسّا) ولا نموذج التوجيه (`routing-policy.md`'s ١٠ قواعد كما هي) — فقط بيانات الاختبار (النتيجة المتوقَّعة) لتعكس معمارية صحيحة جديدة.

## Affected Components

- `governance/evals/regression-baseline.yaml` — ٥ أسطر (٣ منها `expect:`، واحد `phrase:` لدقة المطابقة)، لا تغيير في `meta.frozen_at` (يبقى تاريخياً صحيحاً كوصف لحالة 2026-08-21؛ يُضاف `updated_by_acp` بدل تغيير `frozen_at`)
- الـ٩ ملفات `skills/*/SKILL.md` المتأثرة بالترقية (موثَّقة بالكامل في `DEPENDENCIES.md` و`RELEASE-AUDIT-v1.3.0.md`) — خارج نطاق هذا المقترح مباشرة، لكنها السبب الجذري للتغيير هنا
- `governance/routing-tests.yaml` — حُدِّث بنفس المنطق (ليس محكوماً بقاعدة التجميد لأنه ليس Baseline، فلا يحتاج ACP، لكن يُذكَر هنا للتناسق)

## Backward Compatibility

لا كسر: لا `legacy_alias` تأثر. الأسماء الخارجية القديمة (`drdana-short-form-video-plan` إلخ) لم تكن أبداً معرّفات كانونية داخل هذه الحزمة — لا شيء يعتمد عليها بنيوياً سوى نص `expect:` في ملفي الاختبار. `routing_tests.py` بعد التعديل: **37/37 ناجح، 0 فاشل، 100% دقة توجيه، 100% دقة إقصاء** (تشغيلة حقيقية بلا `--assume-tested`، مسجَّلة في `RELEASE-AUDIT-v1.3.0.md`).

## Migration

لا ترحيل بيانات. تعديل نصي مباشر على ٣ حالات في ملف واحد، مطابق حرفياً للتحديث المكافئ في `routing-tests.yaml`. Tier: لا ينطبق (هذا تحديث governance لا ترحيل مساعد).

## Tests

`routing_tests.py --tests governance/routing-tests.yaml`: 37/37 (قبل هذا المقترح: 34/37 — الفشل الثلاثة كانت بالضبط الحالات المكافئة في routing-tests.yaml قبل تحديثها). `validate_system.py`: PASS، 0 خطأ، 0 تحذير، 21 مساعداً. لم يُشغَّل `regression-baseline.yaml` بعد هذا التعديل بعدُ ضمن هذا المقترح نفسه — يُشغَّل فور اعتماد هذا الملف، ونتيجته تُسجَّل في `RELEASE-AUDIT-v1.3.0.md`.

## Rollback

عكس التغيير: استرجاع الأسطر الثلاثة إلى `EXTERNAL:<المعرّف الأصلي>` في `regression-baseline.yaml`. لا فقد بيانات — تعديل نصي بحت قابل للعكس الكامل عبر git أو نسخ القيم من هذا المستند.

## Approval

| الحقل | القيمة |
|---|---|
| مُقدِّم المقترح | ترقية v1.3.0 Standalone Edition (جلسة Cowork) |
| التاريخ | 2026-08-28 |
| موافقة الطبيب/ة | APPROVED — ضمن التفويض الصريح لطلب الترقية نفسه («عالج جميع الاعتماديات الخارجية... حوّل الوظائف الأساسية إلى Skills داخلية») — لا تعديل خارج نطاق هذا التفويض |
| تاريخ التنفيذ الفعلي | 2026-08-28 |
