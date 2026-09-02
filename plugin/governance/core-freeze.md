---
document: core-freeze
type: GOVERNANCE
version: 1.0.0
status: ACTIVE
applies_to: ALL_ASSISTANTS
---

# تجميد المعمارية الأساسية — Core Freeze v1.0.0

**هذا الملف يُفعَّل فقط بعد نجاح بوابة الإصدار الكاملة لمرحلة System Hardening** (`governance/release-policy.md`، تسع بوابات، جميعها PASS) — انظر `SYSTEM_HARDENING_REPORT.md` للحالة الفعلية وقت التفعيل. من لحظة تفعيله: أي تغيير على المكوّنات المجمَّدة أدناه **يمر إلزامياً** عبر `governance/templates/architecture-change-proposal.md`، لا عبر تعديل مباشر — حتى لو كان التعديل صغيراً أو "تحسيناً واضحاً". هذا يمنع بالضبط ما حذّر منه توجيه Hardening: إعادة تصميم الجوهر مرة أخرى بدل البناء فوقه.

التجميد لا يعني التوقف — يعني أن **التغيير على هذه الطبقة تحديداً** يحتاج مبرراً موثَّقاً (أحد مبادئ §١ في توجيه Hardening) وموافقة بشرية صريحة، بينما البناء فوقها (مساعدون جدد، معرفة جديدة، تحسينات نصية) يستمر بلا احتكاك.

## المكوّنات المجمَّدة — Frozen Components

| # | المكوّن | الملف/الآلية المرجعية | ما يعنيه "مجمَّد" هنا |
|---|---|---|---|
| 1 | مخطط الـ metadata الكانوني | `governance/assistant-schema.md` — الحقول الإلزامية، `assistant_id` pattern، المفردات المضبوطة (`domain`, `role`, `safety_level`) | لا حقل جديد إلزامي، لا حذف حقل موجود، لا تغيير صيغة `assistant_id` دون ACP |
| 2 | نموذج التوجيه | `governance/routing-policy.md` (٩ قواعد) + خوارزمية `route()`/`phrase_score()` في `scripts/routing_tests.py` | ترتيب الأولوية، منطق الاستبعاد قبل المطابقة، آلية كسر التعادل — لا تُعاد كتابتها دون ACP |
| 3 | مخطط الـ handoff | `governance/handoff-schema.yaml` — بنية `handoff:`، `status_codes` الثمانية، `validation_rules` | إضافة `status_code` جديد أو حقل جديد للبنية = تغيير معماري، لا إضافة حرة |
| 4 | نموذج الحالات ودورة الحياة | `governance/lifecycle-versioning.md` — الحالات الست (DRAFT/TESTING/PILOT/ACTIVE/DEPRECATED/ARCHIVED)، شرط `last_tested_version == version` لـ ACTIVE، انضباط SemVer | لا حالة جديدة، لا تغيير لشرط دخول ACTIVE، دون ACP |
| 5 | وراثة السياسة العامة | آلية `policy_dependencies` + `house-rules.md`/`clinical-firewall.md` كسياستين عامتين بـ `override_allowed: false` و`priority: HIGHEST` | لا سياسة عامة ثالثة، لا تغيير لقاعدة "لا اختراق"، دون ACP — تعديل *محتوى* السياستين نفسه يبقى ممكناً بالمسار العادي (هو ملف سياسة، لا مخطط بنيوي) |
| 6 | منطق توليد الدليل | `scripts/build_registry.py` — شكل الجدول، مصادر الحقول، معالجة `legacy_aliases`/`deferred` | تغيير شكل المخرَج أو مصدر أي عمود = تغيير معماري |
| 7 | إطار قرار المنسّق | `skills/system-assistant-orchestrator/SKILL.md` §ج (قرار مفرد-vs-متعدد)، §ز (حل التعارض ٦ خطوات)، أكواد التوقف الرسمية | لا تُضاف طبقة قرار جديدة ولا يُعاد ترتيب خطوات حل التعارض دون ACP؛ **حدود التنفيذ الرقمية** (`governance/orchestrator-config.yaml`) مستثناة جزئياً — رفعها قرار حوكمة موثَّق لكنه أخف من ACP كامل (انظر تعليق الملف نفسه) |
| 8 | مخطط ملفات المعرفة | `governance/knowledge-schema.md` — الحقول الإلزامية، الحالات الخمس | نفس منطق المكوّن ١ لكن لطبقة المعرفة |

## ما يبقى قابلاً للتعديل بلا ACP — Allowed Modifications

هذه الأنشطة **تستهلك** المعمارية المجمَّدة أعلاه ولا **تغيّرها** — تستمر بالمسار العادي (تعديل مباشر → `validate_system.py` → `routing_tests.py` → بوابة الإصدار):

- إضافة مساعد جديد يتبع `assistant-schema.md` الحالي كما هو (لا حقل جديد).
- إضافة/تعديل محتوى ملفات معرفة تتبع `knowledge-schema.md` الحالي كما هو، بما فيها ملء حقول `⟨املئيه⟩` في ملفات `knowledge/shared/*` الحالية.
- تعديل نص/محتوى جسم أي `SKILL.md` (بروزا، أمثلة، جداول) دون لمس حقول الـ metadata البنيوية.
- ترقيات SemVer عادية (patch/minor) وفق `lifecycle-versioning.md` كما هو، بما فيها انتقالات الحالة (DRAFT→TESTING→ACTIVE) عبر بوابة الإصدار القائمة.
- إضافة حالات اختبار جديدة إلى أي ملف `governance/evals/*.yaml`.
- إضافة `legacy_aliases`/`negative_triggers` لمساعد قائم — هذه بيانات ضمن المخطط الحالي، لا تغيير للمخطط.
- إضافة مساعدين مستقبليين لإضافة Clinical Core منفصلة مستقبلية (خارج نطاق هذه الحزمة) — طالما يتبعون نفس المخطط المجمَّد أعلاه حرفياً ولا يوسّعون نطاق `assistant-studio` نفسه إلى قرار سريري (انظر `governance/scope-boundary.md`).

## عملية التغيير المعماري — Breaking-Change Process

أي تغيير لا يقع ضمن "ما يبقى قابلاً للتعديل" أعلاه:

1. يُنسَخ `governance/templates/architecture-change-proposal.md` إلى `governance/proposals/YYYY-MM-DD-<وصف-مختصر>.md` ويُملأ كاملاً — تحديداً حقل *Reason* (يجب أن يحقق أحد مبادئ §١ السبعة في توجيه Hardening، وإلا لا يُقدَّم المقترح أصلاً).
2. لا يُنفَّذ أي كود قبل موافقة بشرية صريحة على المقترح (الطبيب/ة أو من تفوّضه) — لا يوجد مسار "موافقة تلقائية" لتغيير معماري، بصرف النظر عن مدى وضوح الفائدة الظاهرة.
3. بعد الموافقة: التنفيذ يتبع نفس بوابة الإصدار العادية (`release-policy.md`) بإضافة بند فحص خاص بالتوافق مع المقترح المعتمَد.
4. سجل كل مقترح (معتمَد أو مرفوض) يبقى في `governance/proposals/` كأرشيف قرار — لا حذف.

## سجل التحديث

| التاريخ | ما تغيّر |
|---|---|
| 2026-08-21 | إنشاء الملف — تفعيل تجميد الجوهر بعد نجاح مرحلة System Hardening |
