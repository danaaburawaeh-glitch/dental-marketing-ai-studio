# CHANGELOG

## v1.4.1 — 2026-09-02 — Built-in Update Checker

- Added `system-update-checker` as the 29th Skill.
- Added `scripts/check_update.py` for read-only Semantic Version comparison against GitHub Latest Release.
- Added a permanent latest-download URL and offline fallback behavior.
- Update checks never install, delete, or replace files automatically.
- Added routing regression cases for Arabic and English update requests.

## 1.4.0 — Marketing OS — 2026-09-02

### Added
- `marketing-offer-architect` — تصميم العرض التسويقي والباقة واختبارات القيمة.
- `marketing-paid-media-planner` — Media plan متعدد المنصات واختبارات الجمهور/الرسالة/الكرياتيف.
- `marketing-lead-funnel-optimizer` — تشخيص مسار Lead → Qualified → Booking وتحديد التسرب.
- `sales-lead-followup-manager` — تأهيل وتسلسل متابعة متعدد اللمسات مع قواعد توقف.
- `marketing-campaign-director` — تشغيل حملة متكاملة من brief إلى post-campaign review.
- `marketing-roi-analyst` — CPL/CPQL/Cost per Booking/CAC/ROAS وحدود الإسناد.
- `marketing-local-seo-geo-strategist` — Local SEO + GEO + Google Business/Profile/Entity signals.

### Changed
- توسيع `marketing-strategy-planner` ليوجّه النوايا المتخصصة إلى Skills الجديدة بدل محاولة تغطيتها بخطة عامة.
- رفع الحزمة إلى 28 Skill مع الحفاظ على Standalone وClinical Firewall.
- إضافة حالات routing جديدة للقدرات التسويقية الجديدة.


كل تغيير جوهري في Assistant Studio، من الأحدث إلى الأقدم. الشكل يتبع
[Keep a Changelog](https://keepachangelog.com/) والإصدارات [SemVer](https://semver.org/)
(`governance/lifecycle-versioning.md`).

## 1.3.0 — Standalone Edition — 2026-08-28

الترقية الكبرى: تحويل الحزمة إلى نسخة مستقلة بالكامل، قابلة للتثبيت والتشغيل
لدى أي مستخدم آخر بصفر اعتماد على مساعدين أو Skills أو ملفات معرفة خاصة
بحساب مُنشئ الحزمة الأصلي — دون حذف أي قدرة قائمة ودون بناء Skills وهمية
للتعويض.

### Added

- 4 مهارات داخلية جديدة تستوعب القدرة الفعلية لست إحالات كانت تشير خارج
  الحزمة: `content-whatsapp-lead-responder`، `marketing-strategy-planner`
  (يستوعب أيضاً لينكدإن كقناة واحدة)، `content-social-calendar-scheduler`،
  `content-short-form-video-planner`.
- قدرة توحيد صور الحالة دُمجت داخل `content-case-post-reviewer` الموجودة
  بدل مهارة خامسة منفصلة (تفادي التضخم).
- `governance/standalone-guarantee.md` — الالتزام المعماري بصفر اعتماديات.
- `governance/portability.md` — سبع قواعد قابلية نقل صريحة + جدول استثناءات
  موثَّقة.
- `governance/capability-detection.md` — تصنيف رسمي لنمط Progressive
  Enhancement / Manual Execution Mode، مبني على نمط "مصادر البيانات"
  الموجود أصلاً في مهارات `instagram/*`.
- `governance/routing-matrix.md` — مصفوفة Intent → Primary Skill → Secondary
  → Escalation → Out-of-scope كاملة للـ21 مهارة.
- `governance/proposals/2026-08-28-standalone-external-reference-removal.md`
  — اقتراح تغيير معماري (ACP) يوثّق تحديث 3 حالات في خط الأساس المجمَّد
  `governance/evals/regression-baseline.yaml`.
- بوابة إصدار عاشرة ("Standalone validation") في `governance/release-policy.md`.
- `tests/standalone/test_standalone.py` — 6 اختبارات استقلالية مسمّاة.
- `tests/dependency-scan.py` — ماسح اعتماديات آلي يفحص كل ملف في الحزمة
  (لا `skills/` فقط) عن مسارات مطلقة، أسرار، أسماء شخصية، روابط خاصة،
  ومراجع داخلية غير محلولة.
- `DEPENDENCIES.md`، `SKILLS-INVENTORY.md`، `INSTALL.md`، `config.example`،
  `RELEASE-AUDIT-v1.3.0.md`.

### Changed

- الإصدار 1.2.1 → 1.3.0 في `.claude-plugin/plugin.json` وكل ملف حوكمة يذكره.
- `plugin.json`: `author.name` من اسم شخصي إلى `"Assistant Studio"`.
- `owner: dana` → `owner: clinic-owner` في كل ملف حوكمة وقالب (5 ملفات)
  + قيمة افتراضية مطابقة في `scripts/migrate.py`.
- 5 مهارات موجودة (`content-case-post-reviewer`، `instagram-conversion-analyst`،
  `instagram-personal-brand-strategist`، `instagram-reel-strategist`،
  `instagram-content-architect`) — `negative_triggers.route_to` أُعيد توجيهه
  من معرّفات خارجية إلى المهارات الداخلية الجديدة؛ رُقّيت جميعها MINOR.
- `governance/routing-tests.yaml`: 1.0.0 → 1.1.0 — 3 حالات مصححة + 9 حالات
  جديدة (37 حالة إجمالاً، كانت 29).
- `governance/evals/regression-baseline.yaml`: 1.0 → 1.1 — 3 حالات محدَّثة عبر
  ACP موثَّق (لا تعديل صامت لملف مجمَّد).
- `governance/release-policy.md`: 1.0.0 → 1.1.0 — إضافة البوابة العاشرة.
- `README.md`: بايلاين شخصي مُزال، إعادة هيكلة كاملة (ماذا تفعل/لا تفعل،
  المهارات، الحوكمة، التوجيه، معمارية الاستقلالية، التكاملات الاختيارية،
  التثبيت، الاختبار)، سجل التحديثات السابق محفوظ كاملاً كملحق تاريخي.
- `knowledge/assistants-registry.md` — أُعيد توليده (21 مساعداً، 20 ACTIVE).

### Removed

- `roadmap/clinical-core-plan.md` (والمجلد `roadmap/` بالكامل) — صفر
  اعتمادية تشغيلية من أي مساعد أو سكربت، كان يشير لنظام سريري خاص منفصل
  تابع لحساب المُنشئ الأصلي.

### Fixed

- `SYSTEM_HARDENING_REPORT.md`، `SYSTEM_HARDENING_AUDIT.md` — عُمِّمت إشارات
  نظام سريري خاص خارج نطاق هذه الحزمة.
- `scripts/build_migration_map.py` — عبارة "قرار دانا" الحرفية في نصوص
  التقارير المولَّدة استُبدلت بـ"قرار مالك العيادة".
- `governance/migration-spec.yaml` — قسم `deferred:` أُعيد كتابته ليعكس حل
  6 اعتماديات داخلياً (`RESOLVED_INTERNAL_V1.3.0`) بدل حالتها المؤجَّلة سابقاً.

### Security

فحص مخصص عن أسرار/مفاتيح API/رموز/بيانات اعتماد مضمَّنة عبر كامل الحزمة —
صفر نتيجة (`tests/dependency-scan.py` § الأسرار). لا `config.example`/`.env`
مطلوب لأي قدرة أساسية — كل تكامل اختياري يُدار عبر موصّلات منصة Cowork، لا
مفاتيح API مضمَّنة في الكود.

### Known non-regressions (documented, not hidden)

- `governance/evals/regression-baseline.yaml`: 26/29 — 3 فشل سابق لهذه
  الترقية بالكامل (حالتان توقعان `EXTERNAL:dana-instagram-growth-director`
  من قبل إصلاح v1.2.0، وحالة توقيت ترقية `content-case-post-reviewer` كانت
  موروثة من مصدر v1.2.1 نفسه). لا علاقة لها بإزالة الاعتماديات الخارجية
  التي يستهدفها هذا الإصدار.
- لا مهارة مخصصة لنطاق "SOP إدارية/استقبال" — فجوة موجودة أصلاً منذ v1.2.1،
  خارج نطاق مهمة إزالة الاعتماديات، لم تُغلَق تفادياً لتضخم غير مبرَّر.

---

## 1.2.0 — 2026-08-28 — تعميم القالب

إزالة كل ربط بين الاستوديو واسم طبيب/ة بعينه/ها؛ `identity/house-rules.md §١`
أصبح نقطة التخصيص الوحيدة بدل تكرار فقرة الهوية يدوياً في 11 ملف مهارة.
التفاصيل الكاملة في `README.md § سجل التحديثات`.

## 1.1.6 — 2026-08-28

أول ترقية `TESTING → ACTIVE` فعلية (`content-case-post-reviewer`) عبر مسار
`lifecycle-versioning.md` الموثَّق، على حالة حقيقية من الحساب.

## 1.1.5 — 2026-08-28

تحقُّق مباشر عبر `ListSkills` من 7 مهارات خارجية مذكورة سابقاً كتحذيرات؛
إغلاق فعلي (لا جزئي) لفجوة `project_read`/`project_write` غير الموجودة في
Cowork.

## 1.1.4 — 2026-08-28

إصلاح تحذير `orphan_assistant` كاذب على `system-assistant-orchestrator`
(تصميم مقصود، لا عيب).

## 1.1.3 — 2026-08-28

إصلاح رفض رفع فعلي: حد 1024 حرفاً على `description` غير موثَّق سابقاً؛
فحص `description_length` جديد يمنع تكراره.

## 1.1.2 — 2026-08-28

إصلاح افتراضات `project_read`/`project_write` غير الموجودة في بيئة Cowork
عبر 3 مهارات نظام.

## 1.1.1 — 2026-08-28

إصلاح فجوة إنفاذ حوكمة: محرّك التوجيه الفعلي كان لا يميّز `TESTING` عن
`ACTIVE` عبر `description`؛ وسم `[STATUS: ...]` إلزامي أُضيف.

## 1.0.0 — 2026-08-21

مرحلة Foundation Hardening — خط الأساس الأول الموثَّق والمختبَر آلياً.
