# Dental Marketing AI Studio v1.4.1 — Built-in Update Checker

This maintenance release adds a built-in, read-only update checker to Dental Marketing AI Studio.

## What's new

- Added `system-update-checker` as the 29th Skill.
- Users can ask in Arabic or English whether a newer version is available.
- The checker compares the installed Semantic Version with the latest public GitHub Release.
- When a newer version exists, it provides the permanent latest-download link.
- If the live check cannot reach GitHub, it explicitly reports that the check failed instead of guessing.

## Safety

The update checker is read-only. It does not install, delete, replace, upload, or modify user files automatically.

## Quality gates

- 29 Skills
- Routing: 50/50 passed — 100% accuracy, 0 ambiguity
- Standalone tests: 6/6 passed
- Orchestration: 34/34 passed
- Required unresolved dependencies: 0
- Broken internal references: 0
- Dependency cycles: 0
- Clinical Firewall inheritance: 29/29

## Distribution file

Upload the package as:

`Dental-Marketing-AI-Studio-Latest.zip`

The permanent download URL remains:

`https://github.com/danaaburawaeh-glitch/dental-marketing-ai-studio/releases/latest/download/Dental-Marketing-AI-Studio-Latest.zip`
