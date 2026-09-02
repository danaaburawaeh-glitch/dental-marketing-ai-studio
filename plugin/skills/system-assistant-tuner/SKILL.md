---
name: system-assistant-tuner
description: >
  صيانة وتحسين المساعدين — يشخّص لماذا لا يشتغل مساعد أو يشتغل في الوقت الخطأ أو يعطي مخرجاً رديئاً، ويصلحه
  ويعيد تغليفه (مكافئ Configure/Edit في Custom GPT). This skill should be used when the user says "المساعد ما
  اشتغل", "اشتغل المساعد الغلط", "عدّلي المساعد", "ردّه صار سيئ", "خليه يسوي كذا بدل كذا", "حدّثي المهارة",
  "الرد طويل/قصير", or in English "fix my assistant", "the wrong skill triggered", "the assistant didn't fire",
  "update the skill", "improve the assistant's output", "edit my assistant". Diagnoses first, then fixes the
  specific cause.
metadata:
  assistant_id: system-assistant-tuner
  display_name: صيانة وتحسين المساعدين
  domain: system
  role: maintainer
  purpose: تشخيص سبب فشل مساعد في التشغيل أو المخرَج وإصلاح الموضع المسبِّب وحده وإعادة اختباره
  triggers:
  - المساعد ما اشتغل
  - اشتغل المساعد الغلط
  - عدّلي المساعد
  - ردّه صار سيئ
  - fix my assistant
  - the wrong skill triggered
  - update the skill
  negative_triggers:
  - match: ابني لي مساعد جديد
    route_to: system-assistant-builder
  - match: احفظي هذي المعلومة للمساعد
    route_to: system-knowledge-manager
  required_inputs:
  - ما قيل حرفياً
  - ما كان متوقعاً
  - ما حصل فعلاً
  optional_inputs: []
  outputs:
  - تشخيص بسطر
  - التعديل الأصغر الكافي
  - نتيجة إعادة الاختبار
  - إصدار مرفوع
  knowledge_dependencies:
  - knowledge/assistants-registry.md
  policy_dependencies:
  - house-rules
  - clinical-firewall
  - routing-policy
  skill_dependencies: []
  tool_dependencies:
  - bash
  - edit
  can_delegate_to:
  - system-knowledge-manager
  cannot_delegate_to: []
  handoff_contract:
    accepts_from: []
    delegates_to:
    - system-knowledge-manager
    required_inputs:
    - ما قيل حرفياً
    - ما كان متوقعاً
    - ما حصل فعلاً
    guaranteed_outputs:
    - تشخيص بسطر
    - التعديل الأصغر الكافي
    - نتيجة إعادة الاختبار
    - إصدار مرفوع
  routing_priority: 75
  safety_level: MODERATE
  status: ACTIVE
  version: 1.2.0
  last_tested_version: 1.2.0
  owner: clinic-owner
  created_at: '2026-08-21'
  last_updated: '2026-08-21'
  last_tested: '2026-08-28'
  evaluation_suite: governance/routing-tests.yaml
  legacy_aliases:
  - assistant-tuning
  deprecated_by: null
  notes: أُضيفت clinical-firewall إلى policy_dependencies ضمن فصل نطاق العيادة/التسويق عن السريري — 2026-08-21
---













# صيانة وتحسين المساعدين

المشكلة الواحدة لها سبب واحد. شخّص أولاً، ثم أصلح المكان الصحيح — تعديل الجسم لن يصلح مشكلة تشغيل، وتعديل الوصف لن يحسّن مخرَجاً رديئاً.

## جدول التشخيص

| العرض | السبب شبه المؤكد | مكان الإصلاح |
|---|---|---|
| المساعد لم يشتغل أصلاً | الوصف لا يحتوي العبارة التي قالها/تها الطبيب/ة | `description` |
| اشتغل مساعد آخر | وصفان متداخلان بلا سطر تمييز | `description` في **الاثنين** |
| اشتغل لكن سأل أسئلة كثيرة | المدخلات غير معرَّفة أو بلا افتراضات | قسم «ما يحتاجه» |
| المخرَج مختلف كل مرة | «شكل المخرَج» عام | قسم «شكل المخرَج» |
| المخرَج طويل أو قصير | لا يوجد سقف طول | «شكل المخرَج» |
| ينسى معلومة معروفة | المعرفة غير محفوظة أو غير مربوطة | مهارة `system-knowledge-manager` |
| تجاوز حداً (أرسل، وعد بنتيجة، ذكر اسم مريض) | قسم «الحدود» ناقص أو رخو | «الحدود» — بصيغة قاطعة |
| النبرة غير مناسبة | `identity/house-rules.md §١-٢` بيانات ناقصة أو خطأ، أو المساعد لا يُصرِّح بـ `house-rules` في `policy_dependencies` | `identity/house-rules.md` أو `policy_dependencies` |

## الخطوات

### ١. اجمع الواقعة
اطلب من الطبيب/ة: ماذا قال/ت حرفياً، وماذا توقّع/ت، وماذا حصل. بلا هذه الثلاثة، التشخيص تخمين.

### ٢. اقرأ المساعد
اقرأ `SKILL.md` الحالي كاملاً. إن كان تعارض تشغيل، اقرأ أوصاف كل المساعدين المتنافسين. الدليل في `knowledge/assistants-registry.md`.

### ٣. اعرض السبب قبل التعديل
سطر واحد: «السبب: وصف المساعد لا يذكر عبارة "…" التي استخدمتِها.» احصل على تأكيد أن التشخيص يطابق ما حصل.

### ٤. أصلح — أصغر تغيير يكفي
لا تعد كتابة المهارة. عدّل القسم المسبِّب فقط. إعادة الكتابة الكاملة تُدخل أخطاء جديدة وتفقد ما كان يعمل.

**عند إصلاح وصف:** أضف العبارة الحرفية التي استخدمها/تها الطبيب/ة. العبارة كما قالها/تها، لا كما «يُفترض» أن تُقال.

**عند إصلاح تداخل:** أضف لكل مساعد سطر «لا يشتغل عند: … استخدم `اسم-الآخر`». التعديل في طرف واحد لا يكفي.

**عند إصلاح مخرَج:** حوّل الوصف العام إلى بنية مرقّمة بسقوف طول.

### ٥. اختبر
- **تشغيل:** ٥ جمل — ٣ يجب أن تشغّله، ٢ يجب ألا تشغّلاه (قريبة لكن تخص غيره). أعد القراءة وقرر من الوصف وحده.
- **مخرَج:** أعد تشغيل نفس الحالة التي فشلت، واعرض النتيجة الجديدة على الطبيب/ة.
- **حدود:** إن كان الإصلاح متعلقاً بتجاوز حد، اختبر الحالة التي يجب أن يرفضها.
- **بنيوي:** `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/validate_assistant.py <المسار>`

### ٦. أصدر
- ارفع `metadata.version` وفق `governance/lifecycle-versioning.md`: PATCH لتصحيح لا يغيّر السلوك · MINOR لعبارة تشغيل أو قدرة جديدة · MAJOR لتغيّر الغرض أو الحدود أو المعرّف.
- **رفع الإصدار يُسقط الاعتماد تلقائياً:** بعد الرفع تصبح `last_tested_version != version`، فالحالة الصحيحة `TESTING` لا `ACTIVE`، والفاحص يفرض ذلك. أعد الاختبار ثم اختم بـ `scripts/stamp_tested.py` وارفع الحالة إلى `ACTIVE`.
- إن غيّرت معرّفاً: أضف المعرّف القديم إلى `legacy_aliases`، وسجّل القيد في `governance/assistant-id-migration-map.md`، وحدّث كل مرجع إليه.
- أعد توليد الدليل بـ `scripts/build_registry.py` — لا تحرّره يدوياً.
- غلّف: `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/package_assistant.py <المسار>`
- سلّم عبر `SendUserFile` وقل صراحة: **احفظي النسخة الجديدة من البطاقة، وهي تحل محل القديمة.**
- حدّث الدليل: الإصدار، تاريخ التحديث، وسطر في «تعارضات معروفة» إن كان الإصلاح تداخلاً.

## المراجعة الدورية

عند طلب «راجعي المساعدين»:

1. مساعد لم يُستخدم منذ فترة طويلة → هل السبب أنه غير مطلوب أم أن وصفه لا يشتغل؟ الثاني قابل للإصلاح.
2. مساعدون يتشابهون في المهمة → ادمج أو ميّز.
3. مساعدون يفعلون خمسة أشياء → اقترح تقسيمهم.
4. معرفة تجاوزت موعد مراجعتها → أحِل إلى `system-knowledge-manager`.
5. أقسام السلامة والخصوصية موجودة في كل مساعد يتعامل مع مرضى أو محتوى طبي → إن غابت، أضفها فوراً، لا تنتظر طلباً.

## قاعدة

لا تسلّم تعديلاً لم تختبره. المساعد المعدَّل غير المختبر أسوأ من المساعد المعطوب المعروف عطبه.
