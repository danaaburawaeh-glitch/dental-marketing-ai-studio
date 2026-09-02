---
document: standalone-guarantee
type: GOVERNANCE
version: 1.0.0
status: ACTIVE
applies_to: ALL_ASSISTANTS
---

# ضمان الاستقلالية — Standalone Guarantee v1.0.0

هذا المستند يثبّت التزاماً معمارياً صريحاً وُلد مع v1.3.0 (Standalone Edition): **Assistant Studio يجب أن يبقى قابلاً للعمل بالكامل لدى أي مستخدم آخر، دون أي اعتماد على مساعدين أو Skills أو ملفات معرفة خاصة بحساب مُنشئه الأصلي، أو مسارات محلية، أو تكاملات اختيارية.** أي تعارض بين هذا المستند وأي وثيقة أخرى (باستثناء `identity/house-rules.md` و `identity/clinical-firewall.md`) يُحسم لصالح هذا المستند فيما يخص قابلية التثبيت والتشغيل المستقل.

## البيان الأساسي

> Assistant Studio must remain fully functional without account-specific assistants, private skills, private knowledge files, local paths, or optional integrations.
>
> Missing optional integrations must never cause core workflow failure.

كل Skill داخل هذه الحزمة — بلا استثناء — يجب أن تنفّذ وظيفتها الأساسية كاملة لمستخدم فتح الحزمة للتو، بلا أي حساب مربوط، بلا أي MCP، بلا أي Skill أو Assistant آخر خارج ما يأتي داخل هذا الـ ZIP نفسه.

## ما يضمنه هذا الملف تحديداً

1. **صفر اعتماديات Required خارج الحزمة.** أي قدرة كانت تُحال سابقاً إلى Skill أو Assistant خارجي (انظر `DEPENDENCIES.md`) إما بُنيت داخلياً، أو دُمجت في Skill قائمة، أو أُزيلت لأنها غير عامة الوظيفة. لا استثناء.
2. **كل تكامل خارجي Optional بالتصميم.** WhatsApp/ChatPlace، Meta Ads، Windsor.ai، Canva، Google Workspace — جميعها Progressive Enhancement (انظر `governance/capability-detection.md`). لا Skill تفترض وجود أي منها قبل التحقق الفعلي.
3. **لا فشل عند غياب تكامل اختياري.** كل Skill تعتمد على تكامل اختياري تنفّذ Manual Execution Mode كاملة عند غيابه — تحليل، توصية، مخرَج جاهز للنسخ، قائمة تحقق، وخطوة تالية. غياب الأداة يُنقص الأتمتة لا القدرة.
4. **لا مسار محلي، لا معرّف حساب، لا رابط خاص.** انظر `governance/portability.md` للقواعد التفصيلية.

## من يتحمّل هذا الضمان

| المكوّن | مسؤوليته تحت هذا الضمان |
|---|---|
| كل `skills/*/SKILL.md` | `tool_dependencies` تُعامَل كاختيارية دائماً؛ لا `required_inputs` يفترض وجود تكامل خارجي؛ قسم "مصادر البيانات" أو ما يعادله يتضمن مساراً يدوياً صريحاً |
| `system-assistant-builder` | يرفض حفظ أي Skill جديدة تجعل تكاملاً خارجياً (غير `house-rules`/`clinical-firewall`) شرطاً إلزامياً للعمل؛ يطلب توضيح مسار Manual Execution Mode قبل الاعتماد |
| `governance/release-policy.md` | بوابة الإصدار تتضمن الآن التحقق من `tests/dependency-scan.py` (صفر اعتماديات Required غير محلولة) و `tests/standalone/` (Manual Execution Mode يعمل فعلياً) قبل أي اعتماد |
| مستخدم جديد | لا يحتاج فعل أي شيء إضافي — تثبيت الـ ZIP وحده كافٍ لتشغيل كل قدرة أساسية |

## الاختبار العملي لهذا الضمان

`tests/standalone/` (انظر الملف) يحاكي مستخدماً جديداً بلا أي مساعد أو Skill أو ملف معرفة أو API خاص بالحساب الأصلي، ويؤكد أن الأوامر الأساسية (إدارة، تسويق، محتوى، واتساب) تعمل، وأن الطلب السريري يُحجب بجدار الحماية السريري — لا أكثر ولا أقل.

## العلاقة بالوثائق الأخرى

```
governance/portability.md          ← القواعد التفصيلية لعدم وجود مسار/معرّف/رابط خاص
governance/capability-detection.md ← آلية اكتشاف التكامل الاختياري والتراجع اليدوي
DEPENDENCIES.md                    ← الجرد الكامل والنتيجة النهائية: صفر اعتماديات Required
tests/standalone/                  ← الإثبات التنفيذي لهذا الضمان
tests/dependency-scan.py           ← الماسح الآلي الذي يفشل البناء عند أي مرجع غير محلول
```

## سجل التحديث

| التاريخ | ما تغيّر |
|---|---|
| 2026-08-28 | إنشاء الملف — v1.3.0 Standalone Edition، بعد إغلاق كل اعتماديات Required المكتشفة في DEPENDENCIES.md |
