#!/usr/bin/env python3
"""ختم الاختبار — يضبط last_tested_version و last_tested بعد نجاح الاختبارات.

الاستخدام:
    python3 stamp_tested.py --skills <مجلد> --routing-json <نتيجة الاختبارات>
                            --date YYYY-MM-DD [--only id,id] [--exclude id,id]

لا يختم إلا إذا كانت نتيجة اختبارات التوجيه صفر فشل. الختم هو ما يجعل
مساعداً ACTIVE مؤهلاً للتوجيه — لا يُضبط يدوياً ولا يُفترض.
"""

import argparse
import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent))
from lib_studio import discover_skill_dirs, load_skill, parse_frontmatter  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skills", required=True)
    ap.add_argument("--routing-json", required=True)
    ap.add_argument("--date", required=True)
    ap.add_argument("--only")
    ap.add_argument("--exclude", default="")
    args = ap.parse_args()

    routing = json.loads(Path(args.routing_json).read_text(encoding="utf-8"))
    if routing.get("failed", 1) != 0:
        print(f"✗ لا ختم: اختبارات التوجيه فيها {routing.get('failed')} فشل.")
        return 1

    only = {s.strip() for s in args.only.split(",")} if args.only else None
    exclude = {s.strip() for s in args.exclude.split(",") if s.strip()}

    stamped, skipped = [], []
    for d in discover_skill_dirs(Path(args.skills).expanduser().resolve()):
        rec = load_skill(d)
        if not rec["frontmatter_ok"]:
            continue
        aid = rec["meta"].get("assistant_id")
        if not aid or (only and aid not in only) or aid in exclude:
            skipped.append(aid)
            continue

        path = Path(rec["file_path"])
        text = path.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        meta = fm["metadata"]
        meta["last_tested_version"] = meta["version"]
        meta["last_tested"] = args.date

        desc_lines = [ln for ln in text.split("description: >", 1)[1]
                      .split("\nmetadata:", 1)[0].splitlines() if ln.strip()]
        meta_yaml = yaml.safe_dump(meta, allow_unicode=True, sort_keys=False,
                                   default_flow_style=False, width=100).rstrip("\n")
        meta_indented = "\n".join("  " + ln for ln in meta_yaml.splitlines())
        new_fm = (f"---\nname: {fm['name']}\ndescription: >\n"
                  + "\n".join(desc_lines) + f"\nmetadata:\n{meta_indented}\n---\n")
        path.write_text(new_fm + body, encoding="utf-8")
        stamped.append(aid)

    print(f"مختوم: {len(stamped)}")
    for a in stamped:
        print(f"  ✓ {a}")
    if skipped:
        print(f"غير مختوم: {'، '.join(x for x in skipped if x)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
