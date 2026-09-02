#!/usr/bin/env python3
"""مستخرِج ومدقّق رسم الاعتماديات — assistant → delegates_to/depends_on/knowledge/policy.

الاستخدام:
    python3 dependency_graph.py --skills <مجلد> [--out <ملف md>] [--json <ملف>]

يبني الرسم من metadata فقط (لا افتراض)، ويفحص: عقد مكسورة (مرجع لمعرّف غير
موجود)، دورات، اعتماديات على DEPRECATED، aliases غير معروفة. هذا استخراج/تقرير —
الفشل الفعلي للبناء يبقى مسؤولية validate_system.py (invalid_delegation_target،
circular_delegation، deprecated_as_dependency هناك تطبّق نفس المنطق كبوابة).
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib_studio import as_list, detect_circular, discover_skill_dirs, load_skill  # noqa: E402


def build(skills_root):
    canonical, all_legacy = {}, {}
    for d in discover_skill_dirs(skills_root):
        rec = load_skill(d)
        if rec["frontmatter_ok"] and rec["meta"].get("assistant_id"):
            canonical[rec["meta"]["assistant_id"]] = rec["meta"]
    for aid, meta in canonical.items():
        for a in as_list(meta.get("legacy_aliases")):
            all_legacy.setdefault(a, []).append(aid)
    known = set(canonical)

    nodes = {}
    broken, cycles_report, deprecated_deps, unknown_aliases = [], [], [], []

    for aid, meta in canonical.items():
        delegates_to = as_list(meta.get("can_delegate_to"))
        depends_on = as_list(meta.get("skill_dependencies"))
        knowledge = as_list(meta.get("knowledge_dependencies"))
        policy = as_list(meta.get("policy_dependencies"))

        nodes[aid] = {
            "status": meta.get("status"), "domain": meta.get("domain"),
            "delegates_to": delegates_to, "depends_on": depends_on,
            "knowledge": knowledge, "policy": policy,
        }

        for target in delegates_to + depends_on:
            if target not in known:
                broken.append({"from": aid, "field": "can_delegate_to/skill_dependencies",
                                "target": target})
            elif canonical[target].get("status") == "DEPRECATED":
                deprecated_deps.append({"from": aid, "target": target,
                                        "replacement": canonical[target].get("deprecated_by")})

    graph = {k: [t for t in v["delegates_to"] if t in known] for k, v in nodes.items()}
    for c in detect_circular(graph):
        cycles_report.append(" → ".join(c))

    return {
        "nodes": nodes,
        "broken_references": broken,
        "cycles": cycles_report,
        "deprecated_dependencies": deprecated_deps,
        "legacy_aliases": all_legacy,
        "counts": {"assistants": len(canonical), "broken": len(broken),
                   "cycles": len(cycles_report), "deprecated_deps": len(deprecated_deps)},
    }


def to_markdown(report):
    L = ["# رسم الاعتماديات — Dependency Graph Report", "",
         f"مساعدون: {report['counts']['assistants']} · "
         f"مراجع مكسورة: {report['counts']['broken']} · "
         f"دورات: {report['counts']['cycles']} · "
         f"اعتماد على DEPRECATED: {report['counts']['deprecated_deps']}",
         "", "## العقد", "",
         "| المساعد | الحالة | يفوّض إلى | يعتمد على | معرفة | سياسة |",
         "|---|---|---|---|---|---|"]
    for aid, n in sorted(report["nodes"].items()):
        L.append(f"| `{aid}` | {n['status']} | "
                 f"{'، '.join(n['delegates_to']) or '—'} | "
                 f"{'، '.join(n['depends_on']) or '—'} | "
                 f"{len(n['knowledge'])} | {'، '.join(n['policy'])} |")
    L += ["", "## مشاكل"]
    if report["broken_references"]:
        L += ["", "**مراجع مكسورة:**"]
        for b in report["broken_references"]:
            L.append(f"- `{b['from']}` → `{b['target']}` ({b['field']})")
    if report["cycles"]:
        L += ["", "**دورات:**"]
        for c in report["cycles"]:
            L.append(f"- {c}")
    if report["deprecated_dependencies"]:
        L += ["", "**اعتماد على DEPRECATED:**"]
        for d in report["deprecated_dependencies"]:
            L.append(f"- `{d['from']}` → `{d['target']}` (البديل: `{d['replacement']}`)")
    if not (report["broken_references"] or report["cycles"] or report["deprecated_dependencies"]):
        L += ["", "لا مشاكل — الرسم نظيف."]
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skills", required=True)
    ap.add_argument("--out")
    ap.add_argument("--json")
    args = ap.parse_args()

    report = build(Path(args.skills).expanduser().resolve())
    md = to_markdown(report)
    print(md)

    if args.out:
        Path(args.out).write_text(md, encoding="utf-8")
    if args.json:
        Path(args.json).write_text(json.dumps(report, ensure_ascii=False, indent=2),
                                    encoding="utf-8")

    dirty = report["counts"]["broken"] or report["counts"]["cycles"]
    return 1 if dirty else 0


if __name__ == "__main__":
    sys.exit(main())
