#!/usr/bin/env python3
"""توليد خريطة ترحيل المعرّفات من migration-spec.yaml — لا تُحرَّر يدوياً."""

import argparse
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent))
from lib_studio import discover_skill_dirs, load_skill  # noqa: E402


def flat(s):
    return " ".join(str(s or "").split())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--skills", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    spec = yaml.safe_load(Path(args.spec).read_text(encoding="utf-8"))

    # من يشير إلى من — يُقرأ من الملفات المُرحَّلة لا من الافتراض
    refs = {}
    for d in discover_skill_dirs(Path(args.skills).expanduser().resolve()):
        rec = load_skill(d)
        if not rec["frontmatter_ok"]:
            continue
        m = rec["meta"]
        aid = m.get("assistant_id")
        targets = set()
        for key in ("can_delegate_to", "cannot_delegate_to", "skill_dependencies"):
            for t in (m.get(key) or []):
                targets.add(t)
        for n in (m.get("negative_triggers") or []):
            if isinstance(n, dict) and n.get("route_to"):
                targets.add(n["route_to"])
        for t in targets:
            refs.setdefault(t, set()).add(aid)

    L = ["# خريطة ترحيل المعرّفات — ID Migration Map", "",
         "> **ملف مولَّد** من `governance/migration-spec.yaml` — لا يُحرَّر يدوياً.",
         "> حقل REFERENCED BY مقروء من الملفات المُرحَّلة الفعلية لا من الافتراض.", "",
         f"**إصدار المواصفة:** {spec['meta']['spec_version']} · "
         f"**التاريخ:** {spec['meta']['generated']} · "
         f"**المرحلة:** {spec['meta']['phase']}", "",
         "## نطاقات الحوكمة", "",
         "| النطاق | الوصف | الخطر | الإجراء |", "|---|---|---|---|"]
    for k, v in spec["tiers"].items():
        L.append(f"| `{k}` | {flat(v['description'])} | {v['risk']} | "
                 f"{v.get('action', 'MIGRATE')} |")
    L += ["", "**المنطق:** " + " · ".join(
        f"`{k}` — {flat(v['rationale'])}" for k, v in spec["tiers"].items()
        if v.get("rationale")), ""]

    L += ["## القيود المنفَّذة", ""]
    for e in spec["assistants"]:
        rb = sorted(refs.get(e["canonical_id"], []))
        deps = sorted(set((e["metadata"].get("skill_dependencies") or [])
                          + (e["metadata"].get("can_delegate_to") or [])))
        L += [f"### `{e['old_id']}`", "",
              "```",
              f"OLD ID:        {e['old_id']}",
              f"CANONICAL ID:  {e['canonical_id']}",
              f"ACTION:        {e['action']}",
              f"TIER:          {e['tier']}",
              f"RISK:          {e['risk']}",
              "",
              "REFERENCED BY:",
              *([f"  - {r}" for r in rb] or ["  (لا مراجع داخلية)"]),
              "",
              "DEPENDENCIES:",
              *([f"  - {d}" for d in deps] or ["  (لا اعتماديات)"]),
              "",
              f"REASON:        {flat(e['reason'])}",
              "```", ""]

    if spec.get("deferred"):
        L += ["## قيود مؤجَّلة — ACTION: REVIEW / KEEP", "",
              "لم تُنفَّذ في هذه المرحلة. سبب التأجيل مذكور، وشرط رفع التأجيل معه.", ""]
        for d in spec["deferred"]:
            L += [f"### `{d['id']}`", "", "```",
                  f"ACTION:            {d['action']}",
                  f"TIER:              {d['tier']}",
                  f"RISK:              {d['risk']}",
                  f"PROPOSED CANONICAL:{d.get('proposed_canonical_id', '—')}",
                  "",
                  "REFERENCED BY:",
                  *([f"  - {r}" for r in d.get("referenced_by", [])] or ["  (غير محصور)"]),
                  "",
                  f"REASON:            {flat(d['reason'])}",
                  f"UNBLOCK:           {flat(d.get('unblock_condition', 'قرار مالك العيادة'))}",
                  "```", ""]

    if spec.get("duplicates"):
        L += ["## تكرارات وأسماء قديمة — قرارات بلا حذف", "",
              "| العنصر | المقابل | التشابه | القرار | السبب | خطوة يدوية |",
              "|---|---|---|---|---|---|"]
        for d in spec["duplicates"]:
            L.append(f"| `{d.get('item_a')}` | "
                     f"{'`'+str(d['item_b'])+'`' if d.get('item_b') else '—'} | "
                     f"{d.get('similarity') or '—'} | **{d.get('decision')}** | "
                     f"{flat(d.get('reason'))} | {flat(d.get('manual_step', '—'))} |")
        L += ["", "**لا حذف في هذه المرحلة** — حتى `DELETE_CANDIDATE` يبقى حتى قرار مالك العيادة.", ""]

    if spec.get("policies"):
        L += ["## السياسات", "", "| المعرّف | المسار | النوع | النطاق | التجاوز | الإجراء |",
              "|---|---|---|---|---|---|"]
        for p in spec["policies"]:
            L.append(f"| `{p['id']}` | `{p['path']}` | {p['type']} | {p['scope']} | "
                     f"{'مسموح' if p['override_allowed'] else '**ممنوع**'} | {p['action']} |")
        L.append("")

    Path(args.out).write_text("\n".join(L), encoding="utf-8")
    print(f"وُلّدت خريطة الترحيل: {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
