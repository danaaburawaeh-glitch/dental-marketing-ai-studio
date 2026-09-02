# خريطة ترحيل المعرّفات — ID Migration Map

> **ملف مولَّد** من `governance/migration-spec.yaml` — لا يُحرَّر يدوياً.
> حقل REFERENCED BY مقروء من الملفات المُرحَّلة الفعلية لا من الافتراض.

**إصدار المواصفة:** 1.0.0 · **التاريخ:** 2026-08-21 · **المرحلة:** foundation-hardening

## نطاقات الحوكمة

| النطاق | الوصف | الخطر | الإجراء |
|---|---|---|---|
| `T1_studio_uninstalled` | مهارات الاستوديو — نسخة عمل فقط، غير مثبتة في الحساب | LOW | MIGRATE |
| `T2_studio_installed` | فريق نمو انستغرام — محفوظ فعلياً في حساب الطبيب/ة | MEDIUM | MIGRATE |
| `T3_dana_authored_ungoverned` | مهارات كتبتها الطبيب/ة قبل الاستوديو، ولها مراجع خارج سيطرتنا | HIGH | REVIEW |
| `T4_vendor` | مهارات Anthropic والحزم الجاهزة | OUT_OF_SCOPE | KEEP |

**المنطق:** `T1_studio_uninstalled` — لا اعتمادية على حالة الحساب؛ الترحيل لا يكسر شيئاً قائماً · `T2_studio_installed` — المراجع كلها داخل ملفات نتحكم بها، لكن تغيير المعرّف يستلزم خطوة يدوية واحدة (حذف النسخ القديمة من الحساب) وإلا نشأ ازدواج نشط. · `T3_dana_authored_ungoverned` — مراجع نصية متبادلة مع مهارات لا تُرحَّل في هذه المرحلة

## القيود المنفَّذة

### `new-assistant`

```
OLD ID:        new-assistant
CANONICAL ID:  system-assistant-builder
ACTION:        RENAME
TIER:          T1_studio_uninstalled
RISK:          LOW

REFERENCED BY:
  - system-assistant-directory
  - system-assistant-tuner
  - system-knowledge-manager

DEPENDENCIES:
  - system-knowledge-manager

REASON:        المعرّف بلا مجال، و«new» صفة حالة لا وظيفة
```

### `assistant-directory`

```
OLD ID:        assistant-directory
CANONICAL ID:  system-assistant-directory
ACTION:        RENAME
TIER:          T1_studio_uninstalled
RISK:          LOW

REFERENCED BY:
  - system-assistant-builder
  - system-knowledge-manager

DEPENDENCIES:
  (لا اعتماديات)

REASON:        توحيد بادئة المجال
```

### `assistant-knowledge`

```
OLD ID:        assistant-knowledge
CANONICAL ID:  system-knowledge-manager
ACTION:        RENAME
TIER:          T1_studio_uninstalled
RISK:          LOW

REFERENCED BY:
  - system-assistant-builder
  - system-assistant-tuner

DEPENDENCIES:
  (لا اعتماديات)

REASON:        المعرّف يصف موضوعاً لا وظيفة
```

### `assistant-tuning`

```
OLD ID:        assistant-tuning
CANONICAL ID:  system-assistant-tuner
ACTION:        RENAME
TIER:          T1_studio_uninstalled
RISK:          LOW

REFERENCED BY:
  - system-assistant-builder
  - system-assistant-directory

DEPENDENCIES:
  - system-knowledge-manager

REASON:        توحيد بادئة المجال وتحويل الاسم من مصدر إلى دور
```

### `case-post-reviewer`

```
OLD ID:        case-post-reviewer
CANONICAL ID:  content-case-post-reviewer
ACTION:        RENAME
TIER:          T1_studio_uninstalled
RISK:          LOW

REFERENCED BY:
  - instagram-reel-strategist

DEPENDENCIES:
  (لا اعتماديات)

REASON:        بلا بادئة مجال؛ ولم يُحفظ في الحساب بعد فلا اعتمادية قائمة
```

### `1-chief-growth-officer-inst`

```
OLD ID:        1-chief-growth-officer-inst
CANONICAL ID:  instagram-funnel-diagnostician
ACTION:        RENAME
TIER:          T2_studio_installed
RISK:          MEDIUM

REFERENCED BY:
  - instagram-conversion-analyst
  - instagram-data-analyst
  - instagram-experimentation-manager
  - instagram-weekly-growth-review

DEPENDENCIES:
  - instagram-data-analyst

REASON:        بادئة رقم تسلسلي ولاحقة مبتورة؛ والاسم القديم يصف رتبة لا وظيفة — الوظيفة الفعلية بعد ترقية 0.2.0 هي تشخيص نقطة تسرّب القمع لا قيادة الفريق
```

### `2-instagram-data-analyst-inst`

```
OLD ID:        2-instagram-data-analyst-inst
CANONICAL ID:  instagram-data-analyst
ACTION:        RENAME
TIER:          T2_studio_installed
RISK:          MEDIUM

REFERENCED BY:
  - instagram-content-performance-analyst
  - instagram-experimentation-manager
  - instagram-funnel-diagnostician
  - instagram-weekly-growth-review

DEPENDENCIES:
  (لا اعتماديات)

REASON:        بادئة رقم تسلسلي ولاحقة مبتورة؛ الوظيفة مطابقة للمعرّف الجديد
```

### `3-audience-intelligence-analyst-insta`

```
OLD ID:        3-audience-intelligence-analyst-insta
CANONICAL ID:  instagram-audience-analyst
ACTION:        RENAME
TIER:          T2_studio_installed
RISK:          MEDIUM

REFERENCED BY:
  - instagram-content-architect
  - instagram-conversion-analyst
  - instagram-weekly-growth-review

DEPENDENCIES:
  - instagram-content-architect

REASON:        بادئة رقم تسلسلي ولاحقة مبتورة؛ و«intelligence» لا تضيف معنى
```

### `4-content-performance-analyst-inst`

```
OLD ID:        4-content-performance-analyst-inst
CANONICAL ID:  instagram-content-performance-analyst
ACTION:        RENAME
TIER:          T2_studio_installed
RISK:          MEDIUM

REFERENCED BY:
  - instagram-audience-analyst
  - instagram-content-architect
  - instagram-data-analyst
  - instagram-personal-brand-strategist
  - instagram-reel-strategist
  - instagram-weekly-growth-review

DEPENDENCIES:
  - instagram-data-analyst
  - instagram-experimentation-manager

REASON:        بادئة رقم تسلسلي ولاحقة مبتورة
```

### `5-reel-strategy-specialist-inst`

```
OLD ID:        5-reel-strategy-specialist-inst
CANONICAL ID:  instagram-reel-strategist
ACTION:        RENAME
TIER:          T2_studio_installed
RISK:          MEDIUM

REFERENCED BY:
  - content-case-post-reviewer
  - instagram-content-performance-analyst
  - instagram-weekly-growth-review

DEPENDENCIES:
  - content-case-post-reviewer

REASON:        بادئة رقم تسلسلي ولاحقة مبتورة؛ و«strategy-specialist» تكرار
```

### `6-personal-brand-strategist-inst`

```
OLD ID:        6-personal-brand-strategist-inst
CANONICAL ID:  instagram-personal-brand-strategist
ACTION:        RENAME
TIER:          T2_studio_installed
RISK:          MEDIUM

REFERENCED BY:
  - instagram-competitor-analyst
  - instagram-content-architect
  - instagram-weekly-growth-review

DEPENDENCIES:
  - instagram-competitor-analyst
  - instagram-content-performance-analyst

REASON:        بادئة رقم تسلسلي ولاحقة مبتورة
```

### `7-competitor-intelligence-analyst-insta`

```
OLD ID:        7-competitor-intelligence-analyst-insta
CANONICAL ID:  instagram-competitor-analyst
ACTION:        RENAME
TIER:          T2_studio_installed
RISK:          MEDIUM

REFERENCED BY:
  - instagram-content-architect
  - instagram-personal-brand-strategist
  - instagram-weekly-growth-review

DEPENDENCIES:
  - instagram-content-architect

REASON:        بادئة رقم تسلسلي ولاحقة مبتورة؛ و«intelligence» لا تضيف معنى
```

### `8-growth-experimentation-manager-inst`

```
OLD ID:        8-growth-experimentation-manager-inst
CANONICAL ID:  instagram-experimentation-manager
ACTION:        RENAME
TIER:          T2_studio_installed
RISK:          MEDIUM

REFERENCED BY:
  - instagram-content-performance-analyst
  - instagram-weekly-growth-review

DEPENDENCIES:
  - instagram-data-analyst

REASON:        بادئة رقم تسلسلي ولاحقة مبتورة
```

### `9-content-architect-inst`

```
OLD ID:        9-content-architect-inst
CANONICAL ID:  instagram-content-architect
ACTION:        RENAME
TIER:          T2_studio_installed
RISK:          MEDIUM

REFERENCED BY:
  - content-case-post-reviewer
  - instagram-audience-analyst
  - instagram-competitor-analyst
  - instagram-personal-brand-strategist

DEPENDENCIES:
  - instagram-audience-analyst
  - instagram-competitor-analyst
  - instagram-content-performance-analyst
  - instagram-personal-brand-strategist

REASON:        بادئة رقم تسلسلي ولاحقة مبتورة
```

### `10-conversion-analyst-inst`

```
OLD ID:        10-conversion-analyst-inst
CANONICAL ID:  instagram-conversion-analyst
ACTION:        RENAME
TIER:          T2_studio_installed
RISK:          MEDIUM

REFERENCED BY:
  - instagram-audience-analyst
  - instagram-weekly-growth-review

DEPENDENCIES:
  (لا اعتماديات)

REASON:        بادئة رقم تسلسلي ولاحقة مبتورة
```

### `11-weekly-growth-meeting-inst`

```
OLD ID:        11-weekly-growth-meeting-inst
CANONICAL ID:  instagram-weekly-growth-review
ACTION:        RENAME
TIER:          T2_studio_installed
RISK:          MEDIUM

REFERENCED BY:
  - instagram-funnel-diagnostician

DEPENDENCIES:
  - instagram-audience-analyst
  - instagram-competitor-analyst
  - instagram-content-performance-analyst
  - instagram-conversion-analyst
  - instagram-data-analyst
  - instagram-experimentation-manager
  - instagram-personal-brand-strategist
  - instagram-reel-strategist

REASON:        بادئة رقم تسلسلي ولاحقة مبتورة؛ و«review» أدق من «meeting» لوصف المخرَج
```

## قيود مؤجَّلة — ACTION: REVIEW / KEEP

لم تُنفَّذ في هذه المرحلة. سبب التأجيل مذكور، وشرط رفع التأجيل معه.

### `dana-instagram-growth-director`

```
ACTION:            REVIEW
TIER:              T3_dana_authored_ungoverned
RISK:              HIGH
PROPOSED CANONICAL:instagram-growth-director

REFERENCED BY:
  - drdana-short-form-video-plan
  - short-form-video-plan
  - instagram-funnel-diagnostician
  - instagram-weekly-growth-review

REASON:            اسم شخص في المعرّف، لكنه مذكور نصياً داخل وصف drdana-short-form-video-plan و short-form-video-plan — وكلاهما خارج نطاق الترحيل. إعادة التسمية تكسر مرجعين لا نملك تعديلهما في هذه المرحلة.
UNBLOCK:           ترحيل مهارات الفيديو في المرحلة الثانية، ثم تسمية الثلاثة معاً
```

### `drdana-short-form-video-plan`

```
ACTION:            REVIEW
TIER:              T3_dana_authored_ungoverned
RISK:              HIGH
PROPOSED CANONICAL:content-short-form-video-planner

REFERENCED BY:
  (غير محصور)

REASON:            اسم شخص في المعرّف، ومرجع متبادل مع نسخة مكررة ومع مدير النمو
UNBLOCK:           حسم المكرر أولاً (انظر duplicates)
```

### `chief-advertising-officer-cao`

```
ACTION:            REVIEW
TIER:              T3_dana_authored_ungoverned
RISK:              MEDIUM
PROPOSED CANONICAL:marketing-advertising-director

REFERENCED BY:
  (غير محصور)

REASON:            لاحقة اختصار مبهم (cao)، ولم يخضع لترقية وصف بعد؛ لا يُلمس قبل ترقيته
UNBLOCK:           قرار الطبيب/ة
```

### `whatsapp-closing-specialist`

```
ACTION:            KEEP
TIER:              T3_dana_authored_ungoverned
RISK:              LOW
PROPOSED CANONICAL:patient-inquiry-closer

REFERENCED BY:
  (غير محصور)

REASON:            معرّف وصفي سليم، لكن المجال المضبوط له هو patient لا قناة (whatsapp). يُعاد تسميته في المرحلة الثانية مع بقية مساعدي المرضى، لا الآن.
UNBLOCK:           قرار الطبيب/ة
```

### `smile-doc-standardizer`

```
ACTION:            KEEP
TIER:              T3_dana_authored_ungoverned
RISK:              LOW
PROPOSED CANONICAL:patient-case-photo-standardizer

REFERENCED BY:
  (غير محصور)

REASON:            معرّف وصفي مقبول؛ يُرحَّل مع مجال patient في المرحلة الثانية
UNBLOCK:           قرار الطبيب/ة
```

### `dr-dana-medical-dental-english`

```
ACTION:            KEEP
TIER:              T3_dana_authored_ungoverned
RISK:              LOW
PROPOSED CANONICAL:research-dental-english-editor

REFERENCED BY:
  (غير محصور)

REASON:            اسم شخص في المعرّف، لكن لا اعتمادية عليه ولا ضرر قائم؛ يؤجَّل لمجال research
UNBLOCK:           قرار الطبيب/ة
```

## تكرارات وأسماء قديمة — قرارات بلا حذف

| العنصر | المقابل | التشابه | القرار | السبب | خطوة يدوية |
|---|---|---|---|---|---|
| `short-form-video-plan` | `drdana-short-form-video-plan` | PROBABLE_DUPLICATE | **DEPRECATE** | وصفان متطابقان حرفياً تقريباً وتاريخ تحديث واحد (2026-08-02). لا قدرة فريدة في النسخة العامة. تُوسم DEPRECATED بـ deprecated_by يشير إلى drdana-short-form-video-plan. لا حذف في هذه المرحلة. | حذف المهارة من الحساب — قرار الطبيب/ة |
| `personal-brand-strategy` | `instagram-personal-brand-strategist` | HIGH | **MANUAL_REVIEW** | تشابه في الغرض لا في النطاق: النسخة العامة تغطي منصات وعلامات غير طبية، والمرقّاة مخصصة لانستغرام ولتموضع الطبيب/ة. لا يُدمجان بناءً على التشابه وحده. القرار يحتاج الطبيب/ة: هل تحتاج استراتيجية علامة خارج انستغرام؟ | — |
| `emai-test` | — | — | **DELETE_CANDIDATE** | مهارة اختبار بوصف من كلمتين، بلا مراجع، بلا قدرة فعلية | حذف من الحساب — لا يُحذف آلياً |
| `meta-ads-test` | — | — | **DELETE_CANDIDATE** | مهارة اختبار بوصف من كلمتين، بلا مراجع، بلا قدرة فعلية | حذف من الحساب — لا يُحذف آلياً |
| `lower` | — | — | **ARCHIVE** | «كاتب صحائف الدعوى» — مجال legal خارج نطاق العمل الحالي تماماً. قدرة حقيقية لا مهارة اختبار، فلا تُحذف. تُؤرشف حتى تُقرَّر. | قرار الطبيب/ة |

**لا حذف في هذه المرحلة** — حتى `DELETE_CANDIDATE` يبقى حتى قرار الطبيب/ة.

## السياسات

| المعرّف | المسار | النوع | النطاق | التجاوز | الإجراء |
|---|---|---|---|---|---|
| `house-rules` | `identity/house-rules.md` | GLOBAL_POLICY | ALL_ASSISTANTS | **ممنوع** | NORMALIZE_HEADER_ONLY |
