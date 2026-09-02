---
document: assistant-schema
type: GOVERNANCE
version: 1.2.0
status: ACTIVE
applies_to: ALL_ASSISTANTS
---

# مخطط المساعد الموحّد — Assistant Schema v1.2.0

مخطط إلزامي لكل مساعد داخل استوديو المساعدين. المساعد الذي لا يطابقه لا يُعتمد `ACTIVE` ولا يدخل الـ routing التلقائي.

## أين يعيش المخطط

**داخل `SKILL.md` نفسه، في كتلة `metadata` في الـ frontmatter.** لا في ملف جانبي ولا في الدليل.

هذا هو **مصدر الحقيقة الوحيد**. الدليل (`assistants-registry`) وفهرس المعرفة يُولَّدان من هنا ولا يُحرَّران يدوياً.

```yaml
---
name: instagram-data-analyst          # يطابق assistant_id حرفياً
description: >
  ...                                  # للـ semantic routing — لا شعار تسويقي
metadata:
  assistant_id: instagram-data-analyst
  ...
---
```

`name` في الـ frontmatter و `assistant_id` في الـ metadata واسم المجلد — **ثلاثتها متطابقة**. الفاحص يرفض أي اختلاف.

## الحقول

| الحقل | إلزامي | النوع | القاعدة |
|---|---|---|---|
| `assistant_id` | ✔ | string | Canonical · immutable · kebab-case |
| `display_name` | ✔ | string | الاسم المعروض — عربي مسموح |
| `domain` | ✔ | enum | من المفردات المضبوطة أدناه |
| `role` | ✔ | string | الدور بكلمتين أو ثلاث |
| `purpose` | ✔ | string | جملة واحدة: ما الذي يُنجزه |
| `triggers` | ✔ | list | عبارات تشغيل حرفية، عربية وإنجليزية |
| `negative_triggers` | ✔ | list of maps | `{match, route_to}` — إلزامي، ولا يُقبل فارغاً |
| `required_inputs` | ✔ | list | ما لا يعمل بدونه |
| `optional_inputs` | — | list | |
| `outputs` | ✔ | list | مكوّنات النتيجة |
| `knowledge_dependencies` | — | list | مسارات داخل `knowledge/` |
| `policy_dependencies` | ✔ | list | يجب أن تحوي `house-rules` و `clinical-firewall` معاً |
| `skill_dependencies` | — | list | مساعدون تُستهلك مخرجاتهم كمدخل |
| `tool_dependencies` | — | list | الموصّلات المستخدمة |
| `can_delegate_to` | — | list | **تحويل فعلي أثناء التنفيذ فقط** |
| `cannot_delegate_to` | — | list | منع صريح عند خطر دورة أو تعارض |
| `handoff_contract` | — | map | مشتق حصراً من `can_delegate_to`/`skill_dependencies`/`required_inputs`/`outputs` لنفس المساعد — انظر أدناه. غيابه = لا يشارك هذا المساعد في تسليم منظَّم (يعمل مستقلاً) |
| `routing_priority` | ✔ | int 0–100 | ١٠٠ الأعلى |
| `safety_level` | ✔ | enum | LOW · MODERATE · HIGH · CRITICAL |
| `status` | ✔ | enum | دورة الحياة — انظر `lifecycle-versioning.md` |
| `version` | ✔ | semver | MAJOR.MINOR.PATCH |
| `last_tested_version` | ✔ لكل ACTIVE | semver | إن خالف `version` → لا يجوز ACTIVE |
| `owner` | ✔ | string | المسؤول البشري |
| `created_at` · `last_updated` | ✔ | date | ISO 8601 |
| `last_tested` | — | date | |
| `evaluation_suite` | — | string | مسار ملف اختبارات الـ routing |
| `legacy_aliases` | — | list | معرّفات قديمة تُقبل ولا تُستخدم في ملفات جديدة |
| `deprecated_by` | — | string | المعرّف البديل عند `DEPRECATED` |
| `notes` | — | string | |

## `can_delegate_to` مقابل `skill_dependencies` — تمييز حاسم

| | المعنى | يدخل فحص الدورات؟ |
|---|---|---|
| `can_delegate_to` | **يستدعي** مساعداً آخر أثناء تنفيذ مهمته | ✔ نعم |
| `skill_dependencies` | **يستهلك مخرجات** مساعد آخر كمدخل جاهز | ✘ لا |
| `negative_triggers[].route_to` | **إحالة توجيه** قبل بدء العمل | ✘ لا |

الخلط بينها يُنتج دورات وهمية. مثال: «اجتماع النمو» يستدعي المتخصصين ← `can_delegate_to`. «مهندس المحتوى» يقرأ نتائج محلل الجمهور ← `skill_dependencies`. «مشخّص القمع» يقول «للمراجعة الدورية استخدم المدير» ← `negative_triggers`.

## `handoff_contract` — عقد التسليم لهذا المساعد بعينه

اختياري. يُضاف فقط إن كان لهذا المساعد `can_delegate_to` أو `skill_dependencies` غير فارغ — لا يُضاف تجميلاً لمساعد يعمل مستقلاً. القالب الإلزامي في `governance/handoff-schema.yaml`؛ هذا الحقل يُلخِّص جزء المساعد منه:

```yaml
handoff_contract:
  accepts_from: []      # = skill_dependencies لنفس المساعد — من يستهلك مخرجه
  delegates_to: []       # = can_delegate_to لنفس المساعد — من يستدعيه فعلياً أثناء التنفيذ
  required_inputs: []     # = required_inputs لنفس المساعد — لا قائمة جديدة
  guaranteed_outputs: []   # = outputs لنفس المساعد — لا قائمة جديدة
```

**قاعدة صارمة:** لا يُشتق `handoff_contract` إلا من الحقول الأربعة المذكورة لنفس المساعد نفسه. **ممنوع** إضافة علاقة إلى `accepts_from`/`delegates_to` غير مذكورة فعلياً في `can_delegate_to`/`skill_dependencies` لذلك المساعد — هذا يخترع علاقة تنسيق غير موجودة ويُفسد فحص `orchestration_tests.py`.

## المفردات المضبوطة — `domain`

`system` · `instagram` · `marketing` · `content` · `patient` · `clinical` · `research` · `management` · `finance` · `sales` · `legal` · `operations`

لا يُنشأ domain جديد إلا بتحديث هذا الملف والفاحص معاً.

> **قيد إضافي خاص بهذه الإضافة:** `assistant-studio` مخصصة لإدارة العيادة والتسويق حصراً. `clinical` · `patient` · `research` **ممنوعة داخل هذه الإضافة تحديداً** ولو كانت موجودة في المفردات العامة أعلاه — التفصيل والسبب في `governance/scope-boundary.md`. الفاحص يفشل البناء (`domain_out_of_scope`) عند أي مساعد بأحد هذه القيم الثلاث داخل `skills/`.

## قواعد المعرّف — `assistant_id`

```
<domain>-<function>-<role>     أو     <domain>-<function>
```

- حروف إنجليزية صغيرة و kebab-case فقط · لا مسافات · لا `_`
- يبدأ بحرف — **لا أرقام تسلسلية في المعرّف**
- لا لاحقات مبتورة (`-inst`، `-insta`)
- لا اسم شخص إلا لسبب معماري موثَّق
- يصف **الوظيفة** لا موقع الملف ولا ترتيبه
- **ثابت عبر الإصدارات.** تغيير المعرّف = ترحيل موثَّق في `assistant-id-migration-map.md`، لا تعديل عابر

## `description` — للتوجيه لا للتسويق

يجب أن تجيب: **متى يُستدعى هذا المساعد تحديداً، ومتى لا يُستدعى.** ثلاث جمل: ماذا يفعل · عبارات التشغيل مقتبسة بالعربية والإنجليزية · ما يخص غيره مع تسمية البديل.

الوصف الذي لا يحتوي عبارات مقتبسة يُرفض آلياً.

## `safety_level` — كيف يُحدَّد

| المستوى | المعيار |
|---|---|
| `CRITICAL` | بوابة موافقة مريض أو نشر أو امتثال — الخطأ فيه غير قابل للتراجع |
| `HIGH` | يُنتج محتوى يصل للمرضى أو نصاً يُنشر، أو يمس بيانات مرضى |
| `MODERATE` | يحلل بيانات الحساب أو ينتج توصيات داخلية |
| `LOW` | إداري بحت، بلا مخرَج عام وبلا بيانات حساسة |

`HIGH` و `CRITICAL` يلزمهما وجود أقسام السلامة والخصوصية في الجسم — يفحصها الفاحص.

## سياسة إلزامية

`policy_dependencies` يجب أن تحوي `house-rules` **و** `clinical-firewall` معاً في **كل** مساعد بلا استثناء — كلاهما GLOBAL_POLICY بنفس المرتبة (`priority: HIGHEST`، `override_allowed: false`). غياب أيّهما = فشل بناء. انظر `routing-policy.md § التسلسل` و `governance/scope-boundary.md`.

## قالب كامل

```yaml
metadata:
  assistant_id: instagram-data-analyst
  display_name: محلل بيانات انستغرام
  domain: instagram
  role: data-analyst
  purpose: قراءة أرقام الحساب وحساب المعدلات ومقارنتها بالفترة السابقة، بلا تفسير محتوى
  triggers:
    - "وش تقول الأرقام"
    - "كم معدل التفاعل"
    - "calculate my engagement rate"
  negative_triggers:
    - match: "ليش هذا المنشور نجح"
      route_to: instagram-content-performance-analyst
    - match: "ليش الحساب ما ينمو"
      route_to: instagram-funnel-diagnostician
  required_inputs: ["فترة زمنية محددة", "مصدر بيانات متاح"]
  optional_inputs: ["فترة مقارنة سابقة"]
  outputs: ["جدول مؤشرات", "ثلاث ملاحظات", "سؤال قابل للاختبار"]
  knowledge_dependencies: []
  policy_dependencies: ["house-rules", "clinical-firewall"]
  skill_dependencies: []
  tool_dependencies: ["windsor", "meta-ads", "chatplace"]
  can_delegate_to: []
  cannot_delegate_to: []
  routing_priority: 65
  safety_level: MODERATE
  status: ACTIVE
  version: "1.0.0"
  last_tested_version: "1.0.0"
  owner: clinic-owner
  created_at: "2026-08-21"
  last_updated: "2026-08-21"
  last_tested: "2026-08-21"
  evaluation_suite: governance/routing-tests.yaml
  legacy_aliases: ["2-instagram-data-analyst-inst"]
  deprecated_by: null
  notes: ""
```
