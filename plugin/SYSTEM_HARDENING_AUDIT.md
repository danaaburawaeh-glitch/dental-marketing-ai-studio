# تدقيق التصليب — System Hardening Audit

> يُقرأ قبل أي تعديل في مرحلة System Hardening. Preserve → Harden → Test → Freeze Core → Build Clinical System.
> **لا يعيد هذا التدقيق تصميم المعمارية.** المعمارية معتمدة؛ هذا حصر لما هو موجود فعلياً (لا ما تفترضه الوثائق) وما هو ناقص فعلياً.

**تاريخ:** 2026-08-21 · **نطاق القراءة:** كل ملف في `governance/`، `identity/`، `scripts/`، `skills/*/SKILL.md` (metadata كاملة)، `knowledge/`.

---

## ١. ما هو موجود فعلياً (مُتحقَّق بالقراءة، لا بالافتراض)

### ١.١ الهوية والسياسة
| الملف | الحالة |
|---|---|
| `identity/house-rules.md` | GLOBAL_POLICY v1.1.0 · `override_allowed: false` · `priority: HIGHEST` |
| `identity/clinical-firewall.md` | GLOBAL_POLICY v1.0.0 · نفس المرتبة · فحص قبل أي شيء آخر |
| `governance/scope-boundary.md` | GOVERNANCE v1.0.0 · يحصر النطاق بـ system/instagram/marketing/content |

### ١.٢ الحوكمة
| الملف | يوفّر فعلياً |
|---|---|
| `governance/assistant-schema.md` v1.1.0 | مخطط `metadata` الإلزامي، تمييز `can_delegate_to` عن `skill_dependencies` عن `negative_triggers[].route_to` |
| `governance/lifecycle-versioning.md` v1.0.0 | 6 حالات (DRAFT→ARCHIVED)، قفل `last_tested_version == version` لـ ACTIVE، SemVer بقواعد PATCH/MINOR/MAJOR |
| `governance/routing-policy.md` v1.1.0 | 10 قواعد (٠–٩) — القاعدة ٠ الجدار السريري، بقية القواعد تحسم التوجيه أحادي المساعد فقط |
| `governance/routing-tests.yaml` | 29 حالة (إصابة/إقصاء/إحالة خارجية/لا مطابقة) — **كلها أحادية المساعد؛ لا حالة واحدة تفكيك مهمة مركّبة** |
| `governance/migration-spec.yaml` | مصدر الترحيل: 16 ترحيل مُنفَّذ + 6 `deferred` (REVIEW/KEEP) + 5 تكرارات موثَّقة (DEPRECATE/MANUAL_REVIEW/DELETE_CANDIDATE/ARCHIVE) — **لا حذف منفَّذ في أي منها** |
| `governance/assistant-id-migration-map.md`, `governance/foundation-validation-report.md` | تقارير مرحلة سابقة — مرجعية فقط |

### ١.٣ الأدوات (`scripts/`)
| الملف | يفحص/يفعل فعلياً |
|---|---|
| `lib_studio.py` | ثوابت مشتركة: `DOMAINS`, `GLOBAL_POLICY_IDS`, `KNOWN_POLICY_IDS`, `OUT_OF_SCOPE_DOMAINS`, `LIFECYCLE`, `detect_circular` (DFS على `can_delegate_to` فقط)، `jaccard`/`overlap_band` |
| `validate_system.py` | 27 فحصاً (بعد إضافة `domain_out_of_scope`): schema، id، domain، lifecycle، semver، قفل الاختبار، `policy_inheritance`/`policy_reference` لسياستين معاً، `negative_triggers_required`، `description_routable`، مراجع (external/knowledge/policy)، **دورات التفويض على `can_delegate_to` فقط**، `delegation_contradiction`، `active_overlapping_roles` (Jaccard) |
| `routing_tests.py` | موجّه حتمي (`phrase_score` + عتبتا 0.34/0.55) يحاكي القاعدة ٢/٤/٥ فقط، **لا يحاكي قواعد ٧ (تعدد النوايا) ولا ٩ (الغموض) ولا orchestration من أي نوع** |
| `build_registry.py` | يولّد `knowledge/assistants-registry.md` من metadata — تمثيل أحادي المساعد (جدول مسطّح)، لا يعرض DAG |
| `stamp_tested.py` | يختم `last_tested_version`/`last_tested` بشرط `failed==0` من `routing_tests.py --json` |
| `validate_assistant.py` | فحص بنيوي لمساعد مفرد قبل التغليف (placeholders، طول، أقسام السلامة) |
| `migrate.py`, `build_migration_map.py`, `inventory.py`, `package_assistant.py` | أدوات الترحيل والجرد والتغليف — لم تُعدَّل، لا حاجة لتعديلها في هذه المرحلة |

### ١.٤ المساعدون — 16 (بعد فصل النطاق)
15 `ACTIVE` + 1 `TESTING` (`content-case-post-reviewer`، ينتظر أول تشغيلة حقيقية معتمَدة من الطبيب/ة). كلهم v1.1.0، `last_tested_version` مطابق (بعد مسار stamp الأخير)، كلهم يرثون `house-rules` + `clinical-firewall` معاً.

### ١.٥ خريطة الاعتماديات (مستخرَجة برمجياً من metadata — مصدر الحقيقة الوحيد)

```
system-assistant-builder    → can_delegate_to → system-knowledge-manager
system-assistant-tuner      → can_delegate_to → system-knowledge-manager
instagram-audience-analyst      → can_delegate_to → instagram-content-architect
instagram-competitor-analyst    → can_delegate_to → instagram-content-architect
instagram-content-performance-analyst → can_delegate_to → instagram-experimentation-manager
instagram-reel-strategist       → can_delegate_to → content-case-post-reviewer
instagram-weekly-growth-review  → can_delegate_to → [8 مساعدين — كل فريق النمو عدا مشخّص القمع]

instagram-content-architect     → skill_dependencies → audience-analyst, content-performance-analyst,
                                                          personal-brand-strategist, competitor-analyst
instagram-content-performance-analyst → skill_dependencies → instagram-data-analyst
instagram-experimentation-manager     → skill_dependencies → instagram-data-analyst
instagram-funnel-diagnostician        → skill_dependencies → instagram-data-analyst
instagram-personal-brand-strategist   → skill_dependencies → content-performance-analyst, competitor-analyst
```

**لا دورات.** `detect_circular` يفحص `can_delegate_to` فقط (بتصميم موثَّق في `assistant-schema.md`)، وهذا يتحقق: لا عقدة تصل لنفسها عبر تفويض فعلي. `cannot_delegate_to` يمنع 3 مسارات محتملة الخطر بشكل استباقي (`instagram-content-architect` ↛ محلِّلَيه، `instagram-funnel-diagnostician`/`instagram-weekly-growth-review` كل منهما يمنع الآخر).

**ملاحظة جوهرية لبناء الـOrchestrator:** `instagram-weekly-growth-review` هو المثال الوحيد الحالي لتنسيق متعدد المساعدين — لكنه **مُقفَل الشكل** (تقرير أسبوعي بترتيب ثابت مسبقاً في تعليماته النثرية)، لا قراراً ديناميكياً وقت التنفيذ. لا يوجد اليوم آلية عامة تُحلل نية مركّبة عشوائية وتبني DAG وقت التشغيل. هذه بالضبط الفجوة التي يسدها `system-assistant-orchestrator`.

---

## ٢. ما هو ناقص فعلياً (لا مفترَض — تحقَّق غيابه بالقراءة)

| الفجوة | الأثر |
|---|---|
| لا `system-assistant-orchestrator` | لا آلية لتفكيك طلب مركّب إلى DAG من المساعدين؛ المستخدمة تعتمد على `instagram-weekly-growth-review` كحالة خاصة وحيدة، أو تستدعي المساعدين يدوياً واحداً تلو الآخر |
| لا `governance/handoff-schema.yaml` | لا عقد موحّد لما يُسلَّم بين مساعد ومساعد؛ الاعتماد حالياً على نثر غير منظَّم |
| لا `handoff_contract` في metadata أي مساعد | `skill_dependencies` تذكر *من* يُستهلَك، لكن لا تذكر *ماذا* بالضبط (الشكل، الحقول المضمونة) |
| لا `governance/release-policy.md` صريح | البوابة موجودة **إجرائياً** (validate → routing_tests → stamp) لكن غير مُثبَّتة كوثيقة سياسة رسمية بمعايير نجاح مرقَّمة |
| لا `governance/evaluation-policy.md` / `governance/evals/` | `routing-tests.yaml` وحيد وعام؛ لا مجموعات منفصلة لـ orchestration/handoff/safety/regression-baseline/edge-cases |
| لا `governance/telemetry-schema.yaml` | لا مخطط قياسي حتى لو غير مُفعَّل |
| لا `governance/core-freeze.md` | لا تجميد معماري موثَّق يمنع إعادة الهيكلة العرضية |
| لا `governance/templates/architecture-change-proposal.md` | تغييرات المخطط الأساسي (id schema، حالة، توجيه) تمر بلا قالب موحّد |
| لا حوكمة معرفة (`knowledge metadata schema`, `build_knowledge_index.py`) | `knowledge/INDEX.md` (في الـ Project) يُحرَّر يدوياً بلا مخطط موحّد لكل ملف معرفة |
| لا `scripts/orchestration_tests.py`, لا `scripts/studio_health.py` | لا اختبار لمنطق التنسيق، ولا تقرير صحة موحَّد يجمع كل الفحوص |
| لا `roadmap/clinical-core-plan.md` | لا خارطة طريق موثَّقة لمرحلة العيادة السريرية القادمة |
| `max_steps`/`max_depth` غير موجودَين لأنه لا orchestrator بعد | يجب أن يُبنيا كـ config لا hard-code، من البداية |

---

## ٣. تعارضات مكتشَفة

**لا تعارض توجيه فعلي.** آخر تشغيلة `validate_system.py` + `routing_tests.py` (قبل هذه المرحلة): `PASS WITH WARNINGS`، 29/29 توجيه، صفر أخطاء. التنبيهات العشرة كلها `external_reference` لمهارات حساب غير مُرحَّلة (منطقية ومتوقَّعة، موثَّقة في `migration-spec.yaml deferred`).

**تعارض تصميمي واحد يستحق التسجيل (لا يُحل الآن، فقط يُوثَّق):** `instagram-weekly-growth-review` يملك `can_delegate_to` لثمانية مساعدين — أوسع صلاحية تفويض في النظام حالياً. حين يُبنى الـOrchestrator، يجب أن يُقرَّر صراحة: هل يبقى هذا المساعد "منسقاً خاصاً" للتقرير الأسبوعي فقط (نطاق ثابت)، أم يُعاد بناء التقرير الأسبوعي *فوق* الـOrchestrator العام لاحقاً؟ **القرار في هذه المرحلة: يبقى كما هو.** لا تعديل على `instagram-weekly-growth-review` — التغيير هنا سيكسر نطاقه المُختبَر بلا داعٍ حقيقي (لا يحقق أياً من مبادئ §١ السبعة).

---

## ٤. خريطة التغييرات المقترحة لهذه المرحلة

كل تغيير أدناه يحقق سبباً واحداً على الأقل من §١ (منع فشل حقيقي · تقليل غموض التوجيه · منع تعارض المساعدين · تحسين السلامة · قابلية الاختبار · قابلية التنبؤ بالـ handoff · التوسع دون كسر):

| التغيير | يحقق |
|---|---|
| `system-assistant-orchestrator` (جديد) | ٢ (تقليل غموض عند مهمة مركّبة) + ٦ (handoff قابل للتنبؤ) + ٧ (توسّع مستقبلي) |
| `governance/handoff-schema.yaml` + `handoff_contract` لكل مساعد | ٦ + ٥ (قابلية الاختبار) |
| توسيع `validate_system.py` (فحوص جديدة مذكورة في §15 من الطلب) | ١ (يمنع فشلاً حقيقياً: orphan، alias collision، إلخ) |
| `scripts/orchestration_tests.py` | ٥ |
| `governance/release-policy.md` (تثبيت البوابة الموجودة فعلياً كوثيقة) | ٥ + ٧ |
| `governance/evals/*` | ٥ |
| `scripts/studio_health.py` | ٥ + ٤ (رؤية موحّدة تكشف مشاكل السلامة) |
| `governance/core-freeze.md` | ٧ (يمنع إعادة هيكلة عرضية تكسر التوسّع) |
| حوكمة المعرفة (schema + generator + بنية مجلدات فقط) | ٧ (تُمكِّن Clinical Core لاحقاً دون بناء يدوي من الصفر) |
| `roadmap/clinical-core-plan.md` (واجهات فقط) | ٧ |

**لا تغيير على:** أي `assistant_id` كانوني، أي `canonical_id` قائم، محتوى house-rules/clinical-firewall الموضوعي، `instagram-weekly-growth-review`، أي legacy alias، بنية `skills/*/SKILL.md` الحالية (إضافات فقط: `handoff_contract`).

---

## ٥. خلاصة القراءة

لا blocker حقيقي يمنع البدء. المضي مباشرة إلى Phase B (Governance Schemas).

---

> **ملاحظة v1.3.0 Standalone:** `roadmap/clinical-core-plan.md` (مذكور أعلاه كسجل تاريخي فقط) **استُبعد من حزمة v1.3.0** — كان يوثّق نظاماً سريرياً خاصاً منفصلاً تابعاً لحساب المُنشئ الأصلي، بلا أي اعتماد تشغيلي عليه من أي Skill أو Script في هذه الحزمة. هذا الملف يبقى كسجل تاريخي لقرار حوكمة سابق.
