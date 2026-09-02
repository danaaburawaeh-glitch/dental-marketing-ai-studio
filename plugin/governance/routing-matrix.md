---
document: routing-matrix
type: GOVERNANCE
version: 1.0.0
status: ACTIVE
applies_to: ALL_ASSISTANTS
---

# مصفوفة التوجيه — Routing Matrix v1.0.0

هذا المستند مكمِّل لـ `governance/routing-policy.md` — لا يعدّل أياً من قواعدها العشر المجمَّدة (`governance/core-freeze.md`)، بل يعرضها بصيغة جدول Intent ← Skill لسهولة المراجعة البشرية والاختبار اليدوي السريع. **المرجع الحاكم فعلياً عند أي تعارض هو `routing-policy.md` + `governance/routing-tests.yaml`، لا هذا الجدول.**

## الجدول الرئيسي

| النية (Intent) | Skill الأساسية | Skill الثانوية (إن غابت الأولى/تعقيداً إضافياً) | التصعيد | خارج النطاق |
|---|---|---|---|---|
| تحليل أرقام/معدلات عامة | `instagram-data-analyst` | — | — | — |
| لماذا الحساب لا ينمو (تشخيص) | `instagram-funnel-diagnostician` | `instagram-weekly-growth-review` (مراجعة دورية) | `system-assistant-builder` (لا مساعد "استراتيجية ٩٠ يوم" حالياً) | — |
| من هو الجمهور | `instagram-audience-analyst` | — | — | — |
| تحليل منافسين | `instagram-competitor-analyst` | — | — | — |
| تصميم تجربة/اختبار A-B | `instagram-experimentation-manager` | — | — | — |
| تموضع شخصي/علامة | `instagram-personal-brand-strategist` | `marketing-strategy-planner` (خطة أشمل) | — | — |
| بناء نظام محتوى (ركائز) | `instagram-content-architect` | — | — | — |
| تحليل/كتابة ريل واحد | `instagram-reel-strategist` | `content-case-post-reviewer` (قبل نشر ريل حالة) | — | — |
| خطة فيديو قصير ٣٠ يوماً | `content-short-form-video-planner` | `instagram-reel-strategist` (سكربت تفصيلي لاحق) | — | — |
| تقويم نشر بتواريخ | `content-social-calendar-scheduler` | `instagram-content-architect` (إن لم يوجد نظام ركائز بعد) | — | — |
| أداء المحتوى المنشور | `instagram-content-performance-analyst` | `instagram-experimentation-manager` (لتحويل النتيجة لتجربة) | — | — |
| مراجعة تحويل البروفايل | `instagram-conversion-analyst` | — | — | — |
| رد على عميل/ليد متردد | `content-whatsapp-lead-responder` | `instagram-conversion-analyst` (إن كانت المشكلة بروفايل لا رسالة) | — | — |
| مراجعة منشور/صورة حالة قبل النشر | `content-case-post-reviewer` | — | — | — |
| خطة تسويقية كاملة متعددة القنوات | `marketing-strategy-planner` | `instagram-content-architect` + `instagram-personal-brand-strategist` (مدخلات) | — | — |
| اجتماع/تقرير نمو أسبوعي | `instagram-weekly-growth-review` | — | — | — |
| بناء مساعد/Skill جديدة | `system-assistant-builder` | — | — | — |
| عرض/اكتشاف المساعدين المتاحين | `system-assistant-directory` | — | — | — |
| إصلاح مساعد لا يعمل صح | `system-assistant-tuner` | — | — | — |
| حفظ معرفة دائمة | `system-knowledge-manager` | — | — | — |
| طلب مركّب (أكثر من نية حقيقية) | `system-assistant-orchestrator` | — | — | — |
| أي نية سريرية (تشخيص، علاج، دواء، تفسير أشعة) | — | — | — | **يُحجب بالكامل** — `identity/clinical-firewall.md`، القاعدة ٠ |

## معالجة الحالات الخاصة (بند ١٠ من طلب الترقية)

### طلبات غامضة (Ambiguous)

يُطبَّق `routing-policy.md § القاعدة ٩`: إن أمكن الحسم من السياق يُحسم ويُعلَن المساعد المختار في سطر؛ إن تعذّر الحسم والخطأ عالي الأثر (نشر، مريض، مال، إرسال) يُسأل سؤال واحد؛ إن كان الخطأ منخفض الأثر يُختار الأعلى تخصيصاً مع ذكر الاختيار صراحة.

### طلبات متعددة النية (Multi-Intent)

يُطبَّق `routing-policy.md § القاعدة ٧`: يُحال إلى `system-assistant-orchestrator` الذي يبني مسار تنفيذ (DAG) بدل حشر الطلب في مساعد واحد. مثال: «حللي الأرقام وقوليلي وين المشكلة وابني لي محتوى» ← `instagram-data-analyst` → `instagram-funnel-diagnostician` → `instagram-content-architect`.

### معلومات ناقصة (Missing Information)

كل Skill في هذه الحزمة تحمل قسم "ما يحتاجه قبل البدء" أو ما يعادله — إن غاب مدخل مطلوب، يُطلب بسؤال واحد مجمَّع لا بأسئلة متتالية. لا Skill تخترع بيانات غائبة.

### نوايا متعارضة (Conflicting Intent)

مثال: طلب يحوي جزءاً عاماً (تسويقي) وجزءاً سريرياً معاً («كم سعر الفينير وهل يناسبني؟»). يُطبَّق `routing-policy.md § القاعدة ٠`: يُقسَّم الطلب — الجزء العام يتابع التوجيه العادي، والجزء السريري يُحال وفق `clinical-firewall.md` بصرف النظر عن أي مساعد كان سيطابقه.

### خارج النطاق (Out-of-Scope)

أي نية سريرية (تشخيص، خطة علاج لحالة بعينها، دواء/جرعة، تفسير أشعة، طوارئ) تُحجب بالكامل قبل الوصول لأي Skill — القاعدة ٠ تُفحص أولاً وقبل كل شيء. لا Skill في هذه الحزمة تُخوَّل لمعالجة الجزء السريري. انظر `identity/clinical-firewall.md` و `governance/scope-boundary.md`.

## العلاقة بالوثائق الأخرى

```
governance/routing-policy.md   ← المرجع الحاكم فعلياً (10 قواعد مجمَّدة)
governance/routing-tests.yaml  ← الإثبات التنفيذي — 37 حالة إصابة/إقصاء، 0 فشل
knowledge/assistants-registry.md ← الدليل المولَّد آلياً من نفس metadata، تفصيل أدق لكل مساعد
skills/system-assistant-orchestrator/SKILL.md ← منطق تفكيك الطلب متعدد النية بالتفصيل
```

## سجل التحديث

| التاريخ | ما تغيّر |
|---|---|
| 2026-08-28 | إنشاء الملف — v1.3.0 Standalone Edition، يعكس 21 Skill بعد إضافة الأربعة الجديدة |
