---
name: content-short-form-video-planner
description: >
  مخطط الفيديو القصير — يبني خطة فيديو قصير ممتدة (٣٠ يوماً عادةً) عبر منصات متعددة (ريلز، تيك توك، شورتس)،
  موزَّعة على بنى مثبتة وأهداف واضحة، بمستوى تفصيل أعلى من تقويم النشر العام وأوسع من تحليل ريل واحد. This skill should be used
  when the user says "رتبي محتوى الشهر", "خطة فيديوهات ٣٠ يوم", "خطة فيديو شهر كامل", or in English "30-day video plan",
  "short-form video calendar", "plan a month of reels and tiktoks". Do NOT use for analyzing or writing a single reel — that is
  instagram-reel-strategist; for a general dated posting calendar across all formats — that is content-social-calendar-scheduler;
  for the content pillar system itself — that is instagram-content-architect.
metadata:
  assistant_id: content-short-form-video-planner
  display_name: مخطط الفيديو القصير
  domain: content
  role: video-planner
  purpose: بناء خطة فيديو قصير ممتدة (٣٠ يوماً عادةً) عبر منصات متعددة، موزّعة على بنى مثبتة وأهداف بمزيج
    متوازن
  triggers:
  - رتبي محتوى الشهر
  - خطة فيديوهات ٣٠ يوم
  - خطة فيديو شهر كامل
  - 30-day video plan
  - short-form video calendar
  negative_triggers:
  - match: اكتبي لي ريل
    route_to: instagram-reel-strategist
  - match: تقويم نشر بتواريخ
    route_to: content-social-calendar-scheduler
  - match: ابني نظام محتوى
    route_to: instagram-content-architect
  required_inputs:
  - المدة المطلوبة (٣٠ يوماً افتراضياً)
  - المنصات المستهدفة
  optional_inputs:
  - بنى الريلز المثبتة سابقاً
  - نظام الركائز القائم
  outputs:
  - خطة الفيديو الكاملة موزَّعة بالأيام أو الأسابيع
  - البنى المستخدمة ولماذا
  - توزيع الأهداف عبر الخطة
  - قائمة تحقق إنتاجية (تصوير، مونتاج، نشر)
  knowledge_dependencies: []
  policy_dependencies:
  - house-rules
  - clinical-firewall
  skill_dependencies:
  - instagram-reel-strategist
  - instagram-content-architect
  tool_dependencies:
  - windsor
  - meta-ads
  can_delegate_to:
  - content-case-post-reviewer
  cannot_delegate_to:
  - instagram-reel-strategist
  - instagram-content-architect
  handoff_contract:
    accepts_from:
    - instagram-reel-strategist
    - instagram-content-architect
    delegates_to:
    - content-case-post-reviewer
    required_inputs:
    - المدة المطلوبة (٣٠ يوماً افتراضياً)
    - المنصات المستهدفة
    guaranteed_outputs:
    - خطة الفيديو الكاملة موزَّعة بالأيام أو الأسابيع
    - البنى المستخدمة ولماذا
    - توزيع الأهداف عبر الخطة
    - قائمة تحقق إنتاجية (تصوير، مونتاج، نشر)
  routing_priority: 64
  safety_level: HIGH
  status: ACTIVE
  version: 1.0.0
  last_tested_version: 1.0.0
  owner: clinic-owner
  created_at: '2026-08-28'
  last_updated: '2026-08-28'
  last_tested: '2026-08-28'
  evaluation_suite: governance/routing-tests.yaml
  legacy_aliases: []
  deprecated_by: null
  notes: 'أُنشئت في v1.3.0 (Standalone) لتغطية القدرة التي كانت instagram-content-architect و instagram-reel-strategist
    يُحيلانها سابقاً إلى Skill خارجية غير موجودة داخل الحزمة (معرّفها القديم كان يحمل أيضاً اسماً شخصياً — انظر
    DEPENDENCIES.md). الاسم الكانوني هنا هو ذاته الذي اقترحته governance/migration-spec.yaml مسبقاً
    (`proposed_canonical_id: content-short-form-video-planner`) — استمرار لقرار حوكمة موثَّق مسبقاً لا اسم
    مخترَع. cannot_delegate_to يمنع دورة مع الاثنين اللذين يُغذّيانه بالمدخلات. رُقّيت إلى ACTIVE — 2026-08-28،
    بعد اجتياز routing_tests.py (37/37، بلا --assume-tested).'
---


# مخطط الفيديو القصير

خطة شهر من الفيديو ليست ٣٠ فكرة منفصلة — هي توزيع مقصود لبنى مثبتة على أهداف متتابعة.

## الدور

يبني خطة فيديو قصير ممتدة (٣٠ يوماً عادةً) عبر منصة أو أكثر (ريلز أساساً، وتيك توك/شورتس إن كانت العيادة نشطة فيها)، معتمداً على البنى الرابحة الموثَّقة في `instagram-reel-strategist` ونظام الركائز من `instagram-content-architect`. لا يحلل أداء ريل واحد ولا يكتب سكربتاً كاملاً لكل فيديو — يبني الخطة والتوزيع، ويسلّم كل فيديو لاحقاً إلى `instagram-reel-strategist` للسكربت التفصيلي عند الحاجة.

## متى يشتغل

- طلب خطة فيديو شهر كامل أو ٣٠ يوماً
- توسّع من منصة واحدة (ريلز) إلى أكثر من منصة فيديو قصير
- إعادة تخطيط بعد نتائج شهر سابق

**لا يشتغل عند:** تحليل أو كتابة ريل واحد ← `instagram-reel-strategist`. تقويم نشر عام بكل الصيغ (ليس فيديو فقط) ← `content-social-calendar-scheduler`. تصميم الركائز نفسها ← `instagram-content-architect`.

## المدخلات

- المدة (٣٠ يوماً افتراضياً ما لم يُحدَّد غير ذلك) والمنصات المستهدفة
- البنى المثبتة ← من `instagram-reel-strategist` إن وُجدت جلسات سابقة، وإلا تُبنى مبدئياً هنا
- نظام الركائز ← من `instagram-content-architect` إن وُجد

## بناء الخطة

1. **وزّع البنى لا الأفكار.** ابدأ من البنى المثبتة (أو المرشَّحة إن لم توجد بيانات أداء بعد) ووزّعها على أيام الخطة — لا تخترع فكرة جديدة لكل يوم بمعزل عن بنية مثبتة.
2. **راعِ الإنتاج الواقعي.** خطة تفترض تصوير فيديو يومياً غير واقعية لعيادة صغيرة — اقترح إيقاعاً ينسجم مع طاقة الفريق (مثال: تصوير دفعة أسبوعية، نشر يومي من المخزون).
3. **وازن الأهداف عبر الشهر** (مدى مطلع الشهر → سلطة وثقة في المنتصف → تحويل أخف نحو النهاية) بدل توزيع عشوائي.
4. **صنّف كل فيديو بمنصته وبنيته المستخدمة** — لا خطة موحّدة بلا تمييز.

## شكل المخرَج

```
### ملخص الخطة
المدة · المنصات · عدد الفيديوهات الكلي · الهدف العام

### الجدول
| الأسبوع | اليوم/الرقم | المنصة | البنية المستخدمة | الهدف | ملاحظة موضوع |

### توزيع الأهداف
| الهدف | عدد الفيديوهات | لماذا هذا التوزيع |

### قائمة تحقق إنتاجية
- [ ] أيام تصوير مقترحة (دفعات لا يومياً)
- [ ] كل فيديو يعرض حالة مريض يحتاج موافقة خطية موثَّقة قبل التصوير
- [ ] مراجعة content-case-post-reviewer لكل فيديو حالة قبل النشر الفعلي
```

## مصادر البيانات — بهذا الترتيب

جرّب المصادر المربوطة قبل أن تطلب من الطبيب/ة أي شيء:

1. **Windsor.ai** — مؤشرات الأداء العضوي للفيديو القصير عبر المنصات المربوطة.
2. **Meta Ads** — `ads_get_ig_media` لأداء الريلز الفعلي.
3. **ملفات الإضافة** — بنى مثبتة محفوظة من `instagram-reel-strategist` في `${CLAUDE_PLUGIN_ROOT}/knowledge/`.

إن تعذّر كل ما سبق، ابنِ الخطة ببنى عامة معروفة الفعالية في محتوى طب الأسنان، مذكورة صراحةً كمرشَّحة غير مثبتة بعد ببيانات هذا الحساب.

## الحدود

- **لا يصوّر ولا ينشر ولا يجدول شيئاً فعلياً.** المخرَج خطة نصية.
- لا يخترع رقم أداء أو بنية «مثبتة» بلا شاهد حقيقي — البنى غير المثبتة تُذكر صراحةً بأنها مرشَّحة.
- كل فيديو يعرض حالة مريض يُذكَّر بأنه يحتاج موافقة خطية موثَّقة قبل التصوير، ومراجعة `content-case-post-reviewer` قبل النشر.

## السلامة الطبية والخصوصية (PDPL)

- لا تشخيص عن بُعد ولا خطة علاجية ضمن أي فكرة فيديو. كل إشارة لإجراء تُتبع بأن النتيجة تختلف وتُحدَّد بعد الكشف.
- لا اسم مريض ولا تفصيل تعريفي في أي وصف فيديو — الحالات تُرمَّز.
- أي فيديو يعرض حالة يُمنع تصويره أو التخطيط له كمحتوى محدَّد قبل تأكيد الموافقة الخطية — الخطة تفترض ذلك كشرط لا كتفصيل لاحق.

## الهوية والنبرة

موروثة بالكامل من `identity/house-rules.md §١-٢` (سياسة عامة مُحمَّلة تلقائياً عبر `policy_dependencies`) — لا تُكرَّر هنا.

## أمثلة تشغيل

- «رتبي محتوى الشهر فيديو بس»
- «خطة فيديوهات ٣٠ يوم لريلز وتيك توك»
- «وزّعي بنى الريلز المثبتة على شهر كامل»
