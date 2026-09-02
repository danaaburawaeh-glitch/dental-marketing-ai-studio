---
document: knowledge-schema
type: GOVERNANCE
version: 1.0.0
status: ACTIVE
applies_to: ALL_KNOWLEDGE_FILES
---

# مخطط ملفات المعرفة — Knowledge Schema v1.0.0

**لا يعيد هذا الملف بناء قاعدة المعرفة الحالية.** `knowledge/assistants-registry.md` وفهرس الـ Project (`knowledge/INDEX.md`) يبقيان كما هما حتى إشعار آخر. هذا المخطط يؤسس المعمارية التي تجعل فهرس المعرفة **مولَّداً** لاحقاً بدل مُحرَّر يدوياً — بنفس منطق `assistant-schema.md` لدليل المساعدين.

## أين يعيش المخطط

في frontmatter كل ملف معرفة، بنفس نمط `SKILL.md`:

```yaml
---
knowledge_id: shared-services-pricing
title: أسعار الخدمات
version: "1.0.0"
status: DRAFT
owner: clinic-owner
domain: marketing
source: ⟨من أين — الطبيب/ة شخصياً، ملف مرسَل، موقع العيادة⟩
source_type: ⟨primary | secondary | draft⟩
created: "2026-08-21"
last_verified: null
next_review: null
used_by: []
sensitivity: ⟨LOW | INTERNAL | PATIENT_SENSITIVE⟩
patient_data_allowed: false
supersedes: null
tags: []
---
```

## الحقول

| الحقل | إلزامي | القاعدة |
|---|---|---|
| `knowledge_id` | ✔ | فريد، kebab-case، يبدأ عادة ببادئة المجلد (`shared-`, `clinical-`, …) |
| `title` | ✔ | عنوان معروض — عربي مسموح |
| `version` | ✔ | SemVer — نفس منطق `lifecycle-versioning.md` |
| `status` | ✔ | أحد `DRAFT · REVIEWED · ACTIVE · SUPERSEDED · ARCHIVED` — انظر أدناه |
| `owner` | ✔ | المسؤول البشري عن صحة المحتوى |
| `domain` | ✔ | من مفردات `assistant-schema.md § domain`، مقيَّدة بـ `scope-boundary.md` لهذه الإضافة |
| `source` | ✔ | من أين جاء المحتوى فعلياً — لا "غير معروف" |
| `source_type` | ✔ | `primary` (الطبيب/ة نفسها) · `secondary` (ملف/مصدر خارجي موثوق) · `draft` (لم يُعتمَد بعد) |
| `created` | ✔ | ISO 8601 |
| `last_verified` | — | تاريخ آخر تأكيد أن المحتوى لا يزال صحيحاً |
| `next_review` | — | متى يجب إعادة الفحص (أسعار وسياسات تتغيّر) |
| `used_by` | — | قائمة `assistant_id` التي تعتمد هذا الملف عبر `knowledge_dependencies` |
| `sensitivity` | ✔ | `LOW` (عام) · `INTERNAL` (داخلي غير حساس) · `PATIENT_SENSITIVE` (يلمس بيانات/خصوصية مرضى) |
| `patient_data_allowed` | ✔ | `false` دائماً ما لم يُبرَّر خلاف ذلك صراحة ويُراجَع — house-rules.md §٤ يبقى الحاكم |
| `supersedes` | — | `knowledge_id` قديم استُبدل بهذا الملف — لا حذف، `SUPERSEDED` بدلاً |
| `tags` | — | كلمات بحث حرة |

## الحالات — Knowledge Status

| الحالة | المعنى | يُستخدَم من المساعدين؟ |
|---|---|---|
| `DRAFT` | مسودة، معلومات غير مكتملة أو غير مؤكَّدة | ✘ |
| `REVIEWED` | راجعها owner لكن لم تُعتمَد نهائياً | ✘ — إلا بطلب صريح |
| `ACTIVE` | معتمدة، جاهزة للاستخدام | ✔ |
| `SUPERSEDED` | استُبدلت بنسخة أحدث (`supersedes` في الملف الجديد يشير إليها) | ✘ — تبقى للأرشيف والمرجعية |
| `ARCHIVED` | غير صالحة إطلاقاً | ✘ |

**قاعدة صارمة — لا اختراع:** ملف معرفة لا يدخل `ACTIVE` بدون `owner` + `source` + `last_verified` + `used_by` (ولو فارغة صراحة، لا غائبة). ملف بحقول ناقصة يبقى `DRAFT` مهما كان محتواه مكتملاً ظاهرياً — هذا يمنع تحديداً حالة "معلومة تبدو جاهزة لكن لا أحد أكّد صحتها".

## البنية الفعلية على القرص

```
knowledge/
  shared/       معرفة يشترك فيها أكثر من مساعد
  clinical/     خارج نطاق هذه الإضافة فعلياً (scope-boundary.md) — بنية جاهزة فقط، لا محتوى يُبنى هنا
  marketing/    معرفة تسويقية خاصة بمجال أو حملة
  management/   إدارة العيادة الداخلية
  research/     مراجع علمية عامة (ليست بروتوكولات سريرية)
```

**لا نقل عشوائي.** الملفات الموجودة فعلياً (`knowledge/assistants-registry.md`) تبقى في مكانها الحالي؛ أي نقل مستقبلي يمر عبر خطة ترحيل موثَّقة (`governance/templates/architecture-change-proposal.md`) لأنه قد يكسر `knowledge_dependencies` في `skills/*/SKILL.md`.

## ملفان مؤجَّلان عمداً — خارج نطاق هذه الإضافة

من قائمة الأولوية التالية في طلب Hardening: `clinical-safety-policy` و `evidence-policy`. **لم يُنشآ هنا.** كلاهما محتوى سريري/بحثي صراحة، وهذه الإضافة (`assistant-studio`) مقيَّدة بنياً بـ `governance/scope-boundary.md` إلى إدارة عيادة وتسويق فقط — القرار الذي وافقت عليه الطبيب/ة صراحة في مرحلة سابقة من هذا المشروع. مكانهما الطبيعي هو إضافة Clinical Core منفصلة مستقبلية (خارج نطاق هذه الحزمة)، لا `knowledge/clinical/` أو `knowledge/research/` هنا رغم وجود المجلدين كبنية جاهزة. إنشاؤهما داخل هذه الإضافة يكسر الفصل الذي بُني عليه القسم كله.

## المولِّد

`scripts/build_knowledge_index.py` يقرأ frontmatter كل ملف تحت `knowledge/` (عدا الملفات المولَّدة نفسها) وينتج `knowledge/generated-index.md` — **ملف جديد منفصل**، لا يستبدل `knowledge/INDEX.md` الحالي في الـ Project. الانتقال إلى فهرس مولَّد بالكامل قرار لاحق بعد أن تحمل غالبية الملفات هذا المخطط فعلياً.

## سجل التحديث

| التاريخ | ما تغيّر |
|---|---|
| 2026-08-21 | إنشاء الملف — تأسيس معمارية حوكمة المعرفة دون إعادة بناء المحتوى القائم |
