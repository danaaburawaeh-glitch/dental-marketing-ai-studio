# دليل المساعدين — Assistants Registry

> **ملف مولَّد — لا يُحرَّر يدوياً.**
> يُنتج بـ `scripts/build_registry.py` من كتل `metadata` داخل ملفات المهارات.
> عند أي تعارض، الملف الفعلي للمهارة هو مصدر الحقيقة، ويُحل التعارض بإعادة التوليد.

**تاريخ التوليد:** 2026-09-02 · **عدد المساعدين:** 29 · **معتمد (ACTIVE):** 28

**السياسات العامة:** `identity/house-rules.md` + `identity/clinical-firewall.md` — يرثهما كل مساعد معاً، `override_allowed: false`. **حدود النطاق:** `governance/scope-boundary.md`. **سياسة التوجيه:** `governance/routing-policy.md`.

## المحتوى والنشر · `content`

| المساعد | الاسم المعروض | الغرض | يشتغل عند | لا يشتغل عند ← البديل | يفوّض إلى | أولوية | سلامة | الحالة | الإصدار | آخر اختبار |
|---|---|---|---|---|---|---|---|---|---|---|
| `content-case-post-reviewer` | مراجع منشورات الحالات | فحص مسوّدة منشور حالة قبل النشر مقابل الموافقة والخصوصية والادعاءات الطبية والامتثال الإعلاني، وتوحيد صور الحالة (قبل/بعد) بصرياً قبل النشر | «راجعي المنشور قبل النشر» · «هذا الكابشن تمام» · «أبغى أنشر حالة» | «اكتبي لي ريل» ← `instagram-reel-strategist` · «ابني نظام محتوى» ← `instagram-content-architect` | — | 95 | CRITICAL | ACTIVE | 1.3.0 | 2026-08-28 |
| `content-whatsapp-lead-responder` | مجيب محادثات العملاء | كتابة سيناريو رد جاهز للنسخ لإغلاق محادثة واتساب/انستغرام مع عميل محتمل متردد، مع اكتشاف الأداة المتاحة (ChatPlace) والتراجع للوضع اليدوي عند غيابها | «كيف أرد على هذي الرسالة» · «اكتب سيناريو إغلاق ليد متردد» · «العميل متردد» | «راجعي البايو» ← `instagram-conversion-analyst` · «ليش ما أحد يراسل» ← `instagram-conversion-analyst` · «راجعي المنشور قبل النشر» ← `content-case-post-reviewer` | — | 72 | HIGH | ACTIVE | 1.0.0 | 2026-08-28 |
| `content-short-form-video-planner` | مخطط الفيديو القصير | بناء خطة فيديو قصير ممتدة (٣٠ يوماً عادةً) عبر منصات متعددة، موزّعة على بنى مثبتة وأهداف بمزيج متوازن | «رتبي محتوى الشهر» · «خطة فيديوهات ٣٠ يوم» · «خطة فيديو شهر كامل» | «اكتبي لي ريل» ← `instagram-reel-strategist` · «تقويم نشر بتواريخ» ← `content-social-calendar-scheduler` · «ابني نظام محتوى» ← `instagram-content-architect` | `content-case-post-reviewer` | 64 | HIGH | ACTIVE | 1.0.0 | 2026-08-28 |
| `content-social-calendar-scheduler` | منسّق تقويم النشر | تحويل نظام محتوى قائم إلى تقويم نشر بتواريخ محددة (أسبوعي أو شهري)، مع اكتشاف أداة الجدولة المتاحة والتراجع لتقويم يدوي عند غيابها | «تقويم نشر بتواريخ» · «أنشئ تقويم محتوى أسبوعي» · «جدولي المنشورات» | «ابني نظام محتوى» ← `instagram-content-architect` · «خطة فيديوهات ٣٠ يوم» ← `content-short-form-video-planner` · «أنشئ خطة تسويقية كاملة» ← `marketing-strategy-planner` | — | 63 | MODERATE | ACTIVE | 1.0.0 | 2026-08-28 |

## نمو انستغرام · `instagram`

| المساعد | الاسم المعروض | الغرض | يشتغل عند | لا يشتغل عند ← البديل | يفوّض إلى | أولوية | سلامة | الحالة | الإصدار | آخر اختبار |
|---|---|---|---|---|---|---|---|---|---|---|
| `instagram-reel-strategist` | أخصائي استراتيجية الريلز | تحليل الريلز بأول ٣ ثوانٍ ومنحنى الاحتفاظ، وكتابة ريل جاهز للتصوير ببنية مثبتة | «حللي الريلز» · «ليش الريل ما مشى» · «اكتبي لي ريل» | «رتبي محتوى الشهر» ← `content-short-form-video-planner` · «وش نجح من المحتوى كله» ← `instagram-content-performance-analyst` · «راجعي هذا الريل قبل النشر» ← `content-case-post-reviewer` | `content-case-post-reviewer` | 70 | HIGH | ACTIVE | 1.3.0 | 2026-08-28 |
| `instagram-conversion-analyst` | محلل التحويل | تحديد نقطة انكسار الطريق إلى الحجز ومراجعة البروفايل بوصفه أداة تحويل | «المتابعين ما يحجزون» · «راجعي البايو» · «ليش ما أحد يراسل» | «كيف أرد على هذي الرسالة» ← `content-whatsapp-lead-responder` · «ليش المدى نازل» ← `instagram-funnel-diagnostician` · «مين جمهوري» ← `instagram-audience-analyst` | — | 68 | HIGH | ACTIVE | 1.2.0 | 2026-08-28 |
| `instagram-funnel-diagnostician` | مشخّص قمع النمو | تحديد نقطة التسرّب الواحدة في قمع النمو وإخراج أمر تنفيذي واحد بقاعدة قرار | «ليش الحساب ما ينمو» · «وين المشكلة» · «وين نخسر الناس» | «راجعي أرقام الحساب واعطيني خطة ٩٠ يوم» ← `system-assistant-builder` · «تقرير الأسبوع» ← `instagram-weekly-growth-review` · «كم معدل التفاعل» ← `instagram-data-analyst` | — | 68 | MODERATE | ACTIVE | 1.2.1 | 2026-08-28 |
| `instagram-audience-analyst` | محلل ذكاء الجمهور | تقسيم الجمهور إلى شرائح وتحديد الشريحة ذات الأولوية بلغة الجمهور نفسه | «مين جمهوري» · «مين يتابعني فعلاً» · «لمن أوجه المحتوى» | «المتابعين ما يحجزون» ← `instagram-conversion-analyst` · «وش نجح من المحتوى» ← `instagram-content-performance-analyst` | `instagram-content-architect` | 65 | MODERATE | ACTIVE | 1.2.0 | 2026-08-28 |
| `instagram-competitor-analyst` | محلل ذكاء المنافسين | استخراج آليات نجاح الحسابات المرجعية والفجوات القابلة للامتلاك، لغرض داخلي لا للنشر | «حللي هذا الحساب» · «وش يسوون المنافسين» · «وين الفجوة في السوق» | «حوّلي هذا لخطة محتوى» ← `instagram-content-architect` · «تموضعي أنا» ← `instagram-personal-brand-strategist` | `instagram-content-architect` | 65 | MODERATE | ACTIVE | 1.2.0 | 2026-08-28 |
| `instagram-content-architect` | مهندس المحتوى | بناء نظام محتوى من ٥ إلى ٧ ركائز بمزيج نشر بنِسَب مبررة، بلا جدولة زمنية | «ابني نظام محتوى» · «ركائز المحتوى» · «وش أنشر بالضبط» | «تقويم نشر بتواريخ» ← `content-social-calendar-scheduler` · «خطة فيديوهات ٣٠ يوم» ← `content-short-form-video-planner` · «ليش هذا المنشور نجح» ← `instagram-content-performance-analyst` | — | 65 | HIGH | ACTIVE | 1.3.0 | 2026-08-28 |
| `instagram-content-performance-analyst` | محلل أداء المحتوى | استخراج آلية نجاح المحتوى وفشله وتحويلها إلى صيغ قابلة للتكرار بعدد شواهد معلن | «وش نجح من المحتوى» · «ليش هذا المنشور نجح» · «ليش هذا ما مشى» | «كم معدل التفاعل» ← `instagram-data-analyst` · «اكتبي لي ريل» ← `instagram-reel-strategist` | `instagram-experimentation-manager` | 65 | MODERATE | ACTIVE | 1.2.0 | 2026-08-28 |
| `instagram-data-analyst` | محلل بيانات انستغرام | حساب مؤشرات الحساب ومعدلاته ومقارنتها بالفترة السابقة، بلا تفسير محتوى وبلا توصيات | «وش تقول الأرقام» · «احسبي المعدلات» · «قارني هالأسبوع بالسابق» | «ليش هذا المنشور نجح» ← `instagram-content-performance-analyst` · «ليش الحساب ما ينمو» ← `instagram-funnel-diagnostician` · «راجعي أرقام الحساب واعطيني خطة ٩٠ يوم» ← `system-assistant-builder` | — | 65 | MODERATE | ACTIVE | 1.1.1 | 2026-08-28 |
| `instagram-experimentation-manager` | مدير تجارب النمو | تصميم تجربة بمتغير واحد وقاعدة قرار مكتوبة مسبقاً، وقراءة نتيجتها بحكم صريح | «نجرب إيش» · «أبغى أختبر» · «خطّاف A ولا B» | «ليش الحساب ما ينمو» ← `instagram-funnel-diagnostician` · «كم معدل التفاعل» ← `instagram-data-analyst` | — | 65 | MODERATE | ACTIVE | 1.2.1 | 2026-08-28 |
| `instagram-personal-brand-strategist` | استراتيجي العلامة الشخصية | بناء تموضع الطبيب/ة وجملة العلامة الواحدة ومزيج الأوجه، من دليل لا من طموح | «تموضعي» · «كيف يشوفوني الناس» · «حسابي صار إعلانات» | «خطة تسويقية كاملة» ← `marketing-strategy-planner` · «لينكدإن» ← `marketing-strategy-planner` · «ابني نظام محتوى» ← `instagram-content-architect` | — | 65 | HIGH | ACTIVE | 1.3.0 | 2026-08-28 |
| `instagram-weekly-growth-review` | اجتماع النمو الأسبوعي | تجميع مخرجات فريق النمو في تقرير أسبوعي ينتهي بخمسة إجراءات مرحَّلة ومراجَعة | «اجتماع الأسبوع» · «تقرير الأسبوع» · «اجمعي الفريق» | «خطة ٩٠ يوم» ← `system-assistant-builder` · «ليش الحساب ما ينمو» ← `instagram-funnel-diagnostician` | `instagram-data-analyst` · `instagram-content-performance-analyst` · `instagram-reel-strategist` | 60 | MODERATE | ACTIVE | 1.2.2 | 2026-08-28 |

## التسويق والإعلانات · `marketing`

| المساعد | الاسم المعروض | الغرض | يشتغل عند | لا يشتغل عند ← البديل | يفوّض إلى | أولوية | سلامة | الحالة | الإصدار | آخر اختبار |
|---|---|---|---|---|---|---|---|---|---|---|
| `marketing-roi-analyst` | محلل العائد التسويقي | حساب وشرح كفاءة الإنفاق التسويقي من CPL وCAC وتكلفة الحجز إلى ROAS والعائد عندما تتوفر بيانات سليمة | «احسب ROAS» · «كم تكلفة الحجز» · «احسب CAC» | «خطة إعلانات مدفوعة» ← `marketing-paid-media-planner` · «وش تقول أرقام الانستغرام» ← `instagram-data-analyst` · «ليش الليد ما يحجز» ← `marketing-lead-funnel-optimizer` | — | 80 | MODERATE | ACTIVE | 1.0.0 | 2026-09-02 |
| `marketing-lead-funnel-optimizer` | محسن قمع العملاء المحتملين | تشخيص وتحسين الرحلة من الإعلان أو المحتوى حتى الحجز وتحديد نقطة التسرب الأعلى أثراً | «ليش الليد ما يحجز» · «حلل القمع من الإعلان للحجز» · «وين نخسر العملاء المحتملين» | «اكتب متابعة لليد» ← `sales-lead-followup-manager` · «راجعي البايو» ← `instagram-conversion-analyst` · «احسب تكلفة الحجز» ← `marketing-roi-analyst` | — | 76 | MODERATE | ACTIVE | 1.0.0 | 2026-09-02 |
| `marketing-paid-media-planner` | مخطط الإعلانات المدفوعة | بناء خطة إعلانات مدفوعة متعددة المنصات بأهداف وميزانية واختبارات وقياس واضح | «خطة إعلانات مدفوعة» · «وزع ميزانية الإعلانات» · «حملة ميتا» | «احسب ROAS» ← `marketing-roi-analyst` · «صمم عرض تسويقي» ← `marketing-offer-architect` · «ليش الليد ما يحجز» ← `marketing-lead-funnel-optimizer` | — | 74 | HIGH | ACTIVE | 1.0.0 | 2026-09-02 |
| `marketing-campaign-director` | مدير الحملات التسويقية | تحويل هدف أو إطلاق إلى حملة متكاملة متعددة القنوات بمراحل وأصول ومسؤوليات وقياس | «ابنِ حملة إطلاق» · «حملة 30 يوم متكاملة» · «حملة موسمية» | «استراتيجية تسويق شاملة» ← `marketing-strategy-planner` · «تقويم نشر بتواريخ» ← `content-social-calendar-scheduler` · «خطة إعلانات مدفوعة» ← `marketing-paid-media-planner` | — | 73 | HIGH | ACTIVE | 1.0.0 | 2026-09-02 |
| `marketing-offer-architect` | مهندس العرض التسويقي | تصميم عرض تسويقي قابل للتحويل لخدمة أو باقة دون وعود مضللة أو خصومات عشوائية | «صمم عرض تسويقي» · «صمم عرض للفينيرز» · «كيف أبني باقة» | «خطة إعلانات مدفوعة» ← `marketing-paid-media-planner` · «خطة تسويقية كاملة» ← `marketing-strategy-planner` · «احسب العائد على الإعلان» ← `marketing-roi-analyst` | — | 72 | HIGH | ACTIVE | 1.0.0 | 2026-09-02 |
| `marketing-local-seo-geo-strategist` | استراتيجي الظهور المحلي وSEO/GEO | بناء خطة ظهور محلي في Google ومحركات الإجابة والذكاء الاصطناعي عبر صفحات الخدمة والكيانات والمراجعات والمحتوى الداعم | «طور SEO المحلي» · «أريد الظهور في بحث الذكاء الاصطناعي» · «خطة GEO» | «حلل منافسين الانستغرام» ← `instagram-competitor-analyst` · «خطة إعلانات مدفوعة» ← `marketing-paid-media-planner` · «خطة تسويقية كاملة» ← `marketing-strategy-planner` | — | 71 | MODERATE | ACTIVE | 1.0.0 | 2026-09-02 |
| `marketing-strategy-planner` | مخطط الاستراتيجية التسويقية | بناء خطة تسويقية كاملة متعددة القنوات (تشمل لينكدإن كقناة) بأهداف ومؤشرات ومراحل زمنية، مبنية على تموضع ونظام محتوى قائمين | «أنشئ خطة تسويقية كاملة» · «خطة حملة لمدة ٣٠ يوماً» · «استراتيجية تسويق شاملة» | «ابني نظام محتوى» ← `instagram-content-architect` · «تموضعي» ← `instagram-personal-brand-strategist` · «تقويم نشر بتواريخ» ← `content-social-calendar-scheduler` | — | 66 | HIGH | ACTIVE | 1.1.0 | 2026-09-02 |

## مبيعات · `sales`

| المساعد | الاسم المعروض | الغرض | يشتغل عند | لا يشتغل عند ← البديل | يفوّض إلى | أولوية | سلامة | الحالة | الإصدار | آخر اختبار |
|---|---|---|---|---|---|---|---|---|---|---|
| `sales-lead-followup-manager` | مدير متابعة العملاء المحتملين | تصميم تسلسل متابعة وتأهيل للعملاء المحتملين حتى الحجز مع قواعد توقيت وإغلاق واضحة | «اكتب متابعة لليد» · «خطة متابعة واتساب» · «الليد ما رد» | «كيف أرد على هذي الرسالة» ← `content-whatsapp-lead-responder` · «ليش الليد ما يحجز» ← `marketing-lead-funnel-optimizer` · «حلل تكلفة الليد» ← `marketing-roi-analyst` | — | 78 | HIGH | ACTIVE | 1.0.0 | 2026-09-02 |

## النظام والحوكمة · `system`

| المساعد | الاسم المعروض | الغرض | يشتغل عند | لا يشتغل عند ← البديل | يفوّض إلى | أولوية | سلامة | الحالة | الإصدار | آخر اختبار |
|---|---|---|---|---|---|---|---|---|---|---|
| `system-update-checker` | فاحص التحديثات | مقارنة الإصدار المثبت بأحدث GitHub Release وإعطاء حالة التحديث ورابط التنزيل | «هل يوجد تحديث» · «تحقق من التحديثات» · «حدث المساعد» | «المساعد ما اشتغل» ← `system-assistant-tuner` | — | 92 | LOW | ACTIVE | 1.0.0 | 2026-09-02 |
| `system-assistant-directory` | دليل المساعدين | عرض المساعدين المتاحين وتوجيه الطلب إلى الصحيح منهم وفق سياسة التوجيه | «وش المساعدين عندي» · «اعرضي المساعدين» · «مين يساعدني في» | «ابني لي مساعد جديد» ← `system-assistant-builder` · «المساعد ما اشتغل» ← `system-assistant-tuner` · «هل يوجد تحديث» ← `system-update-checker` | — | 90 | MODERATE | ACTIVE | 1.1.2 | 2026-08-28 |
| `system-assistant-orchestrator` | منسّق المساعدين | تفكيك طلب مركّب إلى مسار تنفيذ متعدد المساعدين (DAG)، وتنسيق التسليم بينهم، وتجميع النتيجة — بلا تنفيذ تخصصي بنفسه | «حللي الأرقام واكتشفي المشكلة وابني لي محتوى» · «نفذي هذي كخطوات متتالية» · «نسّقي بين أكثر من مساعد» | «وش المساعدين عندي» ← `system-assistant-directory` · «مين يقدر يساعدني في» ← `system-assistant-directory` · «اكتبي لي ريل» ← `instagram-reel-strategist` | — | 80 | HIGH | TESTING | 1.0.2 | 2026-08-28 |
| `system-assistant-builder` | صانع المساعدين | بناء مساعد مخصص جديد من مقابلة إلى ملف skill مختبَر وجاهز للتثبيت | «ابني لي مساعد» · «أبغى مساعد جديد» · «سوّي لي موظف» | «عدّلي المساعد الموجود» ← `system-assistant-tuner` · «وش المساعدين عندي» ← `system-assistant-directory` · «احفظي هذا للمساعد» ← `system-knowledge-manager` | `system-knowledge-manager` | 75 | MODERATE | ACTIVE | 1.2.2 | 2026-08-28 |
| `system-assistant-tuner` | صيانة وتحسين المساعدين | تشخيص سبب فشل مساعد في التشغيل أو المخرَج وإصلاح الموضع المسبِّب وحده وإعادة اختباره | «المساعد ما اشتغل» · «اشتغل المساعد الغلط» · «عدّلي المساعد» | «ابني لي مساعد جديد» ← `system-assistant-builder` · «احفظي هذي المعلومة للمساعد» ← `system-knowledge-manager` | `system-knowledge-manager` | 75 | MODERATE | ACTIVE | 1.2.0 | 2026-08-28 |
| `system-knowledge-manager` | قاعدة معرفة المساعدين | تحويل الملفات إلى معرفة دائمة منظّمة داخل ملفات الإضافة وربطها بالمساعدين وصيانة فهرسها | «احفظي هذا للمساعد» · «ضيفي هذا لقاعدة المعرفة» · «خليه يعرف هذا» | «ابني لي مساعد» ← `system-assistant-builder` · «وش المساعدين عندي» ← `system-assistant-directory` | — | 75 | HIGH | ACTIVE | 1.1.1 | 2026-08-28 |

## المعرّفات القديمة المقبولة — Legacy Aliases

تُقبل في الطلبات القديمة ولا تُستخدم في أي ملف جديد.

| المعرّف القديم | المعرّف الكانوني |
|---|---|
| `case-post-reviewer` | `content-case-post-reviewer` |
| `5-reel-strategy-specialist-inst` | `instagram-reel-strategist` |
| `10-conversion-analyst-inst` | `instagram-conversion-analyst` |
| `1-chief-growth-officer-inst` | `instagram-funnel-diagnostician` |
| `3-audience-intelligence-analyst-insta` | `instagram-audience-analyst` |
| `7-competitor-intelligence-analyst-insta` | `instagram-competitor-analyst` |
| `9-content-architect-inst` | `instagram-content-architect` |
| `4-content-performance-analyst-inst` | `instagram-content-performance-analyst` |
| `2-instagram-data-analyst-inst` | `instagram-data-analyst` |
| `8-growth-experimentation-manager-inst` | `instagram-experimentation-manager` |
| `6-personal-brand-strategist-inst` | `instagram-personal-brand-strategist` |
| `11-weekly-growth-meeting-inst` | `instagram-weekly-growth-review` |
| `assistant-directory` | `system-assistant-directory` |
| `new-assistant` | `system-assistant-builder` |
| `assistant-tuning` | `system-assistant-tuner` |
| `assistant-knowledge` | `system-knowledge-manager` |

## مؤجَّل إلى المرحلة التالية — خارج نطاق الترحيل الحالي

| المعرّف | الإجراء | الخطر | المعرّف الكانوني المقترح | السبب |
|---|---|---|---|---|
| `dana-instagram-growth-director` | DANGLING_REFERENCE_REMOVED | HIGH | `—` | تحقُّق مباشر عبر ListSkills بتاريخ 2026-08-28 أثبت أن هذا المعرّف غير موجود في حساب الطبيب/ة حالياً بأي اسم — لا تحت هذا الاسم ولا أي نسخة قديمة مرقّمة (كان يُفترض أنه أحد الإحدى عشرة القديمة المذكورة في README § البدء ٢). الافتراض السابق هنا (أنه موجود وينتظر إعادة تسمية في مرحلة ثانية) لم يعد صحيحاً — يبدو أنه حُذف دون بديل، لا أُعيد تسميته. |
| `drdana-short-form-video-plan` | RESOLVED_INTERNAL_V1.3.0 | HIGH | `content-short-form-video-planner` | اسم شخص في المعرّف، ومرجع متبادل مع نسخة مكررة ومع مدير النمو |
| `chief-advertising-officer-cao` | REVIEW | MEDIUM | `marketing-advertising-director` | لاحقة اختصار مبهم (cao)، ولم يخضع لترقية وصف بعد؛ لا يُلمس قبل ترقيته |
| `whatsapp-closing-specialist` | RESOLVED_INTERNAL_V1.3.0 | LOW | `patient-inquiry-closer` | معرّف وصفي سليم، لكن المجال المقترَح هنا (patient) خارج نطاق هذا الاستوديو — governance/scope-boundary.md يمنع domain: patient صراحة لهذه الإضافة. |
| `smile-doc-standardizer` | RESOLVED_INTERNAL_V1.3.0 | LOW | `patient-case-photo-standardizer` | معرّف وصفي مقبول، لكن المجال المقترَح هنا (patient) خارج نطاق هذا الاستوديو. |
| `dr-dana-medical-dental-english` | KEEP | LOW | `research-dental-english-editor` | اسم شخص في المعرّف، لكن لا اعتمادية عليه ولا ضرر قائم؛ يؤجَّل لمجال research |
| `marketing-strategy-director` | RESOLVED_INTERNAL_V1.3.0 | HIGH | `marketing-strategy-planner` | لم يكن مذكوراً في migration-spec.yaml الأصلي — اكتُشف أثناء تدقيق الاعتماديات لـ v1.3.0 (Standalone) عبر فحص شامل لكل negative_triggers، لا افتراضاً أنه المعرّف الوحيد المفقود. |
| `linkedin-strategy` | RESOLVED_INTERNAL_V1.3.0 | MEDIUM | `marketing-strategy-planner` | مثل marketing-strategy-director أعلاه — اكتُشف أثناء تدقيق v1.3.0. |
| `social-media-calendar` | RESOLVED_INTERNAL_V1.3.0 | HIGH | `content-social-calendar-scheduler` | مثل marketing-strategy-director أعلاه — اكتُشف أثناء تدقيق v1.3.0. |

## تكرارات وأسماء قديمة — قرارات موثَّقة بلا حذف

| العنصر | المقابل | التشابه | القرار | السبب |
|---|---|---|---|---|
| `short-form-video-plan` | `drdana-short-form-video-plan` | PROBABLE_DUPLICATE | DEPRECATE | وصفان متطابقان حرفياً تقريباً وتاريخ تحديث واحد (2026-08-02). لا قدرة فريدة في النسخة العامة. تُوسم DEPRECATED بـ deprecated_by يشير إلى drdana-short-form-video-plan. لا حذف في هذه المرحلة. |
| `personal-brand-strategy` | `instagram-personal-brand-strategist` | HIGH | MANUAL_REVIEW | تشابه في الغرض لا في النطاق: النسخة العامة تغطي منصات وعلامات غير طبية، والمرقّاة مخصصة لانستغرام ولتموضع الطبيب/ة. لا يُدمجان بناءً على التشابه وحده. القرار يحتاج الطبيب/ة: هل تحتاج استراتيجية علامة خارج انستغرام؟ |
| `emai-test` | — | — | DELETE_CANDIDATE | مهارة اختبار بوصف من كلمتين، بلا مراجع، بلا قدرة فعلية |
| `meta-ads-test` | — | — | DELETE_CANDIDATE | مهارة اختبار بوصف من كلمتين، بلا مراجع، بلا قدرة فعلية |
| `lower` | — | — | ARCHIVE | «كاتب صحائف الدعوى» — مجال legal خارج نطاق العمل الحالي تماماً. قدرة حقيقية لا مهارة اختبار، فلا تُحذف. تُؤرشف حتى تُقرَّر. |

---

لإعادة التوليد بعد أي تعديل:

```bash
python3 scripts/validate_system.py --skills <مجلد> --policy identity/house-rules.md
python3 scripts/routing_tests.py  --skills <مجلد> --tests governance/routing-tests.yaml
python3 scripts/build_registry.py --skills <مجلد> --out knowledge/assistants-registry.md \
                                  --deferred governance/migration-spec.yaml
```
