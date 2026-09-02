#!/usr/bin/env python3
"""توليد دليل المساعدين من metadata الفعلية — لا يُحرَّر يدوياً.

الاستخدام:
    python3 build_registry.py --skills <مجلد> --out <ملف md> [--deferred <spec.yaml>]

الدليل تمثيل مولَّد للنظام الحقيقي. أي تعارض بينه وبين ملفات المهارات
يُحسم لصالح الملفات، ويُحل بإعادة التوليد لا بالتحرير.
"""

import argparse
import sys
from datetime import date
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent))
from lib_studio import as_list, discover_skill_dirs, load_skill  # noqa: E402

DOMAIN_TITLES = {
    "system": "النظام والحوكمة",
    "instagram": "نمو انستغرام",
    "content": "المحتوى والنشر",
    "patient": "المرضى والعيادة",
    "marketing": "التسويق والإعلانات",
    "clinical": "سريري",
    "research": "علمي وأكاديمي",
    "management": "إدارة",
    "finance": "مالية",
    "sales": "مبيعات",
    "legal": "قانوني",
    "operations": "تشغيل",
}


def fmt_list(values, limit=None, code=False):
    items = as_list(values)
    if limit:
        items = items[:limit]
    if not items:
        return "—"
    return " · ".join(f"`{v}`" if code else f"«{v}»" for v in items)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skills", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--deferred")
    ap.add_argument("--generated-on", default=str(date.today()))
    args = ap.parse_args()

    metas = []
    for d in discover_skill_dirs(Path(args.skills).expanduser().resolve()):
        rec = load_skill(d)
        if rec["frontmatter_ok"] and rec["meta"].get("assistant_id"):
            metas.append(rec["meta"])
    metas.sort(key=lambda m: (m.get("domain", ""), -m.get("routing_priority", 0),
                              m["assistant_id"]))

    L = [
        "# دليل المساعدين — Assistants Registry",
        "",
        "> **ملف مولَّد — لا يُحرَّر يدوياً.**",
        "> يُنتج بـ `scripts/build_registry.py` من كتل `metadata` داخل ملفات المهارات.",
        "> عند أي تعارض، الملف الفعلي للمهارة هو مصدر الحقيقة، ويُحل التعارض بإعادة التوليد.",
        "",
        f"**تاريخ التوليد:** {args.generated_on} · "
        f"**عدد المساعدين:** {len(metas)} · "
        f"**معتمد (ACTIVE):** {sum(1 for m in metas if m.get('status') == 'ACTIVE')}",
        "",
        "**السياسات العامة:** `identity/house-rules.md` + `identity/clinical-firewall.md` — "
        "يرثهما كل مساعد معاً، `override_allowed: false`. **حدود النطاق:** "
        "`governance/scope-boundary.md`. **سياسة التوجيه:** `governance/routing-policy.md`.",
        "",
    ]

    by_domain = {}
    for m in metas:
        by_domain.setdefault(m.get("domain", "—"), []).append(m)

    for domain, group in by_domain.items():
        L += [f"## {DOMAIN_TITLES.get(domain, domain)} · `{domain}`", "",
              "| المساعد | الاسم المعروض | الغرض | يشتغل عند | لا يشتغل عند ← البديل | "
              "يفوّض إلى | أولوية | سلامة | الحالة | الإصدار | آخر اختبار |",
              "|---|---|---|---|---|---|---|---|---|---|---|"]
        for m in group:
            negs = " · ".join(
                f"«{n.get('match')}» ← `{n.get('route_to')}`"
                for n in (m.get("negative_triggers") or [])[:3]
                if isinstance(n, dict)) or "—"
            L.append(
                f"| `{m['assistant_id']}` | {m.get('display_name', '—')} | "
                f"{m.get('purpose', '—')} | {fmt_list(m.get('triggers'), 3)} | {negs} | "
                f"{fmt_list(m.get('can_delegate_to'), 3, code=True)} | "
                f"{m.get('routing_priority', '—')} | {m.get('safety_level', '—')} | "
                f"{m.get('status', '—')} | {m.get('version', '—')} | "
                f"{m.get('last_tested') or '—'} |"
            )
        L.append("")

    L += ["## المعرّفات القديمة المقبولة — Legacy Aliases", "",
          "تُقبل في الطلبات القديمة ولا تُستخدم في أي ملف جديد.", "",
          "| المعرّف القديم | المعرّف الكانوني |", "|---|---|"]
    any_alias = False
    for m in metas:
        for a in as_list(m.get("legacy_aliases")):
            L.append(f"| `{a}` | `{m['assistant_id']}` |")
            any_alias = True
    if not any_alias:
        L.append("| — | — |")
    L.append("")

    if args.deferred and Path(args.deferred).is_file():
        spec = yaml.safe_load(Path(args.deferred).read_text(encoding="utf-8"))
        deferred = spec.get("deferred") or []
        dups = spec.get("duplicates") or []
        if deferred:
            L += ["## مؤجَّل إلى المرحلة التالية — خارج نطاق الترحيل الحالي", "",
                  "| المعرّف | الإجراء | الخطر | المعرّف الكانوني المقترح | السبب |",
                  "|---|---|---|---|---|"]
            for d in deferred:
                L.append(f"| `{d['id']}` | {d['action']} | {d['risk']} | "
                         f"`{d.get('proposed_canonical_id', '—')}` | "
                         f"{' '.join(str(d.get('reason', '')).split())} |")
            L.append("")
        if dups:
            L += ["## تكرارات وأسماء قديمة — قرارات موثَّقة بلا حذف", "",
                  "| العنصر | المقابل | التشابه | القرار | السبب |", "|---|---|---|---|---|"]
            for d in dups:
                L.append(f"| `{d.get('item_a')}` | "
                         f"{'`' + str(d.get('item_b')) + '`' if d.get('item_b') else '—'} | "
                         f"{d.get('similarity') or '—'} | {d.get('decision')} | "
                         f"{' '.join(str(d.get('reason', '')).split())} |")
            L.append("")

    L += ["---", "",
          "لإعادة التوليد بعد أي تعديل:", "",
          "```bash",
          "python3 scripts/validate_system.py --skills <مجلد> --policy identity/house-rules.md",
          "python3 scripts/routing_tests.py  --skills <مجلد> --tests governance/routing-tests.yaml",
          "python3 scripts/build_registry.py --skills <مجلد> --out knowledge/assistants-registry.md \\",
          "                                  --deferred governance/migration-spec.yaml",
          "```", ""]

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text("\n".join(L), encoding="utf-8")
    print(f"وُلّد الدليل: {args.out} ({len(metas)} مساعد)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
