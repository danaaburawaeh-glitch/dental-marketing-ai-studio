#!/usr/bin/env python3
"""مولّد فهرس المعرفة — من frontmatter ملفات knowledge/ إلى knowledge/generated-index.md.

الاستخدام:
    python3 build_knowledge_index.py --knowledge-root <مجلد> --out <ملف md> [--json <ملف>]

**لا يستبدل knowledge/INDEX.md الحالي في الـ Project.** يُنتج ملفاً منفصلاً
(افتراضياً knowledge/generated-index.md) حتى يثبت الانتقال الكامل — انظر
governance/knowledge-schema.md § المولِّد.
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib_studio import parse_frontmatter  # noqa: E402

REQUIRED_FOR_ACTIVE = ["owner", "source", "last_verified", "used_by"]
STATUSES = ["DRAFT", "REVIEWED", "ACTIVE", "SUPERSEDED", "ARCHIVED"]


def discover_knowledge_files(root: Path):
    found = []
    for p in root.rglob("*.md"):
        if p.name in ("generated-index.md", "INDEX.md", "assistants-registry.md"):
            continue
        found.append(p)
    return sorted(found)


def load_entry(path: Path):
    text = path.read_text(encoding="utf-8")
    fm, _ = parse_frontmatter(text)
    if not fm or "knowledge_id" not in fm:
        return None, "بلا frontmatter صالح أو knowledge_id مفقود"
    problems = []
    status = fm.get("status")
    if status not in STATUSES:
        problems.append(f"status غير معروف: {status}")
    if status == "ACTIVE":
        for f in REQUIRED_FOR_ACTIVE:
            if fm.get(f) in (None, "", []) and f != "used_by":
                problems.append(f"ACTIVE بلا {f}")
            if f == "used_by" and fm.get(f) is None:
                problems.append("ACTIVE بلا used_by (حتى لو فارغة، يجب أن يكون []، لا غائبة)")
    fm["_path"] = str(path)
    return fm, "؛ ".join(problems) if problems else None


def build(root: Path):
    entries, problems = [], []
    for p in discover_knowledge_files(root):
        fm, err = load_entry(p)
        if fm is None:
            problems.append({"file": str(p), "error": err})
            continue
        entries.append(fm)
        if err:
            problems.append({"file": str(p), "error": err})
    return entries, problems


def to_markdown(entries, problems, root):
    L = ["# فهرس المعرفة — مولَّد آلياً", "",
         "> **ملف مولَّد — لا يُحرَّر يدوياً.** يُنتج بـ `scripts/build_knowledge_index.py` من "
         "frontmatter ملفات `knowledge/`. هذا **ليس** بديلاً عن `knowledge/INDEX.md` في الـ "
         "Project حتى إشعار آخر — انظر `governance/knowledge-schema.md`.",
         "",
         f"**عدد الملفات:** {len(entries)} · **مشاكل:** {len(problems)}", ""]

    by_status = {}
    for e in entries:
        by_status.setdefault(e.get("status", "—"), []).append(e)

    for status in STATUSES:
        group = by_status.get(status, [])
        if not group:
            continue
        L += [f"## {status}", "",
              "| knowledge_id | العنوان | المجال | المالك | آخر تأكيد | يُستخدَم من |",
              "|---|---|---|---|---|---|"]
        for e in sorted(group, key=lambda x: x.get("knowledge_id", "")):
            used = e.get("used_by") or []
            L.append(f"| `{e.get('knowledge_id')}` | {e.get('title', '—')} | "
                     f"{e.get('domain', '—')} | {e.get('owner', '—')} | "
                     f"{e.get('last_verified') or '—'} | "
                     f"{'، '.join(f'`{u}`' for u in used) or '—'} |")
        L.append("")

    if problems:
        L += ["## مشاكل مرصودة", ""]
        for p in problems:
            L.append(f"- `{p['file']}`: {p['error']}")
        L.append("")

    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--knowledge-root", required=True)
    ap.add_argument("--out", default=None)
    ap.add_argument("--json")
    args = ap.parse_args()

    root = Path(args.knowledge_root).expanduser().resolve()
    entries, problems = build(root)
    out_path = Path(args.out) if args.out else root / "generated-index.md"
    md = to_markdown(entries, problems, root)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")
    print(f"وُلّد الفهرس: {out_path} ({len(entries)} ملف، {len(problems)} مشكلة)")

    if args.json:
        Path(args.json).write_text(json.dumps(
            {"entries": entries, "problems": problems}, ensure_ascii=False, indent=2),
            encoding="utf-8")

    return 0


if __name__ == "__main__":
    sys.exit(main())
