# Installation & Updates

## Method A — Claude Marketplace (recommended)

This repository is a native Claude Code plugin marketplace.

1. Open your Claude plugin or marketplace settings.
2. Choose **Add marketplace**.
3. Paste the marketplace repository URL:

   ```
   https://github.com/danaaburawaeh-glitch/dental-marketing-ai-studio
   ```

4. Enable **Sync automatically**.
5. Click **Sync**.
6. Install the plugin: **`dental-marketing-ai-studio`**.

The marketplace manifest (`.claude-plugin/marketplace.json`) points at the `./plugin` directory in this repository, so Claude reads the plugin straight from `main`.

### Updating with Method A

With **Sync automatically** enabled, Claude picks up new versions from this repository on its own. This is the preferred update path — no manual download or file replacement is needed.

## Method B — Manual ZIP installation

1. Download the permanent latest-release package:

   ```
   https://github.com/danaaburawaeh-glitch/dental-marketing-ai-studio/releases/latest/download/Dental-Marketing-AI-Studio-Latest.zip
   ```

2. Keep the ZIP intact until you are ready to install it in your supported assistant/plugin environment.
3. Follow the installer or plugin import flow supported by your environment.
4. After installation, check `VERSION.json` in this repository whenever you want to confirm the latest stable version.

### Updating with Method B

The public download filename is intentionally fixed:

`Dental-Marketing-AI-Studio-Latest.zip`

Manual installations **do not update themselves**. When a new stable version is published, download the same file again and replace your existing installation yourself.

Before replacing an existing installation:

- Keep a backup of your current working version.
- Read `CHANGELOG.md` to understand what changed.
- Preserve any local/private knowledge or credentials outside the distributed package.
- Do not overwrite private configuration files unless the release notes explicitly instruct you to do so.

## Built-in Update Checker

The plugin includes a read-only Update Checker (`system-update-checker`). Ask `check for updates` or `هل يوجد تحديث؟` and it compares your installed version against the public GitHub Latest Release.

It is a status and diagnostic tool only. It never installs, deletes, overwrites, or replaces files, and it never executes remote code. For users installed via Method A, Marketplace Sync remains the actual update mechanism.

## Stable vs development versions

Only packages referenced by `VERSION.json` with `"channel": "stable"` should be used for routine clinical-practice marketing work.

## Getting update notifications

On GitHub, use **Watch → Custom → Releases** (or the closest available notification option) on this repository to receive notices when new releases are published.

## Scope

Dental Marketing AI Studio is designed for marketing, patient acquisition, content, conversion, lead follow-up and practice growth. It is not a clinical diagnosis or treatment-planning system.
