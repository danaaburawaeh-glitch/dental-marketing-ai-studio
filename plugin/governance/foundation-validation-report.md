---
document: foundation-validation-report
type: GOVERNANCE
version: 1.0.0
phase: foundation-hardening
date: "2026-08-21"
verdict: PASS WITH WARNINGS
---

# تقرير التحقق من الأساس — Foundation Validation Report

**المرحلة:** Foundation Hardening · **التاريخ:** 2026-08-21
**النتيجة:** `PASS WITH WARNINGS` — كل فحوص الحوكمة نجحت؛ التنبيهات مقصودة وموثَّقة، وبقي بندان يحتاجان قرار الطبيب/ة.

---

## ١. الجرد

### قبل

| | العدد |
|---|---|
| عناصر مفحوصة إجمالاً | 74 |
| مهارات في حساب الطبيب/ة | 56 |
| منها `custom` (ملك الطبيب/ة) | 49 |
| منها `anthropic` / `anthropic-example` | 7 |
| نسخ عمل داخل المشروع | 16 |
| عناصر موسومة بمشكلة | 69 |
| معرّفات مكررة | 11 (نسخة حساب + نسخة عمل لكل مهارة نمو) |

**الأوسمة المرصودة:** بلا عبارات تشغيل مقتبسة 43 · بلا `metadata` 28 · بادئة رقم تسلسلي 22 · لاحقة مبتورة `inst`/`insta` 22 · لا يطابق kebab-case 22 · اسم غير وصفي 5 · اسم شخص في المعرّف 3 · وصف أقصر من أن يُطابَق 3 · مهارة اختبار 2.

### بعد — النطاق المحوكَم

| | العدد |
|---|---|
| مساعدون محوكَمون | 16 |
| بـ `metadata` كاملة | 16 (100٪) |
| موسومون بمشكلة | **0** |
| معرّفات مكررة | **0** |
| `ACTIVE` | 15 |
| `TESTING` | 1 |
| سياسات عامة | 1 (`house-rules`) |
| وثائق حوكمة | 6 |

**اكتشاف حاسم من مرحلة DISCOVER:** إضافة `assistant-studio` **لم تكن مثبتة**، و `case-post-reviewer` **لم يُحفظ** في الحساب. هذا خفّض خطر ترحيل خمسة معرّفات من MEDIUM إلى LOW — ولولا الجرد قبل التعديل لعوملت على أنها مثبتة.

---

## ٢. المعرّفات المُغيَّرة

| المعرّف القديم | الكانوني الجديد | الإجراء | الخطر | السبب |
|---|---|---|---|---|
| `new-assistant` | `system-assistant-builder` | RENAME | LOW | بلا مجال، و«new» صفة حالة لا وظيفة |
| `assistant-directory` | `system-assistant-directory` | RENAME | LOW | توحيد بادئة المجال |
| `assistant-knowledge` | `system-knowledge-manager` | RENAME | LOW | يصف موضوعاً لا وظيفة |
| `assistant-tuning` | `system-assistant-tuner` | RENAME | LOW | مصدر لا دور |
| `case-post-reviewer` | `content-case-post-reviewer` | RENAME | LOW | بلا بادئة مجال |
| `1-chief-growth-officer-inst` | `instagram-funnel-diagnostician` | RENAME | MEDIUM | رقم + لاحقة مبتورة؛ والاسم كان يصف رتبة لا الوظيفة الفعلية |
| `2-instagram-data-analyst-inst` | `instagram-data-analyst` | RENAME | MEDIUM | رقم + لاحقة مبتورة |
| `3-audience-intelligence-analyst-insta` | `instagram-audience-analyst` | RENAME | MEDIUM | رقم + لاحقة + «intelligence» بلا معنى مضاف |
| `4-content-performance-analyst-inst` | `instagram-content-performance-analyst` | RENAME | MEDIUM | رقم + لاحقة مبتورة |
| `5-reel-strategy-specialist-inst` | `instagram-reel-strategist` | RENAME | MEDIUM | رقم + لاحقة + تكرار `strategy-specialist` |
| `6-personal-brand-strategist-inst` | `instagram-personal-brand-strategist` | RENAME | MEDIUM | رقم + لاحقة مبتورة |
| `7-competitor-intelligence-analyst-insta` | `instagram-competitor-analyst` | RENAME | MEDIUM | رقم + لاحقة + «intelligence» |
| `8-growth-experimentation-manager-inst` | `instagram-experimentation-manager` | RENAME | MEDIUM | رقم + لاحقة مبتورة |
| `9-content-architect-inst` | `instagram-content-architect` | RENAME | MEDIUM | رقم + لاحقة مبتورة |
| `10-conversion-analyst-inst` | `instagram-conversion-analyst` | RENAME | MEDIUM | رقم + لاحقة مبتورة |
| `11-weekly-growth-meeting-inst` | `instagram-weekly-growth-review` | RENAME | MEDIUM | رقم + لاحقة؛ و«review» أدق من «meeting» لوصف المخرَج |

**66 مرجعاً متقاطعاً** حُدِّث آلياً. **صفر** مرجع لمعرّف قديم بقي في أي ملف (خارج `legacy_aliases`) — تحقُّق آلي بحدود كلمة صارمة.

كل معرّف قديم محفوظ في `legacy_aliases` فلا تنكسر الطلبات القديمة، ولا يُستخدم في أي ملف جديد.

---

## ٣. التكرارات

| العنصر | المقابل | التشابه | القرار | السبب |
|---|---|---|---|---|
| `short-form-video-plan` | `drdana-short-form-video-plan` | **PROBABLE_DUPLICATE** (1.000 مُقاس) | DEPRECATE | وصفان متطابقان وتاريخ تحديث واحد؛ لا قدرة فريدة في النسخة العامة |
| `personal-brand-strategy` | `instagram-personal-brand-strategist` | HIGH | **MANUAL_REVIEW** | تشابه في الغرض لا في النطاق — النسخة العامة تغطي منصات غير انستغرام. لا دمج بناءً على التشابه وحده |
| `emai-test` | — | — | DELETE_CANDIDATE | مهارة اختبار بوصف من كلمتين، بلا مراجع |
| `meta-ads-test` | — | — | DELETE_CANDIDATE | مهارة اختبار بوصف من كلمتين، بلا مراجع |
| `lower` | — | — | ARCHIVE | مجال `legal` خارج نطاق العمل — قدرة حقيقية لا اختبار، فلا تُحذف |

**لم يُحذف شيء.** حتى `DELETE_CANDIDATE` بقي — الحذف قرار الطبيب/ة.

**تحقق من صحة كاشف التداخل:** شُغِّل على الزوج المكرر المعروف فأعطى `1.000 → PROBABLE_DUPLICATE`، وعلى زوج متمايز عمداً فأعطى `0.018 → LOW`. أعلى تشابه داخل النطاق المحوكَم بعد الترحيل: **0.091** (`system-assistant-builder ~ system-knowledge-manager`) — أي `LOW`. صفر تداخل يستوجب إجراءً.

---

## ٤. المراجع المكسورة

**لم يُعثر على أي مرجع مكسور داخل النطاق المحوكَم.** كل `route_to` و `can_delegate_to` و `skill_dependencies` يشير إما إلى معرّف كانوني موجود، أو إلى مهارة حساب خارج نطاق الترحيل.

**10 تنبيهات `external_reference`** — مقصودة وموثَّقة، لا أخطاء:

| المصدر | الهدف الخارجي |
|---|---|
| `instagram-funnel-diagnostician` · `instagram-weekly-growth-review` | `dana-instagram-growth-director` |
| `instagram-reel-strategist` · `instagram-content-architect` | `drdana-short-form-video-plan` |
| `instagram-content-architect` | `social-media-calendar` |
| `instagram-conversion-analyst` | `whatsapp-closing-specialist` |
| `instagram-personal-brand-strategist` | `marketing-strategy-director` · `linkedin-strategy` |
| `content-case-post-reviewer` | `smile-doc-standardizer` |

هذه إحالات إلى مهارات حساب مؤجَّلة إلى المرحلة الثانية. تتحول إلى معرّفات كانونية عند ترحيلها.

---

## ٥. تعارضات التوجيه — قبل وبعد

| التعارض | قبل | بعد |
|---|---|---|
| «راجعي أرقام الحساب» بين محلل البيانات ومالكة الاستراتيجية | غير محسوم | محسوم: العبارة القصيرة ← `instagram-data-analyst`، والعبارة الكاملة مع «خطة ٩٠ يوم» ← `dana-instagram-growth-director` |
| قائد الفريق مقابل مديرة النمو مقابل الاجتماع الأسبوعي | ثلاثة يتنافسون | ثلاثة أدوار مفصولة بـ `negative_triggers` + `cannot_delegate_to` |
| «خطة فيديوهات» بين أخصائي الريلز ومخطط الفيديو | غير محسوم | إقصاء صريح ← `drdana-short-form-video-plan` |
| «كيف أرد على هذي الرسالة» بين محلل التحويل ومساعد الردود | غير محسوم | إقصاء صريح ← `whatsapp-closing-specialist` |

**خلل مكتشَف أثناء الاختبار وأُصلح:** كانت العبارة القصيرة الواقعة داخل عبارة سالبة طويلة تُقصي المساعد بمطابقة كاملة (1.0). صُحِّح بترجيح الطول في `phrase_score`، وأُضيفت حالة اختبار دائمة تحرس السلوك.

---

## ٦. مطابقة المخطط

| | العدد |
|---|---|
| إجمالي المساعدين | 16 |
| مطابق للمخطط بالكامل | **16** |
| غير مطابق | **0** |

كل مساعد يحمل ٢٩ حقلاً وفق `assistant-schema.md`، منها ١٦ إلزامياً. `assistant_id` = `name` = اسم المجلد في كل الحالات.

---

## ٧. السياسة العامة

```
house-rules inheritance:  PASS   — 16/16 مساعد يحمل house-rules في policy_dependencies
override protection:      PASS   — type: GLOBAL_POLICY · scope: ALL_ASSISTANTS
                                   priority: HIGHEST · override_allowed: false
```

التسلسل مثبَّت في `routing-policy.md`:
`GLOBAL POLICY > DOMAIN POLICY > ASSISTANT INSTRUCTIONS > KNOWLEDGE > USER REQUEST`

**لم تُعدَّل أي قاعدة موضوعية في `house-rules`** — أُضيفت ترويسة تصنيف فقط، كما تقتضي الحدود.

---

## ٨. نتائج الفحص الآلي

`scripts/validate_system.py` — **26 فحصاً، كلها PASS**:

| الفحص | النتيجة | الفحص | النتيجة |
|---|---|---|---|
| `duplicate_assistant_id` | PASS | `policy_inheritance` | PASS |
| `id_format` | PASS | `policy_reference` | PASS |
| `id_consistency` | PASS | `knowledge_reference` | PASS |
| `schema_required_fields` | PASS | `external_reference` | PASS |
| `lifecycle_status` | PASS | `circular_delegation` | PASS |
| `semver_format` | PASS | `delegation_contradiction` | PASS |
| `active_requires_tested` | PASS | `legacy_as_canonical` | PASS |
| `active_version_tested` | PASS | `legacy_alias_collision` | PASS |
| `routing_priority_range` | PASS | `active_overlapping_roles` | PASS |
| `safety_level_vocabulary` | PASS | `domain_vocabulary` | PASS |
| `safety_body_sections` | PASS | `negative_triggers_required` | PASS |
| `global_policy_present` | PASS | `description_routable` | PASS |
| `global_policy_override` | PASS | `frontmatter` | PASS |

`scripts/routing_tests.py` — **29/29 حالة ناجحة**: ١٠ حالات انحدار من الدليل قبل الترحيل · ٨ إصابة · ٤ إقصاء · ١ حالة دورة حياة · ١ لا مطابقة · ٥ حالات غموض اكتُشفت أثناء الترحيل.

**اختبار البوابة نفسها:** قبل الختم، فشل الفاحص بـ ١٥ خطأ `active_requires_tested` — أي أن قفل «لا اعتماد بلا اختبار» يعمل فعلاً ولم يكن مجرد نص. بعد الختم: صفر.

---

## ٩. يحتاج مراجعة بشرية

| البند | لماذا لم يُحسم آلياً |
|---|---|
| `dana-instagram-growth-director` | اسم شخص في المعرّف، لكنه مذكور نصياً داخل وصفَي `drdana-short-form-video-plan` و `short-form-video-plan` — وكلاهما خارج نطاق الترحيل. إعادة التسمية تكسر مرجعين. **RISK: HIGH → لم يُلمس.** |
| `drdana-short-form-video-plan` | اسم شخص + مرجع متبادل مع نسخته المكررة. يُحسم بعد قرار المكرر. |
| `personal-brand-strategy` | تشابه HIGH مع `instagram-personal-brand-strategist` لكن النطاق مختلف. **لا يُدمج بناءً على التشابه الدلالي وحده** — القرار يحتاج جواب الطبيب/ة: هل تحتاج استراتيجية علامة خارج انستغرام؟ |
| `chief-advertising-officer-cao` | لاحقة اختصار مبهم، ولم يخضع لترقية وصف بعد. لا يُرحَّل قبل ترقيته. |
| حذف `emai-test` · `meta-ads-test` · `lower` · `short-form-video-plan` | الحذف قرار بشري. الأدوات لا تحذف. |
| `created_at` للمهارات الإحدى عشرة | القيمة `unknown` — التاريخ الحقيقي يسبق الترحيل ولا مصدر موثوق له. **لم يُختلق.** |

---

## ١٠. تغييرات لم تُنفَّذ عمداً

| ما لم يُنفَّذ | السبب |
|---|---|
| ترحيل ٤٩ مهارة `custom` الأخرى | خارج نطاق مرحلة الأساس؛ ترحيلها يستلزم حذف وإعادة حفظ ٤٩ مهارة بلا مكسب معماري في هذه المرحلة |
| ترحيل ٧ مهارات Anthropic | ليست ملكاً للمشروع ولا يمكن تغيير معرّفاتها |
| أي حذف | ممنوع في هذه المرحلة بنص التكليف |
| تعديل قواعد `house-rules` الموضوعية | ممنوع — التصنيف الهيكلي فقط |
| بناء أي مساعد جديد | ممنوع في مرحلة الأساس |
| رفع `content-case-post-reviewer` إلى ACTIVE | مستواه `CRITICAL` ويلزمه تشغيلة حقيقية على منشور فعلي؛ لم تجرِ بعد |

---

## ١١. البند المفتوح الوحيد — يحجب `PASS` الكامل

**النسخ القديمة من مهارات النمو الإحدى عشرة ما زالت محفوظة في حساب الطبيب/ة** بمعرّفاتها القديمة (`1-chief-growth-officer-inst` … `11-weekly-growth-meeting-inst`).

بعد تثبيت الإضافة الجديدة، سيتعايش المعرّف القديم والكانوني معاً حتى تُحذف النسخ القديمة يدوياً — وهذا يخرق معيار **ZERO unresolved duplicate active IDs**.

الحذف من الحساب لا تملكه الأدوات. حتى تُنفَّذ الخطوة، النتيجة الصحيحة هي `PASS WITH WARNINGS` لا `PASS`.

---

## ١٢. معيار النجاح النهائي

| المعيار | الحالة |
|---|---|
| ONE canonical ID per assistant | ✅ 16/16 |
| ONE standard assistant schema | ✅ `assistant-schema.md` v1.0.0 · مطابقة 100٪ |
| ONE lifecycle system | ✅ ٦ حالات · `ACTIVE` وحدها قابلة للتوجيه |
| ONE semantic versioning system | ✅ مع قفل `last_tested_version` |
| ONE global policy hierarchy | ✅ `override_allowed: false` · وراثة 16/16 |
| ONE deterministic routing policy | ✅ ٩ قواعد مرتَّبة + ٢٩ اختباراً |
| ZERO known broken references | ✅ داخل النطاق المحوكَم |
| ZERO unresolved duplicate active IDs | ⚠️ **معلَّق على حذف ١١ نسخة قديمة من الحساب** |
| ZERO circular delegation paths | ✅ فحص آلي |
| ZERO ACTIVE assistants with untested current version | ✅ 15/15 مختوم |

**تسعة من عشرة محقَّقة. العاشر يتطلب خطوة يدوية واحدة من الطبيب/ة.**
