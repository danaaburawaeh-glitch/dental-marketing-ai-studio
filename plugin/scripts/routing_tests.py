#!/usr/bin/env python3
"""اختبارات التوجيه — تحقق حتمي على مستوى الـ metadata.

الاستخدام:
    python3 routing_tests.py --skills <مجلد> --tests governance/routing-tests.yaml [--json <ملف>]

يطبّق موجّهاً حتمياً يجسّد قواعد routing-policy.md على triggers و negative_triggers
و routing_priority. هذا يتحقق من **صحة الـ metadata**، ولا يغني عن التوجيه الدلالي
الحي — لكنه يكشف التصادمات والفجوات قبل وصولها للمستخدم.
"""

import argparse
import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent))
from lib_studio import (  # noqa: E402
    ROUTABLE, as_list, discover_skill_dirs, jaccard, load_skill, token_set,
)

TRIGGER_THRESHOLD = 0.34
NEGATIVE_THRESHOLD = 0.55


def phrase_score(phrase, candidate):
    p, c = phrase.strip(), str(candidate).strip()
    if not p or not c:
        return 0.0
    if c in p:
        return 1.0
    if p in c:
        # جزء قصير داخل عبارة طويلة: ائتمان جزئي بنسبة الطول، لا مطابقة كاملة.
        # بدون هذا تُقصي عبارةٌ سالبة طويلةٌ أيَّ طلب قصير يقع داخلها.
        return len(p) / len(c)
    return jaccard(token_set(p), token_set(c))


def route(phrase, assistants):
    """يعيد (المساعد المختار، سبب، تتبّع) وفق قواعد سياسة التوجيه."""
    trace = []
    excluded, redirects = {}, {}

    for aid, meta in assistants.items():
        if meta.get("status") not in ROUTABLE:
            excluded[aid] = "حالة غير قابلة للتوجيه"
            continue
        if not meta.get("_assume_tested") and \
                meta.get("last_tested_version") != meta.get("version"):
            excluded[aid] = "إصدار غير مختبَر"
            continue
        # القاعدة ٤ — العبارات السالبة تُقصي
        best_neg, neg_target = 0.0, None
        for n in meta.get("negative_triggers") or []:
            if not isinstance(n, dict):
                continue
            s = phrase_score(phrase, n.get("match"))
            if s > best_neg:
                best_neg, neg_target = s, n.get("route_to")
        if best_neg >= NEGATIVE_THRESHOLD:
            excluded[aid] = f"عبارة سالبة ({best_neg:.2f}) → {neg_target}"
            redirects[neg_target] = max(redirects.get(neg_target, 0), best_neg)

    candidates = []
    for aid, meta in assistants.items():
        if aid in excluded:
            continue
        best = max((phrase_score(phrase, t) for t in as_list(meta.get("triggers"))),
                   default=0.0)
        if best >= TRIGGER_THRESHOLD:
            candidates.append((best, meta.get("routing_priority", 0), aid))
            trace.append(f"{aid}:{best:.2f}/p{meta.get('routing_priority')}")

    if not candidates:
        if redirects:
            target = max(redirects, key=redirects.get)
            return f"EXTERNAL:{target}" if target not in assistants else target, \
                   "إحالة عبر عبارة سالبة", trace
        return "NO_MATCH", "لا مطابقة", trace

    # القاعدة ٢ ثم ٥ — الأعلى مطابقةً، فالأعلى أولوية
    candidates.sort(key=lambda x: (-x[0], -x[1], x[2]))
    top = candidates[0]
    tied = [c for c in candidates if c[0] == top[0] and c[1] == top[1]]
    reason = "مطابقة أعلى" if len(candidates) == 1 else (
        "تعادل غير محسوم" if len(tied) > 1 else "أعلى مطابقة ثم أولوية")
    return top[2], reason, trace


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skills", required=True)
    ap.add_argument("--tests", required=True)
    ap.add_argument("--json")
    ap.add_argument("--assume-tested", action="store_true",
                    help="تجاوز قفل الاختبار — للتشغيلة التي تُنتج الختم نفسه")
    ap.add_argument("--orchestration-json",
                    help="نتيجة orchestration_tests.py --json (اختياري) لدمج orchestration accuracy")
    args = ap.parse_args()

    assistants = {}
    for d in discover_skill_dirs(Path(args.skills).expanduser().resolve()):
        rec = load_skill(d)
        if rec["frontmatter_ok"] and rec["meta"].get("assistant_id"):
            meta = dict(rec["meta"])
            meta["_assume_tested"] = args.assume_tested
            assistants[rec["meta"]["assistant_id"]] = meta

    suite = yaml.safe_load(Path(args.tests).read_text(encoding="utf-8"))
    results, failures = [], 0

    for case in suite["cases"]:
        phrase = case["phrase"]
        expected = case["expect"]
        got, reason, trace = route(phrase, assistants)
        ok = (got == expected)
        if not ok:
            failures += 1
        results.append({"phrase": phrase, "expect": expected, "got": got,
                        "ok": ok, "reason": reason, "rule": case.get("rule", ""),
                        "trace": trace})

    print("\nاختبارات التوجيه\n" + "═" * 74)
    for r in results:
        mark = "PASS" if r["ok"] else "FAIL"
        print(f"  {mark}  «{r['phrase']}»")
        if not r["ok"]:
            print(f"        متوقع: {r['expect']}")
            print(f"        فعلي : {r['got']}  ({r['reason']})")
            if r["trace"]:
                print(f"        مرشحون: {'، '.join(r['trace'][:6])}")
    print("═" * 74)
    total = len(results)
    print(f"النتيجة: {total - failures}/{total} ناجح · {failures} فاشل\n")

    # ── مقاييس مجمَّعة — Release Gate summary ──────────────────────────────
    ROUTING_RULES = {"R2", "R5", "R6", "R9", "LIFECYCLE"}
    EXCLUSION_RULES = {"R3", "R4"}
    routing_cases = [r for r in results if r["rule"] in ROUTING_RULES]
    exclusion_cases = [r for r in results if r["rule"] in EXCLUSION_RULES]
    routing_acc = (sum(1 for r in routing_cases if r["ok"]) / len(routing_cases) * 100
                   if routing_cases else None)
    exclusion_acc = (sum(1 for r in exclusion_cases if r["ok"]) / len(exclusion_cases) * 100
                      if exclusion_cases else None)
    ambiguity_count = sum(1 for r in results if r["reason"] == "تعادل غير محسوم")

    orchestration_acc = None
    if args.orchestration_json and Path(args.orchestration_json).is_file():
        odata = json.loads(Path(args.orchestration_json).read_text(encoding="utf-8"))
        svm = [r for r in odata.get("results", []) if r.get("type") == "single_vs_multi"]
        if svm:
            orchestration_acc = sum(1 for r in svm if r["ok"]) / len(svm) * 100

    def pct(v):
        return f"{v:.1f}%" if v is not None else "—"

    gate_pass = failures == 0 and (routing_acc is None or routing_acc >= 95) \
        and (exclusion_acc is None or exclusion_acc >= 95)

    print("Routing Tests")
    print("-------------")
    print(f"Total: {total}")
    print(f"Passed: {total - failures}")
    print(f"Failed: {failures}")
    print(f"Routing accuracy: {pct(routing_acc)}")
    print(f"Exclusion accuracy: {pct(exclusion_acc)}")
    print(f"Ambiguity count: {ambiguity_count}")
    print(f"Orchestration decision: {pct(orchestration_acc)}")
    print(f"Release gate: {'PASS' if gate_pass else 'FAIL'}\n")

    if args.json:
        Path(args.json).write_text(json.dumps(
            {"total": total, "passed": total - failures, "failed": failures,
             "routing_accuracy_pct": routing_acc, "exclusion_accuracy_pct": exclusion_acc,
             "ambiguity_count": ambiguity_count, "orchestration_decision_pct": orchestration_acc,
             "release_gate": "PASS" if gate_pass else "FAIL",
             "results": results}, ensure_ascii=False, indent=2), encoding="utf-8")

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
