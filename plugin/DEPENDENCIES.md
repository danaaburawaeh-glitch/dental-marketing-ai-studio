# DEPENDENCIES.md — Assistant Studio v1.3.0 Standalone Edition

> Generated as the mandatory Phase 1 Dependency Audit for the v1.2.1 → v1.3.0
> Standalone upgrade, then finalized after Phase 2–5 fixes were applied.
> Do not hand-edit the "Final Result" block below without re-running
> `tests/dependency-scan.py` — it is what proves the numbers.

## Final Result (post-upgrade)

```text
Required external skills: 0
Required external assistants: 0
Required private knowledge files: 0
Required account-specific dependencies: 0
```

All four are zero. See `tests/dependency-scan.py` output in
`RELEASE-AUDIT-v1.3.0.md` for the automated proof.

## Optional integrations (not required; system runs fully without them)

| Integration | Used by | Capability unlocked | Behavior if absent |
|---|---|---|---|
| ChatPlace (Instagram DMs, and WhatsApp once connected) | `content-whatsapp-lead-responder`, `instagram-conversion-analyst`, several `instagram-*` skills | Read live conversations/comments, send drafted replies, view automation analytics | Manual Execution Mode — skill produces copy-paste-ready message + a manual send/log checklist |
| Meta Ads (`mcp__meta_ads__*`) | `instagram-*` analytics skills, `marketing-strategy-planner` | Live campaign metrics, ad creation/edits | Falls back to Windsor.ai, then to user-supplied screenshots/exports, then asks once for the numbers |
| Windsor.ai (`mcp__Windsor_ai__*`) | `instagram-data-analyst`, `instagram-conversion-analyst`, `marketing-strategy-planner` | Cross-platform analytics without touching Meta Ads directly | Falls back to Meta Ads or ChatPlace, then manual data entry |
| Canva | `content-social-calendar-scheduler`, `content-short-form-video-planner`, `content-case-post-reviewer` | Generate/export visual assets from a brief | Skill outputs a written creative brief the user can hand to any designer or paste into Canva manually |
| Google Drive / Gmail / Calendar | `system-*` skills, `content-social-calendar-scheduler` | File storage, scheduling reminders, sending drafts | Skill outputs the content inline in chat; user copies it into whatever tool they use |
| WebSearch / WebFetch | Several skills for market/competitor research | Live web lookups | Skill proceeds using supplied information and states the assumption explicitly |

None of the above are called unconditionally by any skill. Every skill that
can use one of them performs a capability check first (see
`governance/capability-detection.md`) and has a fully-specified manual
fallback path (see `governance/standalone-guarantee.md`). No skill's core
workflow depends on any of them succeeding.

## Dependency Audit — full classification table

Legend: **A** = Required capability (must become an internal Skill) · **B** =
Optional integration (Progressive Enhancement) · **C** = Account-specific
reference (must be genericized/removed) · **D** = Broken/dangling reference
(no live effect, informational only).

| # | Dependency | Source file(s) | Type | Required/Optional | Risk | Proposed solution | Status |
|---|---|---|---|---|---|---|---|
| 1 | `whatsapp-closing-specialist` (external assistant name) | `skills/instagram-conversion-analyst/SKILL.md` (negative_trigger route_to, description, body prose) | A | Required | High — routing dead-ends for any user without this private assistant | Build internal skill `content-whatsapp-lead-responder`; repoint all references | ✅ Resolved (Phase 3) |
| 2 | `marketing-strategy-director` (external assistant name) | `skills/instagram-personal-brand-strategist/SKILL.md` (negative_trigger route_to, description, body prose) | A | Required | High — full marketing-strategy requests dead-end | Build internal skill `marketing-strategy-planner`; repoint all references | ✅ Resolved (Phase 3) |
| 3 | `linkedin-strategy` (external assistant name) | `skills/instagram-personal-brand-strategist/SKILL.md` (negative_trigger route_to) | A | Required | Medium — LinkedIn-specific asks dead-end | Absorb as one channel inside `marketing-strategy-planner` (not a separate skill — avoids bloat) | ✅ Resolved (Phase 3) |
| 4 | `social-media-calendar` (external assistant name) | `skills/instagram-content-architect/SKILL.md` (negative_trigger route_to, description, body prose) | A | Required | High — calendar/scheduling requests dead-end | Build internal skill `content-social-calendar-scheduler`; repoint all references | ✅ Resolved (Phase 3) |
| 5 | `drdana-short-form-video-plan` (external assistant name, also contains owner's name) | `skills/instagram-content-architect/SKILL.md`, `skills/instagram-reel-strategist/SKILL.md` (negative_trigger route_to, description, body prose); `governance/routing-tests.yaml` (3 test cases expecting `EXTERNAL:drdana-short-form-video-plan`) | A + C | Required | High — 30-day video plan requests dead-end; also leaks personal name in a live routing id | Build internal skill `content-short-form-video-planner`; repoint all references + update routing-tests.yaml expectations | ✅ Resolved (Phase 3 + 4) |
| 6 | `smile-doc-standardizer` (external assistant name) | `skills/content-case-post-reviewer/SKILL.md` (negative_trigger route_to) | A | Required | Medium — case-photo standardization requests dead-end | Merge capability directly into `content-case-post-reviewer` (already owns case-photo review; avoids a 5th near-duplicate skill) | ✅ Resolved (Phase 3) |
| 7 | `.claude-plugin/plugin.json` → `author.name: "Dr. Dana Aburawaeh"` | `.claude-plugin/plugin.json` | C | Required fix | Medium — real personal name shipped in package metadata, contradicts README's own v1.2.0 changelog claim that this was already fixed | Replace with `"Assistant Studio"` | ✅ Resolved (Phase 2) |
| 8 | README byline "by Dr. Dana Aburawaeh" | `README.md` (title line + intro line) | C | Required fix | Medium — personal name in first-run documentation | Replace with generic "Clinic Assistant Plugin" framing | ✅ Resolved (Phase 2) |
| 9 | `owner: dana` | `governance/telemetry-schema.yaml`, `governance/orchestrator-config.yaml`, `governance/handoff-schema.yaml`, `governance/assistant-schema.md` (template example), `governance/knowledge-schema.md` (template example) | C | Required fix | Low-Medium — inconsistent with the rest of the project's already-templated `owner: clinic-owner` convention | Replace all 5 with `owner: clinic-owner` | ✅ Resolved (Phase 2) |
| 10 | `"قرار دانا"` (Dana's decision, literal Arabic text embedded in generated-report strings) | `scripts/build_migration_map.py` (2 occurrences) | C | Required fix | Low — cosmetic but personal-name leak in generated audit reports | Replace with generic `"قرار مالك العيادة"` (clinic owner's decision) | ✅ Resolved (Phase 2) |
| 11 | `roadmap/clinical-core-plan.md` — heavy references to a private external system "Dana-DIOS" (`CORE v0.4`, `M1–M5`) at private paths (`claude/dana-dios/...`) that exist only in the original author's private Claude.ai Project | `roadmap/clinical-core-plan.md` | C | Not required (zero runtime dependency — no skill loads it) | Low functional risk, but describes an unrelated private/future product and leaks private paths | **Excluded entirely from the v1.3.0 package.** Confirmed no skill, script, or governance doc requires it at runtime. | ✅ Resolved (Phase 2) |
| 12 | "Dana-DIOS" / `claude/dana-dios/` mentions | `SYSTEM_HARDENING_REPORT.md` (2 lines) | C | Not required | Low — historical governance narrative, not a live dependency | Genericize the phrasing; drop the dangling pointer to the now-excluded roadmap file | ✅ Resolved (Phase 2) |
| 13 | `dana-instagram-growth-director` (external assistant name) | Historical `notes:` fields only (`instagram-data-analyst`, `instagram-funnel-diagnostician`, `instagram-weekly-growth-review`); `governance/migration-spec.yaml` `deferred:` section | D | Informational only | None — already resolved in v1.2.0; migration-spec.yaml records it as `DANGLING_REFERENCE_REMOVED` | No functional fix needed; left as historical record | No action needed |
| 14 | `chief-advertising-officer-cao` | `governance/migration-spec.yaml` `deferred:` section, `governance/foundation-validation-report.md`, `governance/assistant-id-migration-map.md` | D | Informational only | None — no live skill references it | No action needed; documented as historically reviewed with no live reference found | No action needed |
| 15 | `dr-dana-medical-dental-english` | `governance/migration-spec.yaml` `deferred:` section, `governance/foundation-validation-report.md` | D | Informational only | None — no live skill references it; also would fall outside clinic-management/marketing scope if ever revived | No action needed | No action needed |
| 16 | ~14 historical `source: /home/claude/...` absolute paths | `governance/migration-spec.yaml` (`assistants:` provenance records) | D | Informational only, inert | None — these are historical provenance records of where each assistant was migrated *from*, at build time; never read at runtime | Left as-is with a clarifying header note that these are historical/inert provenance data, not live paths | Noted, not modified |
| 17 | Skill-managed connectors (Gmail, Calendar, Drive, Canva, Meta Ads, Windsor.ai, ChatPlace, WebSearch/WebFetch) | `identity/house-rules.md` §7 | B | Optional | None — already designed with a "if unavailable, ask/fallback" pattern | Formalize existing pattern into `governance/capability-detection.md`; no house-rules.md edits needed (out of caution per rule 9 — do not modify House Rules without engineering justification, and none exists here) | Formalized (Phase 4) |
| 18 | `"owner": m.get("owner", "dana")` — hardcoded personal-name default in a migration script | `scripts/migrate.py` (used only if a future migration run adds another deferred assistant) | C | Required fix | Low-Medium — dormant until the script is next run, but would re-introduce a personal owner value into a brand-new skill's frontmatter | Default changed to `"clinic-owner"` | ✅ Resolved (Phase 5 — caught by `tests/dependency-scan.py`) |
| 19 | `dana-instagram-growth-director` / `drdana-short-form-video-plan` literal mentions inside 6 skills' `notes:` metadata field (engineering history, not routing logic) | `skills/content-short-form-video-planner`, `instagram-content-architect`, `instagram-data-analyst`, `instagram-funnel-diagnostician`, `instagram-reel-strategist`, `instagram-weekly-growth-review` (all `SKILL.md`) | C | Required fix | Low — informational text, but ships inside the live `SKILL.md` metadata of every install, unlike README's changelog which is pure documentation | Reworded to describe the fix ("external identifier that also carried a personal name") without repeating the literal legacy identifier; full rationale preserved | ✅ Resolved (Phase 5 — caught by `tests/dependency-scan.py`) |

## Automated verification

`tests/dependency-scan.py` is the machine-checked proof behind the table
above — it scans every `.md`/`.yaml`/`.yml`/`.json`/`.py` file in the package
(not just `skills/`) for unresolved internal references, absolute filesystem
paths, secrets/API keys, personal-name patterns, and private URLs, against a
small, explicitly-documented exception list (`governance/portability.md` §
الاستثناءات الموثَّقة — historical changelogs, ACP documents, and test
fixtures that intentionally name a *dead* external identifier to prove the
router correctly excludes it). Latest run:

```text
Required unresolved dependencies: 0
```

Full output is captured in `RELEASE-AUDIT-v1.3.0.md`.

## Notes on methodology

The three dependencies named in the task brief (`whatsapp-closing-specialist`,
`marketing-strategy-director`, `social-media-calendar`) were treated as a
starting point, not the full list, per the explicit instruction not to assume
completeness. Every file type called out in the brief was inspected:
`SKILL.md` ×21, `plugin.json`, all YAML/Markdown under `governance/`, all
`scripts/*.py`, `README.md`, `knowledge/**`, `identity/**`, and the (now
excluded) `roadmap/**`. The search combined whole-project regex grep passes
(`route_to:`, `EXTERNAL:`, known private name patterns, absolute path
patterns, secret/token/API-key patterns, `دانا|Dana|أبورواعه|Aburawaeh`) with
full reads of every governance file, every script, and 13 of 21 skill files
(the remaining were confirmed clean via targeted grep). This produced 2
additional required-capability dependencies (`linkedin-strategy`,
`smile-doc-standardizer`) beyond the 3 named in the brief, plus 8
account-specific leaks not mentioned in the brief at all.

No secrets, API keys, tokens, or hardcoded credentials of any kind were found
anywhere in the project (verified via a dedicated regex pass — see Security
Review in `RELEASE-AUDIT-v1.3.0.md`).
