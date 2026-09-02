# RELEASE AUDIT — v1.4.1 — Built-in Update Checker

**Date:** 2026-09-02

## Scope
Maintenance release adding a read-only update checker backed by the public GitHub Latest Release endpoint.

## Changes
- Added `system-update-checker` (29th Skill).
- Added `scripts/check_update.py`.
- Added Arabic/English routing cases for update requests.
- Documented the public product distribution repository as a narrow portability exception.

## Quality Gates
- System validation: PASS — 29 Skills.
- Routing: PASS — 50/50, 100% accuracy, 0 ambiguity.
- Standalone: PASS — 6/6.
- Dependency scan: PASS — 0 unresolved required dependencies.
- Orchestration: PASS — 34/34 (2 live-run-only cases skipped by design).
- Dependency graph: PASS — 0 broken references, 0 cycles, 0 deprecated dependencies.
- Clinical firewall inheritance: 29/29.

## Update behavior
The checker performs a public GET only. It never installs, deletes, replaces, uploads, or modifies user files. If the live check fails, it reports failure explicitly and provides the public latest-release page for manual verification.
