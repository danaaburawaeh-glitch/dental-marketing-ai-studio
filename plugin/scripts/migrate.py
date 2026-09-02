#!/usr/bin/env python3
"""ترحيل المعرّفات وتطبيع المخطط وفق governance/migration-spec.yaml.

الاستخدام:
    python3 migrate.py --spec <spec.yaml> --out <مجلد الهدف> [--dry-run]

المراحل: نسخ احتياطي ← نسخ المصدر ← تطبيع frontmatter ← حقن المخطط
← تحديث المراجع المتقاطعة ← تسجيل legacy_aliases.

لا يحذف ولا يعدّل المصدر إطلاقاً — يكتب شجرة جديدة.
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent))
from lib_studio import parse_frontmatter  # noqa: E402

META_ORDER = [
    "assistant_id", "display_name", "domain", "role", "purpose",
    "triggers", "negative_triggers",
    "required_inputs", "optional_inputs", "outputs",
    "knowledge_dependencies", "policy_dependencies",
    "skill_dependencies", "tool_dependencies",
    "can_delegate_to", "cannot_delegate_to",
    "routing_priority", "safety_level",
    "status", "version", "last_tested_version",
    "owner", "created_at", "last_updated", "last_tested",
    "evaluation_suite", "legacy_aliases", "deprecated_by", "notes",
]


def build_metadata(entry, spec_meta):
    m = dict(entry.get("metadata") or {})
    meta = {
        "assistant_id": entry["canonical_id"],
        "owner": m.get("owner", "clinic-owner"),
        "last_updated": spec_meta["generated"],
        "last_tested": None,
        "last_tested_version": None,  # يُختم بعد نجاح الاختبارات فقط
        "evaluation_suite": "governance/routing-tests.yaml",
        "legacy_aliases": [entry["old_id"]],
        "deprecated_by": None,
        "notes": m.get("notes", ""),
    }
    meta.update({k: v for k, v in m.items() if k not in ("owner", "notes")})
    meta["assistant_id"] = entry["canonical_id"]
    meta["legacy_aliases"] = [entry["old_id"]]
    meta["last_tested_version"] = None
    meta["last_tested"] = None
    meta["last_updated"] = spec_meta["generated"]
    ordered = {k: meta[k] for k in META_ORDER if k in meta}
    ordered.update({k: v for k, v in meta.items() if k not in ordered})
    return ordered


def rewrite_ids(text, mapping):
    """يستبدل كل معرّف قديم بالمعرّف الكانوني، مع احترام حدود الكلمة."""
    changed = 0
    # الأطول أولاً حتى لا يبتلع معرّف قصير جزءاً من أطول
    for old in sorted(mapping, key=len, reverse=True):
        new = mapping[old]
        pattern = r"(?<![A-Za-z0-9_-])" + re.escape(old) + r"(?![A-Za-z0-9-])"
        text, n = re.subn(pattern, new, text)
        changed += n
    return text, changed


def render_frontmatter(canonical_id, description, metadata):
    import textwrap
    flat = " ".join(description.split())
    body = "\n".join("  " + ln for ln in textwrap.wrap(flat, width=110))
    meta_yaml = yaml.safe_dump(
        metadata, allow_unicode=True, sort_keys=False, default_flow_style=False, width=100
    ).rstrip("\n")
    meta_indented = "\n".join("  " + ln for ln in meta_yaml.splitlines())
    return f"---\nname: {canonical_id}\ndescription: >\n{body}\nmetadata:\n{meta_indented}\n---\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--backup")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    spec = yaml.safe_load(Path(args.spec).read_text(encoding="utf-8"))
    entries = spec["assistants"]
    spec_meta = spec["meta"]
    mapping = {e["old_id"]: e["canonical_id"] for e in entries}

    out_root = Path(args.out).expanduser().resolve()
    report = {"migrated": [], "skipped": [], "ref_updates": 0}

    # ── نسخ احتياطي ──────────────────────────────────────────────────────────
    if args.backup and not args.dry_run:
        backup = Path(args.backup).expanduser().resolve()
        backup.mkdir(parents=True, exist_ok=True)
        for e in entries:
            src = Path(e["source"])
            if src.is_dir():
                dst = backup / src.name
                if dst.exists():
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
        print(f"نسخة احتياطية: {backup}")

    for e in entries:
        src = Path(e["source"]).expanduser().resolve()
        if not (src / "SKILL.md").is_file():
            report["skipped"].append({"id": e["old_id"], "why": f"المصدر غير موجود: {src}"})
            continue

        dst = out_root / e["canonical_id"]
        if args.dry_run:
            report["migrated"].append({
                "old": e["old_id"], "new": e["canonical_id"],
                "action": e["action"], "risk": e["risk"], "target": str(dst),
            })
            continue

        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)

        skill_md = dst / "SKILL.md"
        text = skill_md.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        if fm is None:
            report["skipped"].append({"id": e["old_id"], "why": "frontmatter غير صالح"})
            continue

        description, n1 = rewrite_ids(fm.get("description", ""), mapping)
        body, n2 = rewrite_ids(body, mapping)
        report["ref_updates"] += n1 + n2

        metadata = build_metadata(e, spec_meta)
        skill_md.write_text(
            render_frontmatter(e["canonical_id"], description, metadata) + body,
            encoding="utf-8",
        )

        # تحديث المراجع داخل ملفات المرجع المرافقة
        for extra in dst.rglob("*.md"):
            if extra.name == "SKILL.md":
                continue
            t = extra.read_text(encoding="utf-8")
            t2, n = rewrite_ids(t, mapping)
            if n:
                extra.write_text(t2, encoding="utf-8")
                report["ref_updates"] += n

        report["migrated"].append({
            "old": e["old_id"], "new": e["canonical_id"],
            "action": e["action"], "risk": e["risk"], "target": str(dst),
        })

    mode = "محاكاة" if args.dry_run else "تنفيذ"
    print(f"\nالترحيل ({mode})\n" + "─" * 52)
    for m in report["migrated"]:
        print(f"  {m['old']:42s} → {m['new']}   [{m['risk']}]")
    for s in report["skipped"]:
        print(f"  ✗ {s['id']}: {s['why']}")
    print("─" * 52)
    print(f"مُرحَّل: {len(report['migrated'])} · متخطى: {len(report['skipped'])} · "
          f"مراجع محدَّثة: {report['ref_updates']}")
    return 1 if report["skipped"] else 0


if __name__ == "__main__":
    sys.exit(main())
