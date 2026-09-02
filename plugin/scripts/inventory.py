#!/usr/bin/env python3
"""جرد كامل لكل المهارات والمساعدين والسياسات في النظام.

الاستخدام:
    python3 inventory.py <جذر أو أكثر> --out <ملف json> [--md <ملف markdown>]

يقرأ الملفات الفعلية لا الفهارس، ويستخرج metadata الحقيقية، ويبني رسم المراجع.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib_studio import (  # noqa: E402
    GLOBAL_POLICY_IDS, ID_RE, as_list, discover_skill_dirs, find_references,
    load_skill, write_json,
)

# أنماط الأسماء المشبوهة — تُرصد ولا تُصلح تلقائياً
LEGACY_PATTERNS = [
    (r"^\d+-", "بادئة رقم تسلسلي"),
    (r"-inst$|-insta$", "لاحقة مبتورة (inst/insta)"),
    (r"^(dana|drdana|dr-dana)-", "اسم شخص في المعرّف"),
    (r"-test$|^test-", "مهارة اختبار"),
]

NON_DESCRIPTIVE = {"lower", "test", "temp", "new", "old", "copy", "final", "misc"}


def classify(rec):
    name = rec.get("name") or rec["dir_name"]
    flags = []
    for pattern, label in LEGACY_PATTERNS:
        import re
        if re.search(pattern, name):
            flags.append(label)
    if name in NON_DESCRIPTIVE or len(name) <= 5:
        flags.append("اسم غير وصفي")
    if not ID_RE.match(name):
        flags.append("لا يطابق صيغة kebab-case")
    desc = rec.get("description", "")
    if len(desc) < 80:
        flags.append("وصف أقصر من أن يُطابَق")
    if desc and '"' not in desc and "«" not in desc:
        flags.append("بلا عبارات تشغيل مقتبسة")
    if not rec.get("meta"):
        flags.append("بلا metadata")
    return flags


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("roots", nargs="+")
    ap.add_argument("--out", required=True)
    ap.add_argument("--md")
    args = ap.parse_args()

    # provenance من manifest الحساب: custom / anthropic / anthropic-example
    provenance = {}
    for root in args.roots:
        manifest = Path(root).expanduser().resolve() / "manifest.json"
        if manifest.is_file():
            import json as _json
            try:
                data = _json.loads(manifest.read_text(encoding="utf-8"))
                for entry in data.get("skills", []):
                    provenance[entry.get("name")] = entry.get("source", "")
            except (ValueError, OSError):
                pass

    records = []
    for root in args.roots:
        root_path = Path(root).expanduser().resolve()
        for d in discover_skill_dirs(root_path):
            rec = load_skill(d)
            rec["root"] = str(root_path)
            rec["source"] = (
                "account" if "skills/synced" in str(d)
                else "plugin" if "plugins/synced" in str(d)
                else "working-copy"
            )
            rec["provenance"] = provenance.get(rec["name"] or rec["dir_name"], "")
            records.append(rec)

    known_ids = {r["name"] or r["dir_name"] for r in records}

    inventory = []
    for rec in records:
        current_id = rec["name"] or rec["dir_name"]
        meta = rec["meta"]
        text = rec.get("raw", "")
        refs = sorted(find_references(text, known_ids, self_id=current_id))
        inventory.append({
            "current_id": current_id,
            "display_name": meta.get("display_name") or "",
            "file_path": rec["file_path"],
            "type": "policy" if current_id in GLOBAL_POLICY_IDS else "skill",
            "source": rec["source"],
            "provenance": rec.get("provenance", ""),
            "domain": meta.get("domain") or "",
            "version": meta.get("version") or "",
            "status": meta.get("status") or "",
            "id_matches_dir": current_id == rec["dir_name"],
            "frontmatter_ok": rec["frontmatter_ok"],
            "parse_error": rec["parse_error"],
            "description_len": len(rec["description"]),
            "body_words": len(rec["body"].split()),
            "schema_fields": sorted(meta.keys()),
            "references_to": refs,
            "referenced_by": [],
            "flags": classify(rec),
            "legacy_aliases": as_list(meta.get("legacy_aliases")),
        })

    by_id = {item["current_id"]: item for item in inventory}
    for item in inventory:
        for target in item["references_to"]:
            if target in by_id:
                by_id[target]["referenced_by"].append(item["current_id"])
    for item in inventory:
        item["referenced_by"] = sorted(set(item["referenced_by"]))

    dupes = {}
    for item in inventory:
        dupes.setdefault(item["current_id"], []).append(item["file_path"])
    duplicate_ids = {k: v for k, v in dupes.items() if len(v) > 1}

    payload = {
        "counts": {
            "total": len(inventory),
            "account": sum(1 for i in inventory if i["source"] == "account"),
            "plugin": sum(1 for i in inventory if i["source"] == "plugin"),
            "working_copy": sum(1 for i in inventory if i["source"] == "working-copy"),
            "with_metadata": sum(1 for i in inventory if i["schema_fields"]),
            "flagged": sum(1 for i in inventory if i["flags"]),
        },
        "duplicate_ids": duplicate_ids,
        "items": sorted(inventory, key=lambda i: (i["source"], i["current_id"])),
    }

    write_json(Path(args.out), payload)

    if args.md:
        lines = ["# جرد النظام", "",
                 f"إجمالي: {payload['counts']['total']} · "
                 f"حساب: {payload['counts']['account']} · "
                 f"إضافات: {payload['counts']['plugin']} · "
                 f"نسخ عمل: {payload['counts']['working_copy']} · "
                 f"بـ metadata: {payload['counts']['with_metadata']} · "
                 f"موسوم: {payload['counts']['flagged']}", "",
                 "| current_id | source | domain | version | status | refs→ | ←refs | ملاحظات |",
                 "|---|---|---|---|---|---|---|---|"]
        for i in payload["items"]:
            lines.append(
                f"| `{i['current_id']}` | {i['source']} | {i['domain'] or '—'} | "
                f"{i['version'] or '—'} | {i['status'] or '—'} | "
                f"{len(i['references_to'])} | {len(i['referenced_by'])} | "
                f"{'، '.join(i['flags']) or '—'} |"
            )
        Path(args.md).write_text("\n".join(lines) + "\n", encoding="utf-8")

    c = payload["counts"]
    print(f"جرد: {c['total']} عنصر · {c['flagged']} موسوم · "
          f"{len(duplicate_ids)} معرّف مكرر")
    print(f"كُتب: {args.out}" + (f" و {args.md}" if args.md else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
