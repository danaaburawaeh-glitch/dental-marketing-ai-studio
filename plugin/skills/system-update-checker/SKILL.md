---
name: system-update-checker
description: >
  فاحص تحديثات Dental Marketing AI Studio — يتحقق من أحدث إصدار منشور على GitHub ويقارنه بالإصدار المثبت، ثم يعرض ما إذا كان المستخدم على أحدث نسخة ورابط التنزيل عند توفر تحديث. استخدمه عند قول المستخدم "هل يوجد تحديث؟"، "حدث المساعد"، "ما آخر إصدار؟"، "check for updates", "is there an update", "latest version", أو "update assistant". لا يثبت أو يستبدل ملفات تلقائياً؛ التحديث يحتاج قرار المستخدم وتنزيلاً صريحاً.
metadata:
  assistant_id: system-update-checker
  display_name: فاحص التحديثات
  domain: system
  role: utility
  purpose: مقارنة الإصدار المثبت بأحدث GitHub Release وإعطاء حالة التحديث ورابط التنزيل
  triggers:
  - هل يوجد تحديث
  - تحقق من التحديثات
  - حدث المساعد
  - ما آخر إصدار
  - check for updates
  - is there an update
  - latest version
  - update assistant
  negative_triggers:
  - match: المساعد ما اشتغل
    route_to: system-assistant-tuner
  required_inputs: []
  optional_inputs:
  - إصدار مثبت يذكره المستخدم صراحة
  outputs:
  - الإصدار المثبت
  - أحدث إصدار منشور
  - حالة التحديث
  - رابط تنزيل أحدث نسخة عند الحاجة
  knowledge_dependencies: []
  policy_dependencies:
  - house-rules
  - clinical-firewall
  - routing-policy
  skill_dependencies: []
  tool_dependencies:
  - bash
  - webfetch
  can_delegate_to: []
  cannot_delegate_to: []
  routing_priority: 92
  safety_level: LOW
  status: ACTIVE
  version: 1.0.0
  last_tested_version: 1.0.0
  owner: clinic-owner
  created_at: '2026-09-02'
  last_updated: '2026-09-02'
  last_tested: '2026-09-02'
  evaluation_suite: governance/routing-tests.yaml
  legacy_aliases: []
  deprecated_by: null
  notes: أول إصدار؛ يعتمد GitHub Releases العام كمصدر حقيقة للإصدار الأحدث، مع fallback واضح عند غياب الإنترنت.
---

# فاحص تحديثات Dental Marketing AI Studio

يفحص ما إذا كانت النسخة المثبتة هي أحدث نسخة مستقرة من **Dental Marketing AI Studio**.

## مصدر الحقيقة

- الإصدار المثبت: اقرأ `version` من `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json`.
- الإصدار الأحدث: GitHub Latest Release API:
  `https://api.github.com/repos/danaaburawaeh-glitch/dental-marketing-ai-studio/releases/latest`
- رابط التنزيل الثابت:
  `https://github.com/danaaburawaeh-glitch/dental-marketing-ai-studio/releases/latest/download/Dental-Marketing-AI-Studio-Latest.zip`
- صفحة أحدث إصدار:
  `https://github.com/danaaburawaeh-glitch/dental-marketing-ai-studio/releases/latest`

## طريقة التنفيذ المفضلة

إذا كانت أداة Bash متاحة، شغّل:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/check_update.py"
```

السكريبت يعيد JSON منظمًا ولا يعدّل أي ملف.

إذا لم تتوفر Bash، استخدم WebFetch على GitHub Latest Release API، واقرأ `tag_name`، ثم قارنه بإصدار `plugin.json` وفق Semantic Versioning.

## قواعد المقارنة

1. تجاهل الحرف `v` في بداية tag عند المقارنة.
2. قارن `major.minor.patch` كأرقام، لا كسلاسل نصية.
3. إذا `latest > installed` → تحديث متاح.
4. إذا متساويان → النسخة محدثة.
5. إذا `installed > latest` → النسخة المثبتة أحدث من القناة العامة؛ اذكر ذلك ولا تقترح downgrade تلقائيًا.

## شكل الرد

### عند وجود تحديث

```text
يوجد تحديث جديد لـ Dental Marketing AI Studio.
الإصدار لديك: vX.Y.Z
أحدث إصدار: vA.B.C

أبرز التغييرات: <ملخص موجز من Release notes إن توفر>
تنزيل أحدث نسخة: <رابط التنزيل الثابت>
```

### إذا كانت النسخة محدثة

```text
Dental Marketing AI Studio محدث.
الإصدار المثبت: vX.Y.Z
أحدث إصدار منشور: vX.Y.Z
```

### إذا تعذر الاتصال

قل صراحة إن **الفحص الحي تعذر**. لا تقل إن النسخة محدثة. أعطِ صفحة أحدث إصدار للمستخدم للتحقق يدويًا.

## حدود الأمان والتحديث

- لا تنزّل التحديث ولا تفك ضغطه ولا تستبدل ملفات المستخدم تلقائيًا.
- لا تحذف النسخة الحالية.
- لا تعدّل ملفات معرفة أو إعدادات المستخدم كجزء من "الفحص".
- عند طلب المستخدم تنفيذ التحديث، اعرض أولًا الإصدار الحالي والجديد وما سيتغير، ثم استخدم آلية التثبيت المتاحة في البيئة فقط بعد طلب صريح.
- لا ترسل بيانات حساب أو ملفات محلية إلى GitHub؛ طلب الفحص هو GET عام فقط.
