# Changelog

All notable changes to Dental Marketing AI Studio are documented here.

## [1.4.1] — 2026-09-02

### Added
- `system-update-checker` as the 29th specialized Skill.
- Read-only Semantic Version comparison against the public GitHub Latest Release.
- Permanent latest-download link support.
- Arabic and English update-check routing.

### Safety & behavior
- The checker never installs, deletes, uploads, or replaces user files automatically.
- If live GitHub access fails, it reports that the check failed instead of claiming the installed copy is current.

### Quality checks
- 29 Skills
- Routing tests: 50/50 passed
- Orchestration tests: 34/34 passed
- Standalone tests: 6/6 passed
- Required unresolved dependencies: 0
- Broken internal references: 0
- Dependency cycles: 0
- Clinical Firewall inheritance: 29/29

## [1.4.0] — 2026-09-02

### Added
- Marketing Offer Architect
- Paid Media Planner
- Lead Funnel Optimizer
- Lead Follow-up Manager
- Campaign Director
- Marketing ROI Analyst
- Local SEO / GEO Strategist

### Improved
- Expanded the system from an Instagram-focused assistant into a broader Marketing Operating System.
- Unified workflow: Strategy → Offer → Campaign → Paid Media → Funnel → Lead Follow-up → ROI.
- Preserved existing Instagram, content, WhatsApp, orchestration and system-management Skills.

### Quality checks
- 28 Skills
- Routing tests: 46/46 passed
- Orchestration tests: 34/34 passed
- Standalone tests: 6/6 passed
- Required external dependencies: 0
- Broken internal references: 0

## [1.3.0]

Standalone edition with zero required external assistants, Skills, private knowledge files, or account-specific dependencies.
