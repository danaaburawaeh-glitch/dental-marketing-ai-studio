# استوديو المساعدين — Assistant Studio v1.4.1 — Marketing OS Standalone Edition

نظام محوكَم لبناء وتشغيل وصيانة مساعدين مخصصين داخل Claude لعيادة الأسنان وفريقها التسويقي — بمخطط موحّد، ودورة حياة، وتوجيه حتمي قابل للفحص الآلي، لا اعتماد على أي حساب أو مساعد أو ملف خاص بمُنشئ الحزمة الأصلي.

> **هذه نسخة Standalone بالكامل.** أي مستخدم آخر يستطيع تثبيتها وتشغيلها فوراً: صفر Skill خارجية مطلوبة، صفر Assistant خارجي مطلوب، صفر ملف معرفة خاص مطلوب، صفر اعتمادية خاصة بحساب أحد. الإثبات الآلي الكامل في `DEPENDENCIES.md` و`tests/dependency-scan.py`، والالتزام المعماري في `governance/standalone-guarantee.md`.



## ما الجديد في v1.4.1 — Built-in Update Checker

- مهارة جديدة `system-update-checker` لفحص أحدث إصدار منشور على GitHub.
- مقارنة Semantic Version بين النسخة المثبتة وLatest Release.
- رابط تنزيل ثابت لأحدث نسخة.
- الفحص Read-only: لا يثبت أو يحذف أو يستبدل ملفات تلقائياً.
- عند غياب الإنترنت يصرّح بتعذر الفحص ولا يدّعي أن النسخة محدثة.

## ما الجديد في v1.4.0 — Marketing OS

وسّع هذا الإصدار الاستوديو من منظومة Instagram/Content قوية إلى **Marketing Operating System** يغطي دورة النمو كاملة:

`Strategy → Offer → Campaign → Paid Media → Funnel → Lead Follow-up → ROI`

مع مسار مستقل لـ `Local SEO/GEO`. تمت إضافة 7 Skills جديدة مع اختبارات routing، دون حذف أي Skill سابقة أو كسر وضع Standalone.

## ما هي هذه الإضافة

مجموعة من ٢٨ مهارة (Skill) محوكَمة، مبنية على مخطط بيانات صارم (`governance/assistant-schema.md`) وموجَّهة بمحرّك توجيه حتمي (لا احتمالي) يقرر أي مهارة تُستدعى لكل طلب. كل مهارة تُختبَر آلياً قبل أن تصبح قابلة للاستدعاء، وكل تعديل يمر ببوابة إصدار من عشر خطوات (`governance/release-policy.md`) قبل اعتماده.

### ما تفعله

- **إدارة العيادة والتسويق:** بناء مهارات مخصصة، تحليل أداء Instagram، تخطيط الحملات التسويقية والمحتوى، مراجعة منشورات الحالات قبل النشر، الرد على استفسارات واتساب، جدولة المحتوى.
- **حوكمة ذاتية:** كل مهارة تخضع لسياستين عامتين لا يمكن تجاوزهما (`house-rules`، `clinical-firewall`)، ولاختبار توجيه وسلامة قبل أي ترقية لحالة `ACTIVE`.

### ما لا تفعله عمداً

هذه الإضافة **لا** تبني ولا تُشغّل أي مساعد تشخيص، خطة علاج، تفسير أشعة أو فحوصات، أو أي أداة تتخذ قراراً سريرياً — القرار السريري يبقى بيد الطبيب/ة حصراً، دائماً. أي طلب من هذا النوع يُقصى فوراً بواسطة `identity/clinical-firewall.md`، بصرف النظر عن صياغته. `clinical` · `patient` · `research` ممنوعة بنيوياً كـ`domain` لأي مهارة هنا (`domain_out_of_scope`، مفحوصة آلياً في كل تشغيلة). التفاصيل والحالات الرمادية: `governance/scope-boundary.md`.

## البنية

```
assistant-studio/
├── identity/
│   ├── house-rules.md               GLOBAL_POLICY ١ — يرثها الجميع، لا تُتجاوَز
│   └── clinical-firewall.md         GLOBAL_POLICY ٢ — متى يتوقف المساعد كلياً (نية سريرية)
├── governance/                      وثائق الحوكمة (مخطط، دورة حياة، توجيه، بوابة إصدار، تجميد معماري…)
│   ├── scope-boundary.md            بيان النطاق: عيادة وتسويق فقط، لا سريري
│   ├── assistant-schema.md          المخطط الإلزامي لكل مساعد
│   ├── lifecycle-versioning.md      دورة الحياة والإصدارات الدلالية
│   ├── routing-policy.md            عشر قواعد توجيه مرتَّبة (القاعدة ٠ = الجدار السريري)
│   ├── routing-matrix.md            مصفوفة Intent → Skill كاملة *(جديد v1.3.0)*
│   ├── routing-tests.yaml           ٣٧ حالة اختبار توجيه
│   ├── capability-detection.md      Progressive Enhancement / Manual Execution Mode *(جديد v1.3.0)*
│   ├── standalone-guarantee.md      الالتزام المعماري بصفر اعتماديات *(جديد v1.3.0)*
│   ├── portability.md               سبع قواعد قابلية النقل + الاستثناءات الموثَّقة *(جديد v1.3.0)*
│   ├── release-policy.md            بوابة الإصدار العشرية
│   ├── core-freeze.md               مكوّنات معمارية مجمَّدة (تحتاج ACP للتعديل)
│   ├── evals/regression-baseline.yaml  خط أساس مجمَّد لمنع الانحدار
│   └── proposals/                   اقتراحات تغيير معماري (ACP) موثَّقة
├── scripts/                         أدوات الحوكمة (تحقق، توجيه، تنسيق، ترحيل، جرد)
├── skills/                          ٢٨ مهارة محوكَمة
├── tests/
│   ├── standalone/test_standalone.py   ٦ اختبارات استقلالية *(جديد v1.3.0)*
│   └── dependency-scan.py              ماسح الاعتماديات الآلي *(جديد v1.3.0)*
├── knowledge/                       معرفة مشتركة + دليل مساعدين مولَّد
├── DEPENDENCIES.md                  تدقيق الاعتماديات الكامل *(جديد v1.3.0)*
├── SKILLS-INVENTORY.md              جرد المهارات الكامل *(جديد v1.3.0)*
├── INSTALL.md                       دليل تثبيت أول تشغيلة *(جديد v1.3.0)*
├── CHANGELOG.md                     سجل الإصدارات *(جديد v1.3.0)*
└── README.md
```

## المهارات (٢٨)

| المجال | المهارات |
|---|---|
| `system` (٥) | `system-assistant-builder` · `system-assistant-directory` · `system-knowledge-manager` · `system-assistant-tuner` · `system-assistant-orchestrator` *(TESTING)* |
| `instagram` (١١) | `instagram-funnel-diagnostician` · `instagram-data-analyst` · `instagram-audience-analyst` · `instagram-content-performance-analyst` · `instagram-reel-strategist` · `instagram-personal-brand-strategist` · `instagram-competitor-analyst` · `instagram-experimentation-manager` · `instagram-content-architect` · `instagram-conversion-analyst` · `instagram-weekly-growth-review` |
| `content` (٤) | `content-case-post-reviewer` · `content-whatsapp-lead-responder` *(جديد)* · `content-social-calendar-scheduler` *(جديد)* · `content-short-form-video-planner` *(جديد)* |
| `marketing` (٧) | `marketing-strategy-planner` · `marketing-offer-architect` · `marketing-paid-media-planner` · `marketing-lead-funnel-optimizer` · `marketing-campaign-director` · `marketing-roi-analyst` · `marketing-local-seo-geo-strategist` |
| `sales` (١) | `sales-lead-followup-manager` |

الأربعة المعلَّمة *(جديد)* بُنيت في v1.3.0 لتحل محل ست إحالات كانت تشير خارج الحزمة (`whatsapp-closing-specialist`، `marketing-strategy-director`، `linkedin-strategy`، `social-media-calendar`، `drdana-short-form-video-plan`، `smile-doc-standardizer`) — التفاصيل الكاملة والقرار الهندسي وراء كل واحدة في `DEPENDENCIES.md`. الجرد الكامل بالمدخلات/المخرَجات/الاعتماديات لكل مهارة في `SKILLS-INVENTORY.md`؛ الدليل الآلي المولَّد في `knowledge/assistants-registry.md`.

## الحوكمة

ست قواعد ثابتة منذ Foundation Hardening، ما زالت سارية بلا استثناء:

1. **معرّف كانوني واحد لكل مساعد** — `<domain>-<function>-<role>` · kebab-case · بلا أرقام تسلسلية · ثابت عبر الإصدارات.
2. **المخطط داخل `SKILL.md`** — كتلة `metadata` هي مصدر الحقيقة الوحيد. الدليل يُولَّد منها ولا يُحرَّر يدوياً.
3. **`ACTIVE` وحدها تُوجَّه** — و«`ACTIVE`» تتطلب `last_tested_version == version`. رفع الإصدار يُسقط الاعتماد تلقائياً. `TESTING`/`PILOT`/`DRAFT`/`ARCHIVED` لا تدخل التوجيه بحال، بلا استثناء.
4. **سياستان عامتان فوق الجميع** — `house-rules` (نزاهة المحتوى) و`clinical-firewall` (متى يتوقف المساعد) معاً بـ`override_allowed: false`. لا معرفة ولا مساعد ولا طلب مستخدم يعطّلهما. الـ٢٨ مهارة كلها ترثهما إلزامياً (مفحوص آلياً).
5. **النطاق مضبوط بنيوياً** — `clinical` · `patient` · `research` ممنوعة كـ`domain` داخل هذه الإضافة.
6. **لا تسليم بلا فحص** — `validate_system.py`، `routing_tests.py`، و*(جديد v1.3.0)* `tests/dependency-scan.py` + `tests/standalone/` بوابات إلزامية قبل أي إصدار حزمة كاملة (`governance/release-policy.md` — البوابة العاشرة).

مكوّنات معمارية أساسية (مخطط الـmetadata، خوارزمية التوجيه، مخطط الـhandoff، نموذج دورة الحياة، آلية وراثة السياسات، منطق توليد الدليل، إطار قرار المنسِّق، مخطط المعرفة) **مجمَّدة** — تعديلها يتطلب اقتراح تغيير معماري موثَّق (`governance/core-freeze.md`). إضافة مهارة جديدة مطابقة للمخطط الحالي **لا** تحتاج ACP.

## التوجيه

محرّك توجيه حتمي (لا احتمالي، لا تخمين دلالي): كل طلب يُقاس ضد `triggers`/`negative_triggers` لكل مهارة `ACTIVE`، والمهارة ذات أعلى تطابق (مرجَّح بـ`routing_priority`) تفوز؛ `negative_triggers[].route_to` يُحيل صراحة عند تشابه قريب لمنع الخلط بين مهارات متجاورة (مثال: تحليل بيانات خام مقابل تشخيص قمع التحويل). لا `route_to` أو `can_delegate_to` أو `skill_dependencies` في أي مهارة يشير إلى خارج هذه الحزمة — مفحوص آلياً بـ`tests/dependency-scan.py`. عشر قواعد توجيه مرتَّبة بالكامل، وأولها دائماً: **الجدار السريري يسبق أي توجيه آخر** — في `governance/routing-policy.md`. مصفوفة Intent → Primary Skill → Secondary → Escalation → Out-of-scope الكاملة في `governance/routing-matrix.md` *(جديد v1.3.0)*. ٣٧ حالة اختبار توجيه (إصابة وإقصاء) في `governance/routing-tests.yaml`، ١٠٠٪ دقة توجيه و١٠٠٪ دقة إقصاء في آخر تشغيلة.

## معمارية الاستقلالية (Standalone) — جديد v1.3.0

الالتزام: **صفر اعتمادية Required خارج هذه الحزمة.** أربع ضمانات ملموسة (التفصيل الكامل في `governance/standalone-guarantee.md`):

1. **كل قدرة أساسية داخلية.** لا `route_to`/`can_delegate_to`/`skill_dependencies` يشير لمعرّف غير موجود في `skills/` — مفحوص آلياً.
2. **كل تكامل خارجي اختياري (Progressive Enhancement).** كل مهارة تحتاج أداة خارجية (ChatPlace، Meta Ads، Windsor.ai، Canva، Google Drive/Calendar، WebSearch) تتحقق من توفّرها أولاً؛ عند غيابها تنزل تلقائياً إلى **Manual Execution Mode**: تحليل + توصية + مخرَج جاهز للنسخ اليدوي + الخطوة التالية — أربع نقاط لا تقل عنها أي تشغيلة يدوية. الآلية والجدول الكامل للتكاملات الاختيارية في `governance/capability-detection.md`.
3. **لا معرّف حساب شخصي، لا مسار مطلق، لا رابط خاص.** سبع قواعد قابلية نقل صريحة في `governance/portability.md`.
4. **إثبات آلي، لا وعد نصي.** `tests/dependency-scan.py` يفحص كل ملف في الحزمة (لا `skills/` فقط) عند كل إصدار وينتج رقماً واحداً: `Required unresolved dependencies: 0`. `tests/standalone/test_standalone.py` يحاكي مستخدماً جديداً بلا أي حساب سابق بست اختبارات مسمّاة.

## التكاملات الاختيارية

| التكامل | يُستخدَم في | القدرة عند التوفر | السلوك عند الغياب |
|---|---|---|---|
| ChatPlace (Instagram DM، واتساب) | `content-whatsapp-lead-responder` وعدة مهارات `instagram-*` | قراءة محادثات حية، إرسال ردود مُسوَّدة | Manual Execution Mode — نص جاهز للنسخ + قائمة إرسال يدوي |
| Meta Ads | مهارات تحليل `instagram-*`، `marketing-strategy-planner` | مقاييس حملات حية | Windsor.ai ثم بيانات يُدخلها المستخدم يدوياً |
| Windsor.ai | `instagram-data-analyst`، `instagram-conversion-analyst`، `marketing-strategy-planner` | تحليلات عبر منصات متعددة | Meta Ads أو ChatPlace ثم إدخال يدوي |
| Canva | `content-social-calendar-scheduler`، `content-short-form-video-planner`، `content-case-post-reviewer` | توليد/تصدير أصول بصرية | بريف تصميم مكتوب جاهز لأي مصمم أو للصق اليدوي في Canva |
| Google Drive / Calendar | مهارات `system-*`، `content-social-calendar-scheduler` | تخزين ملفات، تذكيرات جدولة | مخرَج داخل المحادثة، ينسخه المستخدم لأداته |
| WebSearch / WebFetch | عدة مهارات لبحث السوق/المنافسين | بحث ويب حي | يكمل ببيانات مُعطاة مع ذكر الافتراض صراحة |

لا مهارة تستدعي أياً من هذه بلا شرط. الجدول الكامل مع تفاصيل كل مهارة في `DEPENDENCIES.md`.

## التثبيت

دليل كامل خطوة بخطوة لمستخدم جديد في `INSTALL.md`. الخلاصة:

1. ثبّتي الإضافة — لا خطوة إضافية، لا حساب خارجي مطلوب.
2. عبّئي `identity/house-rules.md §١` (اسم العيادة، التخصص، النبرة) — نقطة التخصيص الوحيدة.
3. اقرئي `identity/clinical-firewall.md` و`governance/scope-boundary.md` مرة واحدة.
4. قولي: «وش المساعدين عندي» أو «ابني لي مساعد …» أو أي طلب من `SKILLS-INVENTORY.md`.

## الاختبار

```bash
# البوابة المعتمدة — فحوص الحوكمة والمخطط
python3 scripts/validate_system.py --skills skills \
       --policy identity/house-rules.md --policy identity/clinical-firewall.md

# اختبارات التوجيه — إصابة وإقصاء (٣٧ حالة)
python3 scripts/routing_tests.py --skills skills --tests governance/routing-tests.yaml

# اختبارات التنسيق/الـhandoff/السلامة
python3 scripts/orchestration_tests.py --skills skills

# رسم الاعتماديات — دورات ومراجع مكسورة
python3 scripts/dependency_graph.py --skills skills

# اختبارات الاستقلالية — ٦ حالات (جديد v1.3.0)
python3 tests/standalone/test_standalone.py --skills skills

# ماسح الاعتماديات — Required unresolved dependencies: 0 (جديد v1.3.0)
python3 tests/dependency-scan.py --root .

# صحة النظام الإجمالية
python3 scripts/studio_health.py --root .
```

النتيجة الكاملة لآخر تشغيلة لكل ما سبق في `RELEASE-AUDIT-v1.3.0.md`.

## سجل التحديثات

السجل الكامل بالترتيب الزمني، من مرحلة Foundation Hardening الأولى حتى Standalone Edition. كل تحديث موثَّق بأثره الفعلي على `validate_system.py`/`routing_tests.py` وقت كتابته — سجل هندسي حقيقي لا ملخص لاحق.

## تحديث 1.3.0 — ٢٠٢٦-٠٨-٢٨ — Standalone Edition

طلب صريح: تحويل الحزمة إلى نسخة مستقلة بالكامل، قابلة للتثبيت والتشغيل لدى أي طبيب/ة آخر بلا أي اعتماد على مساعدين أو Skills أو ملفات معرفة خاصة بحساب مُنشئ الحزمة الأصلي، مع الحفاظ على كل قدرة موجودة — بدون بناء Skills وهمية للتعويض.

**تدقيق الاعتماديات (Phase 1):** فحص مستقل تجاوز الأمثلة الثلاثة المُعطاة (`whatsapp-closing-specialist`، `marketing-strategy-director`، `social-media-calendar`) ووجد ٦ إحالات فعلية إلى خارج الحزمة (منها اثنتان إضافيتان: `linkedin-strategy`، `smile-doc-standardizer`) بالإضافة إلى ٨ تسريبات خاصة بالحساب لم تكن مذكورة في الطلب أصلاً (اسم شخصي في `plugin.json`/`README.md`، `owner: dana` في خمسة ملفات، عبارة "قرار دانا" في سكربت مولِّد، ومجلد `roadmap/` كامل يشير لنظام سريري خاص منفصل). التفصيل الكامل جدول-بجدول في `DEPENDENCIES.md`.

**بناء Skills داخلية (Phase 3):** أربع مهارات جديدة فقط — لا خمس، ولا وهمية — استخرجت الوظيفة الفعلية من كل تبعية بدل استبدالها باسم بديل: `content-whatsapp-lead-responder`، `marketing-strategy-planner` (يستوعب أيضاً لينكدإن كقناة واحدة بدل مهارة منفصلة)، `content-social-calendar-scheduler`، `content-short-form-video-planner`. قدرة توحيد صور الحالة (كانت تحال لـ`smile-doc-standardizer` الخارجية) دُمجت داخل `content-case-post-reviewer` الموجودة بدل مهارة خامسة منفصلة — تفادياً للتضخم. كل مهارة جديدة اتبعت نفس مخطط `assistant-schema.md` تماماً (لا تحتاج ACP)، وحملت `policy_dependencies: [house-rules, clinical-firewall]` إلزامياً منذ الإنشاء.

**تعميم البنية (Phase 2):** `plugin.json` (المؤلّف والوصف)، `README.md` (البايلاين)، خمسة ملفات `owner: dana` → `owner: clinic-owner`، عبارة "قرار دانا" في `scripts/build_migration_map.py`، ومجلد `roadmap/clinical-core-plan.md` بالكامل (صفر اعتمادية تشغيلية من أي مساعد — تحقُّق مباشر قبل الحذف) استُبعد من الحزمة.

**حوكمة جديدة (Phase 4):** أربع وثائق: `governance/standalone-guarantee.md` (الالتزام المعماري)، `governance/portability.md` (سبع قواعد قابلية نقل + استثناءات موثَّقة)، `governance/capability-detection.md` (تصنيف Progressive Enhancement رسمي لنمط "مصادر البيانات" الموجود أصلاً في مهارات `instagram/*`)، `governance/routing-matrix.md` (مصفوفة Intent → Skill كاملة). بوابة إصدار جديدة (العاشرة) في `governance/release-policy.md` تُلزم بتشغيل `tests/dependency-scan.py` + `tests/standalone/` قبل أي تعبئة حزمة. تحديث ٣ حالات في `governance/evals/regression-baseline.yaml` المجمَّد عبر اقتراح تغيير معماري موثَّق (`governance/proposals/2026-08-28-standalone-external-reference-removal.md`) — لا تجاوز صامت لقاعدة التجميد.

**الاختبار (Phase 5):** تسع مهارات (خمس مُعدَّلة + أربع جديدة) مرَّت بدورة ترقية `TESTING → ACTIVE` كاملة عبر أدوات المشروع الحقيقية (`routing_tests.py --assume-tested` → `stamp_tested.py` → `validate_system.py` → `routing_tests.py` بلا العلَم). نتيجة نهائية حقيقية: **37/37** اختبار توجيه، **100٪** دقة توجيه وإقصاء. `tests/standalone/test_standalone.py` جديد — ٦ اختبارات مسمّاة (Test 1–6) كلها PASS. `tests/dependency-scan.py` جديد — يفحص كل ملف في الحزمة (لا `skills/` فقط) عن مسارات مطلقة وأسرار وأسماء شخصية وروابط خاصة، ونتيجته: **Required unresolved dependencies: 0** — التقط أثناء التطوير نفسه قيمة افتراضية متبقية `owner: "dana"` في `scripts/migrate.py` وست إشارات نصية تاريخية في حقول `notes:` لملفات SKILL.md، وأُصلحت جميعها.

**نتيجة صافية:** ١٧ → ٢١ مهارة (+٤ داخلية، صفر خارجية جديدة). Required external skills/assistants/private-knowledge/account-specific = **0/0/0/0** — التفاصيل والإثبات الآلي الكامل في `DEPENDENCIES.md` و`RELEASE-AUDIT-v1.3.0.md`. الفجوتان المعروفتان المتبقيتان (حالتا `regression-baseline.yaml` القديمتان لـ`dana-instagram-growth-director`، وغياب مهارة مخصصة لنطاق "SOP إدارية" لم يكن موجوداً أصلاً في v1.2.1) سابقتان لهذه الترقية وخارج نطاقها — موثَّقتان بصراحة في `RELEASE-AUDIT-v1.3.0.md` بدل إخفائهما.

## الحالة

`PASS WITH WARNINGS` · ٢٧ فحصاً ناجحاً (أُضيف `domain_out_of_scope`) · ٢٩ اختبار توجيه ناجحاً · ٩ من ١٠ معايير نجاح محقَّقة — نفس ملف التنبيهات (١٠ مراجع خارجية لمهارات حساب غير مُرحَّلة)، صفر أخطاء جديدة بعد فصل العيادة/التسويق.
البند المفتوح: حذف النسخ القديمة من الحساب — خطوة يدوية لا تملكها الأدوات.

## تحديث 1.1.1 — ٢٠٢٦-٠٨-٢٨

تدقيق مستقل كشف أن محرّك التوجيه الفعلي (Cowork/Claude) يقرأ حقل `description` فقط عند اختيار مهارة، لا `metadata.status` — فمهارة `TESTING` كانت تُستدعى بلا أي تمييز عن `ACTIVE`. أُصلح عبر وسم إلزامي `[STATUS: ...]` في بداية `description` لأي مساعد غير `ACTIVE`، مع فحص آلي جديد (`description_reflects_status`) يمنع تكرار الخطأ. التفاصيل الكاملة والاختبار: `governance/proposals/2026-08-28-description-status-visibility.md`. لا تغيير في عبارات التشغيل ولا في نتائج `routing_tests.py` (لا تزال 29/29). **معتمَد من الطبيب/ة — ٢٠٢٦-٠٨-٢٨.**

## تحديث 1.1.2 — ٢٠٢٦-٠٨-٢٨

فجوة ثانية من نفس التدقيق: ثلاث مهارات نظام (`system-assistant-directory`، `system-assistant-builder`، `system-knowledge-manager`) كانت تعليماتها تفترض أدوات `project_read`/`project_write` وملف `knowledge/INDEX.md` — وهذه خاصة ببيئة Claude.ai «Project» ولا وجود لها في Cowork. النتيجة الفعلية: مساعد يُطالَب بقراءة/كتابة شيء غير موجود، فيرتجل أو يفشل بصمت.

الإصلاح: كل موضع project_read حُوّل إلى `Read` مباشر على `${CLAUDE_PLUGIN_ROOT}/knowledge/...` (مع `ListSkills` مُصفّاة كبديل احتياطي)، وكل موضع project_write حُوّل إلى توليد محلي بالأداة الفعلية القائمة (`build_registry.py` / `build_knowledge_index.py`) متبوعاً بتسليم صريح عبر `SendUserFile` وتعليمات إعادة رفع واضحة — لا ادّعاء بأن شيئاً "تحدَّث في الحساب" قبل أن يحدث ذلك فعلياً. فهرس المعرفة أصبح `knowledge/generated-index.md` المولَّد آلياً بدل `knowledge/INDEX.md` اليدوي المفترَض. `validate_system.py`: صفر أخطاء جديدة (نفس ١١ تنبيهاً). `routing_tests.py`: 29/29 دون تغيير. التفاصيل في حقل `notes` لكل مساعد من الثلاثة.

## تحديث 1.1.3 — ٢٠٢٦-٠٨-٢٨

رفع حزمة 1.1.2 فعلياً على حسابك فشل برسالة حقيقية من واجهة رفع الإضافات: **"Skill 'skills/system-assistant-orchestrator': field 'description' in SKILL.md must be at most 1024 characters"**. السبب: وسم `[STATUS: TESTING]` المُضاف في تحديث 1.1.1 دفع طول `description` إلى 1038 حرفاً — تجاوز حداً فعلياً في منصة Cowork لا يوثّقه أي ملف حوكمة هنا، فمرّ محلياً عبر `validate_system.py` وفشل فقط عند الرفع الحقيقي.

الإصلاح: اختُصر نص شرح `TESTING` في وصف `system-assistant-orchestrator` إلى 905 حرفاً دون مسّ أي عبارة تشغيل مقتبَسة أو الوسم نفسه، وأُضيف فحص جديد `description_length` إلى `validate_system.py` يرفض أي `description` أطول من 1024 حرفاً **محلياً قبل الرفع** — لا بعده. كذلك صُحح حقل `tool_dependencies: [projects]` المتبقّي في هذا المساعد إلى `plugin-files` (نفس تصحيح تحديث 1.1.2، كان قد فات هذا الملف تحديداً). `validate_system.py`: صفر أخطاء (نفس التنبيهات). `routing_tests.py`: 29/29 دون تغيير.

**الدرس:** فحوص هذا النظام الآلية (`validate_system.py`) تتحقق من قواعد حوكمته الداخلية فقط — لا من كل قيد فعلي تفرضه منصة Cowork وقت الرفع. حد الـ 1024 حرفاً أُضيف الآن كفحص دائم، لكن قد توجد قيود مشابهة غير مكتشَفة بعد لن تظهر إلا برفع حقيقي يفشل.

## تحديث 1.1.4 — ٢٠٢٦-٠٨-٢٨

من بقية بنود التدقيق: `validate_system.py` كان يصدر تحذير `orphan_assistant` كاذباً على `system-assistant-orchestrator` — يشتكي أنه "بلا مرجع وارد ولا صادر" رغم أن هذا تصميم مقصود وموثَّق في `handoff_contract.notes` الخاص به: الـ Orchestrator يستهدف أي مساعد `ACTIVE` في الدليل الحي وقت التشغيل، لا مجموعة مقفلة في `can_delegate_to`. أُصلح باستثناء `role: orchestrator` صراحة من هذا الفحص، مع تعليق يشرح السبب. التحذيرات صارت 10 بدل 11. `routing_tests.py`: 29/29 دون تغيير.

**تحذيرات `external_reference` العشرة المتبقية (`dana-instagram-growth-director`، `smile-doc-standardizer`، `whatsapp-closing-specialist`، وغيرها) ليست خطأ يُصلَح كوداً** — تحققت من `governance/migration-spec.yaml § T3_dana_authored_ungoverned`: هذه مهارات كتبتها الطبيب/ة فعلياً قبل الاستوديو، موجودة في حسابها، وقرار تأجيل ترحيلها لمرحلة ثانية موثَّق بسبب وتاريخ محددين لكل واحدة (`action: KEEP`/`REVIEW`، `unblock_condition`). إعادة تسمية أي منها الآن يكسر مراجع نصية متبادلة لا نملك تعديلها في هذه المرحلة. ما يحتاجه هذا البند فعلياً قرار من الطبيب/ة لا كود: هل هذه السبع مهارات ما زالت موجودة بأسمائها في حسابها اليوم (التقرير كُتب ٢٠٢٦-٠٨-٢١)، وهل تريد البدء بترحيل المرحلة الثانية الآن.

## تحديث 1.1.5 — ٢٠٢٦-٠٨-٢٨

بطلبك تحققت مباشرة عبر `ListSkills` من السبع مهارات الخارجية بدل الاكتفاء بالتخمين. النتيجة: ست منها (`smile-doc-standardizer`، `social-media-calendar`، `drdana-short-form-video-plan`، `whatsapp-closing-specialist`، `marketing-strategy-director`، `linkedin-strategy`) موجودة فعلاً بنفس الاسم — تحذيراتها في `validate_system.py` دقيقة، لا تغيير. أما `dana-instagram-growth-director` فغير موجود إطلاقاً — لا بهذا الاسم ولا بأي نسخة قديمة مرقّمة. كان مرجعاً حياً في description وnegative_triggers لثلاث مهارات (`instagram-data-analyst`، `instagram-funnel-diagnostician`، `instagram-weekly-growth-review`)، فيُحيل طلب "استراتيجية ٩٠ يوماً" إلى مساعد ميت. صُحح: description لم يعد يذكره، وroute_to صار `system-assistant-builder` (لا مساعد يغطي هذا النطاق حالياً — يُبنى عند الحاجة).

أثناء هذا الفحص اكتشفت أن إصلاح project_read/project_write (تحديث 1.1.2) لم يكن كاملاً: `instagram-weekly-growth-review` كان لا يزال يستخدم `project_write` فعلياً في قسم الأرشفة، وستة مهارات أخرى (البيانات، الجمهور، المنافسون، بنية المحتوى، أداء المحتوى، التحويل، التجارب، الريلز) كانت تصف مصدر بيانات رابع باسم "الـ Project" في نص وصفي غير تنفيذي لكن غير دقيق. صُححت الجميع لتشير إلى `${CLAUDE_PLUGIN_ROOT}/knowledge/` الفعلي، وصُحح `tool_dependencies: [projects]` المتبقي في خمس مهارات إلى `plugin-files`. كذلك صُححت ملفات القوالب المرجعية (`TEMPLATE-SKILL.md`، `authoring-rules.md`، `registry-template.md`) حتى لا يرث أي مساعد جديد يُبنى لاحقاً نفس الافتراض الخاطئ.

**الدرس المتكرر:** كل مرة أعلن فيها هذا التقرير أن فئة مشكلة "أُغلقت"، اكتشاف لاحق يكشف نسخة أخرى منها لم تُفحص. `validate_system.py` لا يملك فحصاً آلياً يرصد "الـ Project"/`project_read`/`project_write` نصياً عبر كل الملفات — الاعتماد ظل على `grep` يدوي كل مرة، وهذا نفسه خطر تكرار. `validate_system.py`: صفر أخطاء (7 تنبيهات — انخفضت من 10). `routing_tests.py`: 29/29 بعد تحديث حالتي اختبار في `governance/routing-tests.yaml` كانتا تتوقعان `dana-instagram-growth-director` صراحة.

## تحديث 1.1.6 — ٢٠٢٦-٠٨-٢٨

`content-case-post-reviewer` رُقّيت من TESTING إلى ACTIVE — أول ترقية فعلية عبر المسار الذي تنص عليه `governance/lifecycle-versioning.md`، لا يدوياً. المهارة شُغّلت على حالة حقيقية من حساب الطبيب/ة (كابشن ريل فعلي عن الإحساس بتغيّر النطق بعد الفينيرز)، وأنتجت مراجعة حقيقية:

- بوابة الموافقة اشتغلت كما هو مصمَّم لها: قبل أي مراجعة للنص، سألت هل يظهر في الفيديو مريضة/حالة فعلية أم الطبيب/ة فقط تتحدث للكاميرا، وهل الموافقة الخطية موثّقة — ولم تكمل المراجعة قبل الإجابة.
- بعد تأكيد أن لا مريضة تظهر ولا تمويل إعلاني، المراجعة أمسكت مشكلتين حقيقيتين كانتا لتمران بسهولة: ادعاء فعالية علمي («تسرّع التأقلم بشكل ملحوظ») بلا مصدر يدعمه، ووصفاً قاطعاً لمدة تأقلم فردية بلا تنويه بالفروق بين الحالات.
- الطبيب/ة اطّلعت على المخرَج واعتمدته صراحةً كتشغيلة التأهيل الرسمية (لم أُرقِّ الحالة من تلقاء نفسي بمجرد تشغيلها).

description جُرِّد من بادئة `[STATUS: TESTING]` (لم يعد بحاجتها بعد الاعتماد)، والـ metadata حُدِّثت (`status: ACTIVE`، `version: 1.2.0`، `last_tested_version: 1.2.0`). حالة اختبار توجيه واحدة في `governance/routing-tests.yaml` كانت تتوقع صراحةً `NO_MATCH` لعبارة "راجعي المنشور قبل النشر" طالما المهارة TESTING — حُدِّثت لتتوقع `content-case-post-reviewer` الآن. `validate_system.py`: صفر أخطاء (7 تنبيهات، بلا تغيير — كلها `external_reference` مؤجَّلة بحوكمة موثَّقة). `routing_tests.py`: 29/29. توزيع الحالة عبر الـ17 مهارة: ACTIVE 15 → 16، TESTING 2 → 1 (المتبقي: `system-assistant-orchestrator`، بانتظار تشغيلة تنسيق حقيقية معتمَدة من الطبيب/ة بنفس الطريقة).

بهذا يُغلق آخر بند حقيقي كان معلَّقاً من تقييم "تدقيق Assistant Studio" الأصلي، إلى جانب قاعدة المعرفة الفارغة التي تبقى مؤجَّلة عمداً بقرار الطبيب/ة (`أجّليها`) لأنها تتطلب بياناتها الحقيقية.

## تحديث 1.2.0 — ٢٠٢٦-٠٨-٢٨ — تعميم القالب لإعطائه لأطباء آخرين

بطلب صريح: إزالة كل ما يربط هذا الاستوديو باسم طبيب/ة بعينه/ها، حتى يمكن إعطاء نسخة منه لطبيب/ة آخر بلا تسريب هوية الطبيب/ة الأول/ى.

**إعادة الهندسة، لا مجرد حذف نص:** المشكلة الأعمق لم تكن فقط أن اسم الطبيب/ة ولقبه/ا الكامل كانا مكتوبين حرفياً في أماكن كثيرة — بل أن كل مساعد من الـ١١ في `instagram/` كان يحمل **نسخة مطابقة، مكرَّرة يدوياً**، من فقرة الهوية والنبرة الكاملة (الاسم، التخصص، المدينة، قائمة الكلمات الممنوعة). هذا يعني أن أي تغيير مستقبلي في الهوية (حتى تغيير بسيط) كان سيحتاج تعديل ١٢ ملفاً يدوياً ليبقى النظام متسقاً — وهو بالضبط نوع الخطأ المتكرر الذي وثّقته تحديثات 1.1.5 و1.1.2 سابقاً في هذا الملف.

**الإصلاح البنيوي:** `identity/house-rules.md §١` (البروفايل) هو الآن **نقطة التخصيص الوحيدة** — حقول `⟨املئيه⟩` بدل بيانات فعلية. كل مساعد يرث الهوية منه تلقائياً عبر `policy_dependencies: [house-rules]` (كانت هذه التبعية معلَنة أصلاً في كل مساعد، لكن النص كان يُكرَّر يدوياً فوقها بدل الاعتماد عليها فعلياً). فقرة "## النبرة" المكرَّرة في ١١ مهارة استُبدلت بسطر إحالة واحد لكل ملف. لإعطاء الاستوديو لطبيب/ة آخر الآن: **عبّئي `identity/house-rules.md §١` فقط** — لا حاجة لفتح أي ملف مساعد.

**نطاق التنظيف:** ٤٠ ملفاً كانت تذكر الاسم أو اللقب أو معرّف انستغرام أو رابط واتساب فعليَّين — جميعها الآن صفر إشارات مباشرة (تحقَّق ببحث نصي شامل بعد كل تعديل). `owner: dana` في كل ملف تحوّل إلى دور عام `clinic-owner`. مؤلّف الإضافة في `plugin.json` صار "Assistant Studio" بدل الاسم الشخصي. ملفات `knowledge/shared/*.md` (فارغة أصلاً كقوالب DRAFT) صُححت لتشير لـ"الطبيب/ة" بدل الاسم. رابط ريل انستغرام حقيقي كان مذكوراً في تحديث 1.1.6 السابق أُزيل من هذا الملف.

**ما لم يُغيَّر عمداً:** المفردات الخاصة بطب الأسنان والسياق السعودي (PDPL، CST، SFDA، المصطلحات السريرية) بقيت كما هي — الافتراض أن "أطباء آخرين" يعني زملاء في نفس التخصص لا تعميماً لأي تخصص طبي؛ إن كان القصد أوسع فهذا يحتاج مراجعة منفصلة لقاموس `domain_vocabulary` وقواعد `clinical-firewall.md` نفسها. مستندات التخطيط الداخلي (`roadmap/clinical-core-plan.md`, `SYSTEM_HARDENING_REPORT.md`) كانت تحتفظ بإشارات لاسم نظام "Dana-DIOS" — اسم منتج/نظام منفصل تماماً عن هذه الإضافة، لا اسم شخص. **تحديث v1.3.0:** الاستبعاد المذكور هنا كخيار مستقبلي سهل نُفِّذ فعلاً — `roadmap/` حُذف بالكامل من الحزمة (كان بلا أي اعتمادية تشغيلية من أي مساعد)، و`SYSTEM_HARDENING_REPORT.md` عُمِّم. التفاصيل في § تحديث 1.3.0 أدناه. `validate_system.py`: صفر أخطاء (نفس ٧ تنبيهات). `routing_tests.py`: 29/29 — لم يتأثر التوجيه لأن التعديل نصي بحت في محتوى غير مقروء آلياً بواسطة محرّك التوجيه.

---

الإصدار 1.3.0 · Standalone Edition — صفر اعتماديات خارجية، +4 مهارات داخلية · 2026-08-28

الإصدار 1.1.5 · تحقق مباشر من مراجع خارجية + إغلاق فعلي (لا جزئي) لفجوة project_read/write · 2026-08-28
الإصدار 1.1.4 · إصلاح تحذير orphan_assistant الكاذب على orchestrator · 2026-08-28
الإصدار 1.1.3 · إصلاح رفض رفع فعلي (حد 1024 حرفاً على description) · 2026-08-28
الإصدار 1.1.2 · إصلاح افتراضات project_read/project_write غير الموجودة في Cowork · 2026-08-28
الإصدار 1.1.1 · إصلاح فجوة إنفاذ الحوكمة · 2026-08-28
الإصدار 1.0.0 · مرحلة Foundation Hardening · 2026-08-21
