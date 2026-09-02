#!/usr/bin/env python3
"""Check Dental Marketing AI Studio latest public GitHub release.
Read-only: performs a public GET and never modifies installed files.
"""
from __future__ import annotations
import json
import pathlib
import re
import sys
import urllib.request

REPO = "danaaburawaeh-glitch/dental-marketing-ai-studio"
API = f"https://api.github.com/repos/{REPO}/releases/latest"
LATEST_PAGE = f"https://github.com/{REPO}/releases/latest"
DOWNLOAD = f"https://github.com/{REPO}/releases/latest/download/Dental-Marketing-AI-Studio-Latest.zip"


def parse_version(value: str) -> tuple[int, int, int]:
    m = re.fullmatch(r"v?(\d+)\.(\d+)\.(\d+)", value.strip())
    if not m:
        raise ValueError(f"Unsupported version format: {value!r}")
    return tuple(map(int, m.groups()))


def installed_version() -> str:
    root = pathlib.Path(__file__).resolve().parents[1]
    data = json.loads((root / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    return str(data["version"])


def main() -> int:
    installed = installed_version()
    result = {
        "product": "Dental Marketing AI Studio",
        "installed_version": installed,
        "latest_version": None,
        "status": "unknown",
        "update_available": None,
        "latest_release_url": LATEST_PAGE,
        "download_url": DOWNLOAD,
        "error": None,
    }
    try:
        req = urllib.request.Request(API, headers={"Accept": "application/vnd.github+json", "User-Agent": "Dental-Marketing-AI-Studio-Update-Checker"})
        with urllib.request.urlopen(req, timeout=8) as response:
            payload = json.load(response)
        latest_tag = str(payload["tag_name"])
        latest = latest_tag.lstrip("v")
        iv, lv = parse_version(installed), parse_version(latest)
        result["latest_version"] = latest
        result["release_name"] = payload.get("name")
        result["release_notes"] = payload.get("body") or ""
        if lv > iv:
            result["status"] = "update_available"
            result["update_available"] = True
        elif lv == iv:
            result["status"] = "up_to_date"
            result["update_available"] = False
        else:
            result["status"] = "installed_ahead_of_public"
            result["update_available"] = False
    except Exception as exc:
        result["status"] = "check_failed"
        result["error"] = f"{type(exc).__name__}: {exc}"
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] != "check_failed" else 2


if __name__ == "__main__":
    sys.exit(main())
