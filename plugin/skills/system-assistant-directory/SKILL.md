---
name: system-assistant-directory
description: >
  دليل المساعدين — يعرض المساعدين المتاحين، ماذا يفعل كل واحد، ومتى يُستخدم، ويوجّه الطلب إلى المساعد الصحيح
  (مكافئ My GPTs). This skill should be used when the user says "وش المساعدين عندي", "اعرضي المساعدين", "مين
  يقدر يساعدني في", "افتحي الاستوديو", "وش الموظفين اللي عندي", "أي مساعد أستخدم", or in English "list my
  assistants", "what assistants do I have", "which assistant should I use", "open the studio", "show my skills".
  Also use when a request is ambiguous and two or more assistants could handle it, to pick one before starting
  work.
metadata:
  assistant_id: system-assistant-directory
  display_name: دليل المساعدين
  domain: system
  role: router
  purpose: عرض المساعدين المتاحين وتوجيه الطلب إلى الصحيح منهم وفق سياسة التوجيه
  triggers:
  - وش المساعدين عندي
  - اعرضي المساعدين
  - مين يساعدني في
  - افتحي الاستوديو
  - list my assistants
  - which assistant should I use
  negative_triggers:
  - match: ابني لي مساعد جديد
    route_to: system-assistant-builder
  - match: المساعد ما اشتغل
    route_to: system-assistant-tuner
  - match: هل يوجد تحديث
    route_to: system-update-checker
  required_inputs:
  - الدليل من knowledge/assistants-registry.md
  optional_inputs:
  - الطلب المراد توجيهه
  outputs:
  - جدول المساعدين حسب المجال
  - المساعد المختار وسبب اختياره
  knowledge_dependencies:
  - knowledge/assistants-registry.md
  policy_dependencies:
  - house-rules
  - clinical-firewall
  - routing-policy
  skill_dependencies: []
  tool_dependencies:
  - plugin-files
  can_delegate_to: []
  cannot_delegate_to: []
  routing_priority: 90
  safety_level: MODERATE
  status: ACTIVE
  version: 1.1.2
  last_tested_version: 1.1.2
  owner: clinic-owner
  created_at: '2026-08-21'
  last_updated: '2026-08-28'
  last_tested: '2026-08-28'
  evaluation_suite: governance/routing-tests.yaml
  legacy_aliases:
  - assistant-directory
  deprecated_by: null
  notes: قسما «المصدر» و«صيانة الدليل» صُححا لاعتماد Read/SendUserFile بدل project_read/project_write غير
    الموجودة في Cowork — 2026-08-28
---












# دليل المساعدين

نقطة الدخول للاستوديو: ماذا لدى الطبيب/ة من مساعدين، أيّهم يناسب الطلب الحالي، وما الفجوة التي تستدعي بناء مساعد جديد.

## المصدر

الدليل ملف مرفق مع الإضافة نفسها، لا في أداة "Project" منفصلة (تلك خاصة ببيئة Claude.ai ولا وجود لها هنا):

```
${CLAUDE_PLUGIN_ROOT}/knowledge/assistants-registry.md
```

اقرأه بأداة `Read` على هذا المسار الكامل مباشرة. إن تعذّر — بيئة لا تُعرِّف `CLAUDE_PLUGIN_ROOT` أصلاً — فالبديل الوحيد هو `ListSkills`، وهو يعيد **كل** مهارات حساب المستخدمة لا مهارات هذا الاستوديو وحده: صفِّ النتائج بالبحث عن الاسم بادئاً بـ `assistant-studio:` أو بمطابقة المعرّفات المذكورة في هذا الملف قبل عرضها، ولا تعرض مهارة من مصدر آخر على أنها جزء من الاستوديو. لا تخترعي مساراً آخر ولا تفترضي وجود أداة `project_read`.

إن لم يوجد الملف أصلاً على المسار أعلاه، أنشئه من القالب في `references/registry-template.md` ثم املأه بمهارات الاستوديو المكتشَفة عبر `ListSkills` بعد التصفية.

**لا تخترع مساعداً غير موجود في الدليل.** إن لم يوجد ما يناسب، قل ذلك واعرض بناء واحد.

## الوضع الأول — «وش عندي؟»

اعرض جدولاً مختصراً، مجمّعاً حسب المجال، بحد أقصى عمودين نصيين:

```
### نمو انستغرام
| المساعد | يشتغل عند |
|---|---|
| مدير النمو | «راجعي أرقام الحساب» |
| مهندس المحتوى | «رتبي محتوى الشهر» |

### العيادة والمرضى
...
```

لا تعرض أكثر من ١٢ صفاً في المرة الواحدة. إن زادوا، اعرض المجالات أولاً واسأل عن المجال المطلوب.

## الوضع الثاني — «مين يساعدني في كذا؟»

1. طابق الطلب مع عمود «يشتغل عند» في الدليل.
2. **مطابقة واحدة:** سمِّ المساعد، اذكر في سطر ماذا سيفعل، وابدأ العمل مباشرة — لا تنتظر إذناً إضافياً.
3. **مطابقتان أو أكثر:** اعرض الفرق بينهما في سطر لكل واحد، واسأل بـ `AskUserQuestion` سؤالاً واحداً.
4. **لا مطابقة:** قل ذلك صراحة. ثم إما نفّذ الطلب مباشرة بدون مساعد (إن كان طلباً عادياً)، أو اعرض بناء مساعد جديد إن كان الطلب متكرراً بطبيعته.

**معيار «هل يستحق مساعداً جديداً؟»** — إن كانت الطبيب/ة ستطلب هذا الشيء نفسه أكثر من ثلاث مرات، نعم. طلب لمرة واحدة لا يستحق مساعداً.

## الوضع الثالث — تشخيص التداخل

عند شكوى «المساعد الغلط يشتغل» أو «ما اشتغل المساعد»:

1. اقرأ أوصاف المساعدين المتنافسين.
2. حدد أيّها يفتقد سطر «لا يشتغل عند».
3. سلّم التشخيص إلى مهارة `system-assistant-tuner` لإصلاح الوصف.

لا تصلح الوصف من هنا — الإصلاح والاختبار مكانهما `system-assistant-tuner`.

## صيانة الدليل

بعد أي بناء أو تعديل مساعد، لا تحرّري `assistants-registry.md` يدوياً — أعيدي توليده آلياً:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/build_registry.py --skills ${CLAUDE_PLUGIN_ROOT}/skills \
       --out ${CLAUDE_PLUGIN_ROOT}/knowledge/assistants-registry.md \
       --deferred ${CLAUDE_PLUGIN_ROOT}/governance/migration-spec.yaml
```

**قيد بيئي مهم:** هذا الأمر يكتب الملف داخل نسخة الجلسة الحالية فقط. لا توجد أداة `project_write` هنا، ولا آلية تُعيد التعديل تلقائياً إلى حساب المستخدمة أو الإضافة المثبَّتة — كل تعديل يبقى محلياً حتى يُسلَّم صراحة. لذلك بعد التوليد: سلّمي الملف المحدَّث عبر `SendUserFile` وقولي بوضوح: «هذا دليل المساعدين المحدَّث — أعيدي رفعه ليحل محل النسخة القديمة في الإضافة»، بنفس الأسلوب الذي تسلَّم به `system-assistant-builder` ملف `.skill` الجديد. لا تدّعي أن الدليل "تحدَّث في حسابها" قبل أن تفعل هي هذه الخطوة فعلياً.

راجع الدليل مقابل `ListSkills` (مُصفّاة بمهارات الاستوديو فقط) مرة كل فترة؛ إن ظهر تعارض، الحساب هو المصدر الصحيح والدليل يُحدَّث ليطابقه بنفس آلية التسليم أعلاه.

## الحدود

- الدليل **يوجّه ولا ينفّذ محتوى طبياً بنفسه**. أي طلب سريري يُحال إلى المساعد المختص، وإن لم يوجد، لا تُرتجل إجابة طبية.
- مساعدو الاستوديو أدوات صياغة وتحليل. المخرَج الطبي أو الموجّه للمرضى **يُعتمد من الطبيب/ة قبل النشر أو الإرسال** — بلا استثناء.
- لا يُذكر اسم مريض ولا أي تفصيل تعريفي في الدليل أو في أي مخرَج منه (خصوصية المرضى · PDPL).

## مرجع

`references/registry-template.md` — قالب الدليل وحقوله.
