---
name: system-knowledge-manager
description: >
  قاعدة معرفة المساعدين — يحوّل ملفات الطبيب/ة (PDF، Word، Excel، صفحات ويب، ملاحظات) إلى معرفة دائمة داخل ملفات
  الإضافة يقرأها أي مساعد، ويحافظ على فهرسها (مكافئ رفع Knowledge في Custom GPT). This skill should be used when
  the user says "احفظي هذا للمساعد", "ضيفي هذا لقاعدة المعرفة", "خليه يعرف هذا", "حدّثي الأسعار", "هذي
  بروتوكولاتنا", "ارفعي هذا الملف للمساعد", or in English "add this to the knowledge base", "make the assistant
  remember this", "update the assistant's knowledge", "upload this file to my assistant". Also use when an
  assistant repeatedly asks for the same information.
metadata:
  assistant_id: system-knowledge-manager
  display_name: قاعدة معرفة المساعدين
  domain: system
  role: knowledge-manager
  purpose: تحويل الملفات إلى معرفة دائمة منظّمة داخل ملفات الإضافة وربطها بالمساعدين وصيانة فهرسها
  triggers:
  - احفظي هذا للمساعد
  - ضيفي هذا لقاعدة المعرفة
  - خليه يعرف هذا
  - حدّثي الأسعار
  - add this to the knowledge base
  - make the assistant remember this
  negative_triggers:
  - match: ابني لي مساعد
    route_to: system-assistant-builder
  - match: وش المساعدين عندي
    route_to: system-assistant-directory
  required_inputs:
  - المحتوى أو الملف
  - المساعد المستفيد
  optional_inputs:
  - موعد المراجعة
  outputs:
  - ملف معرفة بترويسة موحّدة
  - قيد في الفهرس
  - ربط في تعليمات المساعد
  knowledge_dependencies:
  - knowledge/generated-index.md
  policy_dependencies:
  - house-rules
  - clinical-firewall
  skill_dependencies: []
  tool_dependencies:
  - plugin-files
  - pdf
  - docx
  - xlsx
  can_delegate_to: []
  cannot_delegate_to: []
  routing_priority: 75
  safety_level: HIGH
  status: ACTIVE
  version: 1.1.1
  last_tested_version: 1.1.1
  owner: clinic-owner
  created_at: '2026-08-21'
  last_updated: '2026-08-28'
  last_tested: '2026-08-28'
  evaluation_suite: governance/routing-tests.yaml
  legacy_aliases:
  - assistant-knowledge
  deprecated_by: null
  notes: خطوتا «احفظ» و«حدّث الفهرس» صُححتا لاعتماد Write/build_knowledge_index.py/SendUserFile بدل project_write
    وknowledge/INDEX.md غير الموجودين في Cowork — 2026-08-28
---












# قاعدة معرفة المساعدين

المعرفة الدائمة تعيش في ملفات الإضافة نفسها (`${CLAUDE_PLUGIN_ROOT}/knowledge/`) — لا في المحادثة ولا في ذاكرة النموذج، ولا في أداة "Project" منفصلة (تلك خاصة ببيئة Claude.ai ولا وجود لها في Cowork). ما يُحفظ هنا يقرأه أي مساعد في أي جلسة قادمة، **بشرط أن يُعاد رفع الملف المحدَّث إلى الإضافة المثبَّتة** — لا آلية هنا تفعل ذلك تلقائياً (التفصيل في خطوة ٤ أدناه).

## متى تُحفظ المعرفة أصلاً

احفظ إن تحققت **كل** الشروط:

- تُستخدم أكثر من مرة
- لا يمكن استنتاجها أو البحث عنها لحظياً
- مستقرة نسبياً (لا تتغير كل يوم)

لا تُحفظ: مخرجات جاهزة، نتائج تحليل لمرة واحدة، أي شيء يمكن الحصول عليه ببحث ويب. تخزين ما لا يُقرأ يفسد الفهرس ويبطئ كل مساعد.

## البنية

```
knowledge/generated-index.md            ← الفهرس — مولَّد آلياً، لا يُحرَّر يدوياً
knowledge/assistants-registry.md        ← دليل المساعدين
knowledge/shared/<موضوع>.md             ← يشترك فيه أكثر من مساعد
knowledge/<marketing|management|research>/<موضوع>.md   ← خاص بمجال واحد (وفق governance/knowledge-schema.md)
```

المعرفة التي يحتاجها مساعدان → `shared/`. لا تنسخها مرتين؛ النسختان تتباعدان ثم تتناقضان.

## طريقة العمل

### ١. استخرج
- PDF → اقرأ عبر مهارة `pdf`
- Word / Excel / PowerPoint → عبر `docx` / `xlsx` / `pptx`
- صفحة ويب → `WebFetch`، مع حفظ الرابط وتاريخ الجلب
- كلام الطبيب/ة مباشرة → صُغه أنت وأعد عرضه للتأكيد

### ٢. صُغ — لا تلصق
الملف المرفوع كما هو معرفة سيئة. أعد الصياغة:

- عناوين واضحة، وجداول للحقائق المنظمة
- سطر واحد لكل حقيقة — لا فقرات سردية
- الأرقام مع تاريخها ومصدرها
- احذف الحشو والتنسيق والتكرار
- الملف الواحد تحت ٢٠٠٠ كلمة؛ ما زاد يُقسَّم بالموضوع

### ٣. صدّر بترويسة موحّدة

كل ملف معرفة يبدأ بـ:

```markdown
# ⟨العنوان⟩

| | |
|---|---|
| يستخدمه | ⟨المساعدون⟩ |
| المصدر | ⟨ملف / رابط / الطبيب/ة مباشرة⟩ |
| آخر تحديث | ⟨تاريخ⟩ |
| يحتاج مراجعة | ⟨كل ٣ شهور / عند تغير الأسعار / لا⟩ |
| حساسية | ⟨عام · داخلي · يحتوي بيانات مرضى⟩ |
```

### ٤. احفظ
لا توجد أداة `project_write` هنا — «الـ Project» خاصة ببيئة Claude.ai ولا وجود لها في Cowork. الملف الصحيح فعلياً هو داخل الإضافة نفسها، وفق البنية الموثَّقة في `governance/knowledge-schema.md`:

```
${CLAUDE_PLUGIN_ROOT}/knowledge/<shared|marketing|management|research>/<اسم-الملف>.md
```

اكتبيه بأداة `Write`/`Edit` على هذا المسار، متضمناً حقول الـ frontmatter الإلزامية (`knowledge_id`, `status`, `owner`, `source`, `sensitivity`, `patient_data_allowed`, إلخ — القالب الكامل في `governance/knowledge-schema.md`). هذا يحدّث **نسخة الجلسة الحالية فقط** — لا يصل تلقائياً لحساب المستخدمة.

### ٥. حدّث الفهرس وسلّمي التحديث
ولّدي الفهرس آلياً، لا يدوياً:
```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/build_knowledge_index.py --knowledge-root ${CLAUDE_PLUGIN_ROOT}/knowledge --out ${CLAUDE_PLUGIN_ROOT}/knowledge/generated-index.md
```
ثم سلّمي عبر `SendUserFile` ملف/ملفات المعرفة الجديدة/المعدَّلة مع `generated-index.md` معاً، وقولي بوضوح: **«هذه ملفات معرفة محدَّثة — أعيدي رفعها لتحل محل النسخ القديمة في الإضافة.»** لا تدّعي أن المعرفة "أصبحت متاحة لكل مساعد" قبل أن تُعاد هذه الملفات فعلياً إلى الإضافة المثبَّتة.

### ٦. اربط
افتح `SKILL.md` للمساعد المعني وتأكد أن فيه قسم «المعرفة» يذكر المسار و**متى** يُقرأ. معرفة محفوظة وغير مربوطة = معرفة غير موجودة.

## خصوصية المرضى — حدّ صارم (PDPL)

**لا يُحفظ في قاعدة المعرفة:** اسم مريض، رقم ملف، رقم جوال، صورة حالة، أو أي تفصيل يسمح بالتعرف على شخص.

المسموح: بروتوكولات، نماذج، أسئلة متكررة، حالات مجهولة الهوية تماماً ومرمَّزة (حالة ١، Case A) بعد إزالة كل ما يعرّف.

إن طلبت الطبيب/ة حفظ شيء يحتوي بيانات مريض — توقف، اشرح في سطر، واعرض حفظ النسخة المجهّلة بدلاً منها. هذا شرط PDPL ولا يُتجاوز بطلب.

## الصيانة

عند فتح الاستوديو أو عند طلب مراجعة:

- ملفات تجاوزت موعد مراجعتها → اعرضها للطبيب/ة
- ملفان يتناقضان → نبّه، واسأل أيّهما الصحيح، ثم وحّدهما
- ملف لا يذكره أي مساعد → مرشح للحذف، اسأل قبل الحذف
- أرقام بلا تاريخ → أضف التاريخ أو احذفها؛ الرقم مجهول التاريخ أخطر من غيابه

## مرجع

`references/knowledge-format.md` — قوالب جاهزة (أسعار، بروتوكول، أسئلة متكررة، ملف منافس) وقواعد التجهيل.
