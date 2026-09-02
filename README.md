# Dental Marketing AI Studio

**AI Marketing Operating System for Dentists & Dental Clinics**

Dental Marketing AI Studio is a standalone AI marketing assistant designed for dentists and dental clinics. It turns marketing from scattered prompting into a structured operating system covering strategy, offers, campaigns, paid media, conversion, lead follow-up, ROI, Instagram growth, and Local SEO/GEO.

## Latest stable version

**v1.4.1 — Marketing OS**

This repository is also a **native Claude Code plugin marketplace**. The plugin runtime lives in [`plugin/`](plugin/) and is referenced directly by [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json), so Claude can install and sync it straight from this repository.

### What it includes

- Marketing strategy planning
- Offer architecture
- Campaign direction
- Paid media planning
- Instagram audience, content, reels, conversion and growth analysis
- Funnel optimization
- Lead follow-up workflows
- Marketing ROI analysis
- Local SEO / GEO strategy
- Social content planning and scheduling
- WhatsApp lead response support
- Internal assistant orchestration and routing
- Built-in read-only update checking

The v1.4.1 package contains **29 specialized Skills** and remains standalone with no required private assistant or unresolved required dependency.

## Installation

There are two ways to install Dental Marketing AI Studio.

### Method A — Claude Marketplace (recommended)

Marketplace repository:

```
https://github.com/danaaburawaeh-glitch/dental-marketing-ai-studio
```

Steps:

1. Open your Claude plugin or marketplace settings.
2. Choose **Add marketplace**.
3. Paste the marketplace repository URL:
   `https://github.com/danaaburawaeh-glitch/dental-marketing-ai-studio`
4. Enable **Sync automatically**.
5. Click **Sync**.
6. Install the plugin: **`dental-marketing-ai-studio`**.

**Why this method is preferred:** the marketplace points at the `./plugin` directory inside this repository. When a new version is published to `main`, Claude can pull it in automatically through **Sync automatically** — no manual download, unzip, or file replacement.

### Method B — Manual ZIP download

Use this permanent download link:

**https://github.com/danaaburawaeh-glitch/dental-marketing-ai-studio/releases/latest/download/Dental-Marketing-AI-Studio-Latest.zip**

The URL stays the same for future stable releases, as long as the release asset keeps the filename `Dental-Marketing-AI-Studio-Latest.zip`.

You can also browse all releases here:

**https://github.com/danaaburawaeh-glitch/dental-marketing-ai-studio/releases**

**Note:** manual ZIP users are responsible for updating their own installation. When a new version is released you must download the ZIP again and replace your existing installation folder yourself. Manual installs do **not** update automatically.

See [INSTALLATION.md](INSTALLATION.md) for more detailed step-by-step instructions.

## Updates

**Marketplace Sync is the preferred update mechanism.** If you installed through the Claude Marketplace with **Sync automatically** enabled, updates arrive on their own.

The built-in Update Checker remains available as a secondary status and diagnostic tool. Users can ask:

- `هل يوجد تحديث؟`
- `تحقق من التحديثات`
- `ما آخر إصدار؟`
- `check for updates`

The update checker is **read-only**. It compares the installed version against the public GitHub Latest Release and reports the result. It never installs, deletes, overwrites, or replaces files, and it never executes remote code.

Version information is machine-readable in [VERSION.json](VERSION.json). Releases use semantic versioning:

- `x.y.Z` — fixes and maintenance
- `x.Y.0` — new capabilities and Skills
- `X.0.0` — major architecture changes

## Version history

See [CHANGELOG.md](CHANGELOG.md).

## Important use note

This assistant is a marketing and practice-growth system. It is not intended to replace clinical judgment, diagnosis, treatment planning, or professional medical decision-making.

---

Created for dentists and dental teams who want a structured AI-powered marketing workflow rather than isolated prompting.