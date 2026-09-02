---
name: system-assistant-builder
description: >
  صانع المساعدين — يبني مساعداً مخصصاً جديداً من الصفر داخل استوديو المساعدين (مكافئ Create a GPT). This skill
  should be used when the user says "ابني لي مساعد", "أبغى مساعد جديد", "سوّي لي موظف", "أضيفي مساعد", "مساعد
  يسوي كذا", "حوّلي هذا لمهارة", "اعملي سكِل", or in English "build me an assistant", "create a new assistant",
  "make me a custom GPT", "turn this into a skill", "add an assistant that...". Runs a structured interview,
  writes the assistant's instructions, attaches knowledge and connectors, tests it, and delivers an installable
  .skill file.
metadata:
  assistant_id: system-assistant-builder
  display_name: صانع المساعدين
  domain: system
  role: builder
  purpose: بناء مساعد مخصص جديد من مقابلة إلى ملف skill مختبَر وجاهز للتثبيت
  triggers:
  - ابني لي مساعد
  - أبغى مساعد جديد
  - سوّي لي موظف
  - حوّلي هذا لمهارة
  - build me an assistant
  - create a new assistant
  - turn this into a skill
  negative_triggers:
  - match: عدّلي المساعد الموجود
    route_to: system-assistant-tuner
  - match: وش المساعدين عندي
    route_to: system-assistant-directory
  - match: احفظي هذا للمساعد
    route_to: system-knowledge-manager
  required_inputs:
  - المهمة الواحدة
  - عبارات التشغيل
  - شكل المخرَج
  - المستخدم النهائي
  optional_inputs:
  - ملفات معرفة
  - موصّلات مطلوبة
  outputs:
  - بطاقة تصميم
  - SKILL.md مكتمل المخطط
  - نتيجة الفحص
  - ملف .skill
  - قيد في الدليل
  knowledge_dependencies:
  - knowledge/assistants-registry.md
  policy_dependencies:
  - house-rules
  - clinical-firewall
  skill_dependencies: []
  tool_dependencies:
  - bash
  - write
  can_delegate_to:
  - system-knowledge-manager
  cannot_delegate_to: []
  handoff_contract:
    accepts_from: []
    delegates_to:
    - system-knowledge-manager
    required_inputs:
    - المهمة الواحدة
    - عبارات التشغيل
    - شكل المخرَج
    - المستخدم النهائي
    guaranteed_outputs:
    - بطاقة تصميم
    - SKILL.md مكتمل المخطط
    - نتيجة الفحص
    - ملف .skill
    - قيد في الدليل
  routing_priority: 75
  safety_level: MODERATE
  status: ACTIVE
  version: 1.2.2
  last_tested_version: 1.2.2
  owner: clinic-owner
  created_at: '2026-08-21'
  last_updated: '2026-08-28'
  last_tested: '2026-08-28'
  evaluation_suite: governance/routing-tests.yaml
  legacy_aliases:
  - new-assistant
  deprecated_by: null
  notes: خطوات التسليم (المرحلة ٥) صُحّحت لتعتمد Read/Write/SendUserFile بدل project_read/project_write
    غير الموجودة في Cowork — 2026-08-28
---













# صانع المساعدين

بناء مساعد مخصص جديد: مقابلة قصيرة → تعليمات مكتوبة → معرفة وأدوات مربوطة → اختبار → ملف `.skill` جاهز للتثبيت والمشاركة مع الفريق.

## قبل أي شيء

1. اقرأ ملف الهوية: `${CLAUDE_PLUGIN_ROOT}/identity/house-rules.md`. كل مساعد يرث منه أقسام `[يُنسخ]`.
2. إذا بقيت حقول جوهرية غير ممتلئة في ملف الهوية (اسم العيادة، الخدمات)، نبّه المستخدمة مرة واحدة بسطر واحد واستمر — لا توقف العمل.
3. راجع دليل المساعدين الحالي (`references/registry-template.md` في مهارة `system-assistant-directory`) لتفادي بناء مساعد مكرر. إن وُجد مساعد قريب جداً، اعرض التعديل عليه بدل بناء واحد جديد.

## المرحلة ١ — المقابلة

استخدم `AskUserQuestion` بالعربية. **لا تسأل عمّا أجابت عنه بالفعل.** أقصى جولتين.

الجولة الأولى (أربعة أسئلة كحد أقصى):

| السؤال | لماذا |
|---|---|
| ما المهمة الواحدة التي يتقنها هذا المساعد؟ | مساعد بمهمة واحدة أفضل من مساعد بخمس |
| متى تحتاجينه؟ اذكري ٣ جمل تقولينها له فعلاً | هذه تصبح عبارات التشغيل (triggers) |
| ما شكل المخرَج؟ (رد في المحادثة · ملف Word/Excel/عرض · مسوّدة رسالة · تقرير) | يحدد الأدوات |
| من يستخدمه؟ (أنتِ فقط · فريق العيادة · الاثنان) | يحدد مستوى التفصيل والصلاحيات |

الجولة الثانية — فقط إن بقي غموض:

- هل يحتاج معرفة ثابتة (أسعار، بروتوكولات، نماذج، أسئلة متكررة)؟ وهل الملفات جاهزة؟
- هل يحتاج أدوات خارجية؟ (بريد، درايف، كانفا، إعلانات، محادثات)
- ما الذي **يجب ألا** يفعله؟
- هل يتعامل مع بيانات مرضى أو صور حالات؟ (إن نعم → قسم الخصوصية إلزامي وموسّع)

إن قالت «سوّي اللي تشوفينه مناسب» — اقترحي تصميماً محدداً واطلبي تأكيداً واحداً، لا تتركي الأمر مفتوحاً.

## المرحلة ٢ — بطاقة التصميم

قبل الكتابة، اعرضي بطاقة قصيرة واحصلي على «تمام»:

```
الاسم:            ⟨kebab-case بالإنجليزية⟩ · ⟨الاسم العربي المعروض⟩
المهمة:           سطر واحد
يشتغل عند:        ٣–٥ عبارات تشغيل
المخرجات:         ...
الأدوات:          ...
المعرفة:          ...
لا يفعل:          ...
```

## المرحلة ٣ — الكتابة

انسخ `${CLAUDE_PLUGIN_ROOT}/skills/system-assistant-builder/assets/TEMPLATE-SKILL.md` واملأه.
اتبع قواعد الصياغة في `references/authoring-rules.md` — **اقرأها قبل الكتابة، لا بعدها.**

**املأ كتلة `metadata` كاملة وفق `governance/assistant-schema.md`.** المخطط ليس زينة: الفاحص يرفض أي حقل مطلوب ناقص، وأي معرّف لا يطابق `<domain>-<function>-<role>`، وأي `negative_triggers` فارغة.

القواعد الحاسمة:

- **`description` في الـ frontmatter هي ما يحدد هل يشتغل المساعد أصلاً.** اكتبها بصيغة الغائب، وضمّنها عبارات التشغيل العربية **والإنجليزية** حرفياً بين علامتي تنصيص.
- **الجسم تعليمات للنموذج لا شرح للمستخدمة.** صيغة الأمر: «اقرأ»، «اسأل»، «تحقق» — لا «يجب على المساعد أن…».
- أقل من ١٥٠٠ كلمة في `SKILL.md`. التفاصيل الطويلة إلى `references/`.
- انسخ أقسام `[يُنسخ]` من ملف الهوية داخل المساعد نفسه (مختصرة إن لزم) — لا تكتفِ بالإشارة إليها.
- عرّف **ما لا يفعله** بوضوح، وضع قاعدة المسوّدة الافتراضية إن كان يرسل أو ينشر.

بنية المجلد:

```
<assistant-name>/
├── SKILL.md
├── references/      ← اختياري: بروتوكولات، أمثلة، جداول طويلة
└── knowledge/       ← اختياري: معرفة ثابتة صغيرة تُشحن مع المساعد
```

المعرفة الكبيرة أو المتغيرة لا تُشحن داخل المساعد — تُحفظ عبر مهارة `system-knowledge-manager` في `${CLAUDE_PLUGIN_ROOT}/knowledge/` (لا "Project" — تلك بيئة Claude.ai غير موجودة هنا)، ويُذكر مسارها في تعليمات المساعد.

## المرحلة ٤ — الاختبار قبل التسليم

إلزامي. لا تُسلَّم مهارة لم تُختبر.

1. **اختبار التشغيل:** خذ عبارات التشغيل الثلاث وواحدة قريبة-لكن-ليست-المقصودة. تحقق أن الوصف يميز بينها. إن لم يميز، عدّل الوصف.
2. **تشغيلة حقيقية:** نفّذ المساعد فعلياً على مثال واحد من عمل الطبيب/ة وأنتج المخرَج كاملاً. اعرضي المخرَج عليه/ها.
3. **فحص الحدود:** اطرح على نفسك حالة يجب أن يرفضها المساعد (طلب تشخيص، نشر صورة بلا موافقة، إرسال بلا إذن) وتأكد أن التعليمات تغطيها.
4. **فحص بنيوي سريع:** `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/validate_assistant.py <مسار المجلد>`
5. **فحص الحوكمة — البوابة المعتمدة:**
   `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/validate_system.py --skills ${CLAUDE_PLUGIN_ROOT}/skills --policy ${CLAUDE_PLUGIN_ROOT}/identity/house-rules.md`
6. **اختبارات التوجيه:** أضف حالات المساعد الجديد إلى `governance/routing-tests.yaml` — إصابة لكل عبارة تشغيل، وإقصاء لكل `negative_trigger` — ثم:
   `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/routing_tests.py --skills ${CLAUDE_PLUGIN_ROOT}/skills --tests ${CLAUDE_PLUGIN_ROOT}/governance/routing-tests.yaml`

أصلح ما يظهر، ثم أعد الفحص. **لا تُسلَّم مهارة والفحص فيه خطأ واحد.**

## المرحلة ٥ — التسليم والتسجيل

1. **الاعتماد:** المساعد يُولَّد بـ `status: DRAFT` و `last_tested_version: null`. بعد نجاح الفحوص والتشغيلة الحقيقية، اختم:
   `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/stamp_tested.py --skills ... --routing-json ... --date <اليوم> --only <المعرّف>`
   ثم ارفع الحالة إلى `ACTIVE`. **مساعد بإصدار غير مختوم لا يدخل التوجيه** — انظر `governance/lifecycle-versioning.md`.
2. **أعد توليد الدليل** (لا تحرّره يدوياً):
   `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/build_registry.py --skills ${CLAUDE_PLUGIN_ROOT}/skills --out ${CLAUDE_PLUGIN_ROOT}/knowledge/assistants-registry.md --deferred ${CLAUDE_PLUGIN_ROOT}/governance/migration-spec.yaml`
   لا توجد أداة `project_write` هنا — هذا الأمر يحدّث نسخة الجلسة الحالية فقط. سلّمي الدليل المحدَّث عبر `SendUserFile` مع ملف `.skill` الجديد (الخطوة ٣-٤ أدناه)، لا كخطوة منفصلة صامتة.
3. غلّف: `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/package_assistant.py <مسار المجلد>` — ينتج `<name>.skill`.
4. سلّم عبر `SendUserFile` **ملفين معاً**: `<name>.skill` الجديد، ودليل المساعدين المحدَّث من الخطوة ٢. قولي بوضوح: **«الملف الأول بطاقة المساعد الجديد — اضغطي عليها لحفظها في حسابك. الملف الثاني دليل محدَّث — أعيدي رفعه ليحل محل نسخة الدليل القديمة في الإضافة.»** لا تدّعِ أن أياً منهما حُفظ أو حل محل القديم قبل أن تفعل هي ذلك فعلياً.
5. اعرضي في سطرين: ماذا يفعل، وكيف تشغّله (أول عبارة تشغيل).

## أخطاء متكررة — تجنّبها

| الخطأ | الصواب |
|---|---|
| وصف عام: «يساعد في التسويق» | «يشتغل عند: خطة محتوى شهر، أفكار ريلز، مراجعة أداء منشور» |
| مساعد يفعل خمسة أشياء | خمسة مساعدين، أو واحد بمهمة واحدة وإحالات |
| نسخ ملف الهوية كاملاً في كل مساعد | نسخ الأقسام المعلَّمة `[يُنسخ]` فقط، مختصرة |
| تسليم بدون تشغيل تجريبي | تشغيلة حقيقية على مثال من عملها |
| مساعد يرسل بدون إذن | مسوّدة افتراضياً، الإرسال بموافقة صريحة |

## ملفات المرجع

- `references/authoring-rules.md` — قواعد كتابة الوصف والجسم بالتفصيل، مع أمثلة صح/خطأ
- `references/connectors.md` — الأدوات المتاحة وكيف يُشار إليها داخل تعليمات المساعد
- `assets/TEMPLATE-SKILL.md` — القالب الجاهز
- `scripts/validate_assistant.py` · `scripts/package_assistant.py`
