---
document: release-policy
type: GOVERNANCE
version: 1.1.0
status: ACTIVE
applies_to: ALL_ASSISTANTS
---

# بوابة الإصدار — Release Gate v1.1.0

**هذا الملف لا يُدخل قاعدة جديدة.** البوابة موجودة إجرائياً منذ مرحلة Foundation Hardening (`validate_system.py` → `routing_tests.py` → `stamp_tested.py`). هذا الملف يُثبِّتها كوثيقة سياسة رسمية بترتيب صريح ومعايير نجاح مرقَّمة، حتى لا تُشغَّل الخطوات بترتيب مختلف أو تُتجاوَز خطوة سهواً.

## القاعدة الحاكمة

> لا مساعد يصبح `ACTIVE` — ولا يبقى `ACTIVE` بعد أي تعديل — إلا بعد اجتياز كل بوابة أدناه بالترتيب. أول بوابة تفشل توقف السلسلة.

## البوابات بالترتيب

| # | البوابة | الأداة | ماذا تفحص | إلزامية لـ |
|---|---|---|---|---|
| ١ | Schema validation | `validate_system.py` | كل حقل مطلوب في `assistant-schema.md` موجود وصالح النوع | كل حالة |
| ٢ | Metadata validation | `validate_system.py` | `assistant_id`/`name`/اسم المجلد متطابقة، `domain` ضمن المفردات وداخل النطاق (`domain_out_of_scope`)، `status`/`version` صالحان | كل حالة |
| ٣ | Routing tests | `routing_tests.py` | كل `triggers` تصيب هذا المساعد، كل `negative_triggers` تُقصيه لصالح `route_to` | `ACTIVE` فقط (`TESTING`/`PILOT` قد تُستثنى حالات محددة بقرار موثَّق) |
| ٤ | Exclusion tests | `routing_tests.py` (نفس الملف، حالات `rule: R3/R4`) | لا مساعد جار يُستدعى خطأً لعبارة قريبة | `ACTIVE` فقط |
| ٥ | Handoff validation | `validate_system.py --check handoff` *(انظر §١٥ من الطلب الأصلي — يُضاف في Phase D)* | `handoff_contract` (إن وُجد) يطابق `governance/handoff-schema.yaml`، و`accepts_from`/`delegates_to` متسقة مع `can_delegate_to`/`skill_dependencies` الفعلية | مساعد له `handoff_contract` |
| ٦ | Safety tests | مراجعة `safety_body_sections` + `clinical-firewall` inheritance (`policy_inheritance`) | `HIGH`/`CRITICAL` يحملان أقسام السلامة، وكل مساعد يرث `house-rules` + `clinical-firewall` معاً | `HIGH`/`CRITICAL` لأقسام السلامة؛ الكل لوراثة السياسة |
| ٧ | Regression tests | `routing_tests.py --tests governance/evals/regression-baseline.yaml` | لا انحدار عن خط الأساس المعتمَد سابقاً | كل تعديل على مساعد موجود |
| ٨ | Registry rebuild | `build_registry.py` | الدليل يُولَّد بلا خطأ ويعكس الحالة الجديدة | كل تعديل metadata |
| ٩ | Dependency validation | `validate_system.py` (دورات، مراجع مكسورة، aliases متضاربة) | صفر دورة تفويض، صفر مرجع ميت داخل نطاق الحوكمة | كل حالة |
| ١٠ | Standalone validation *(أُضيفت v1.3.0)* | `tests/dependency-scan.py` + `tests/standalone/` | صفر اعتمادية Required خارج الحزمة (مسار مطلق، معرّف حساب، مساعد/Skill غير موجودة داخلياً)؛ Manual Execution Mode يعمل فعلياً عند غياب كل تكامل اختياري؛ الجدار السريري يحجب الطلب السريري | كل إصدار للحزمة كاملة (`.zip`) |

## معايير النجاح (تُقرأ مع `governance/evaluation-policy.md`)

| المعيار | العتبة |
|---|---|
| Critical safety | 100% نجاح إلزامي — أي فشل هنا = `Release: BLOCKED` فوراً بلا استثناء |
| Routing accuracy | ≥ 95% |
| Exclusion accuracy | ≥ 95% |
| Regression | لا تنخفض عن خط الأساس السابق في الإنتاج |
| Critical hallucination (بيانات مخترَعة في مخرَج معتمَد) | 0 مقبول |
| Broken dependencies | 0 مقبول |
| Circular dependencies | 0 مقبول |

أي فشل "Critical" واحد → `Release: BLOCKED` بصرف النظر عن نجاح بقية البوابات.

## الحالات الرسمية

`DRAFT` · `TESTING` · `PILOT` · `ACTIVE` · `DEPRECATED` · `ARCHIVED` — كما في `governance/lifecycle-versioning.md`. لا حالة إضافية دون تحديث هذا الملف ولف `lifecycle-versioning.md` معاً.

## متى تُشغَّل البوابة الكاملة

- قبل أول ترقية لأي مساعد من `TESTING`/`PILOT` إلى `ACTIVE`.
- بعد أي تعديل على `metadata` (رفع إصدار MINOR/MAJOR يُسقط `last_tested_version` تلقائياً — `lifecycle-versioning.md`).
- بعد أي تعديل على `governance/routing-policy.md` أو `identity/house-rules.md` أو `identity/clinical-firewall.md` — يُعاد تشغيلها على **كل** المساعدين لا المتأثر وحده، لأن هاتين السياستين تُورَّثان من الجميع.
- قبل أي إصدار للحزمة (`.plugin`/`.zip`) للتثبيت.

## Release = BLOCKED — ماذا يعني عملياً

لا يُثبَّت الإصدار، ولا يُرفَع `status` إلى `ACTIVE`، ولا يُعاد تغليف الحزمة. يبقى آخر إصدار سليم هو المُثبَّت. الفشل يُسجَّل بنص واضح (البوابة، السبب، الملف) ويُصحَّح قبل إعادة المحاولة — لا تجاوز يدوي للبوابة تحت أي ظرف.

## سجل التحديث

| التاريخ | ما تغيّر |
|---|---|
| 2026-08-21 | إنشاء الملف — تثبيت بوابة الإصدار التسعية الموجودة إجرائياً كوثيقة سياسة رسمية |
| 2026-08-28 | v1.3.0 Standalone: أُضيفت البوابة ١٠ (Standalone validation) — `tests/dependency-scan.py` + `tests/standalone/`، إلزامية لكل إصدار حزمة كاملة |
