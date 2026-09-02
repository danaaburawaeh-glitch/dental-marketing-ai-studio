#!/usr/bin/env python3
"""اختبارات التنسيق — الجزء الحتمي من system-assistant-orchestrator فقط.

الاستخدام:
    python3 orchestration_tests.py --skills <مجلد>
        [--orchestration governance/evals/orchestration-golden-set.yaml]
        [--handoff governance/evals/handoff-golden-set.yaml]
        [--safety governance/evals/safety-golden-set.yaml]
        [--edge-cases governance/evals/edge-cases.yaml]
        [--handoff-schema governance/handoff-schema.yaml]
        [--json <ملف>]

يتحقق فقط مما هو قابل للحسم آلياً: قرار Single-vs-Multi عبر نفس محرك
routing_tests.py، ترتيب الاعتماديات من handoff_contract الفعلي، اكتشاف
الدورات (حقيقية وصناعية)، وجود الهدف، صلاحية بنية عقد التسليم، حل معرّفات
legacy_alias، وتصنيف تقريبي (heuristic) لنية سلامة العبارة. هذا **لا** يحاكي
تحليل النية الدلالي الحي الذي يقوم به المنسّق وقت التشغيل — أي حالة يُذكر فيها
ذلك صراحة في ملف الحالات نفسه.
"""

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent))
from lib_studio import (  # noqa: E402
    as_list, detect_circular, discover_skill_dirs, load_skill,
)
from routing_tests import route  # noqa: E402

STATUS_CODES = [
    "COMPLETE", "PARTIAL", "BLOCKED", "NEEDS_INPUT", "ROUTING_CONFLICT",
    "SAFETY_BLOCK", "DEPENDENCY_FAILED", "SCHEMA_INVALID",
]

HANDOFF_REQUIRED_TOP = [
    "schema_version", "request_id", "parent_task_id", "task_id", "from_assistant",
    "from_version", "to_assistant", "intent", "input_summary", "required_context",
    "output", "safety", "execution",
]
HANDOFF_REQUIRED_OUTPUT = ["data", "conclusions", "uncertainties", "missing_information",
                           "warnings", "sources"]
HANDOFF_REQUIRED_SAFETY = ["status", "flags"]
HANDOFF_REQUIRED_EXEC = ["status", "confidence", "timestamp"]

# تصنيف تقريبي — proxy آلي لا يغني عن حكم clinical-firewall الحي.
EMERGENCY_RE = re.compile(r"نزيف|تورم|ألم شديد|رضّ|ارتفاع حرارة")
CLINICAL_MARKERS_RE = re.compile(
    r"يناسب(ني)?|أنا بالضبط|لي أنا|مسكن|جرعة|دواء|الأشعة|أشعتي|بالضبط.*جلس|جلس.*بالضبط|"
    r"شدة الألم اللي راح أحسه"
)
IN_SCOPE_MARKERS_RE = re.compile(r"كم سعر|كم مدة|الفرق بين|مواعيد|كيف أحجز")


def classify_safety(phrase):
    if EMERGENCY_RE.search(phrase):
        return "EMERGENCY"
    clinical = bool(CLINICAL_MARKERS_RE.search(phrase))
    in_scope = bool(IN_SCOPE_MARKERS_RE.search(phrase))
    if clinical and in_scope:
        return "COMPOUND"
    if clinical:
        return "CLINICAL_INTENT"
    if in_scope:
        return "IN_SCOPE"
    return "UNKNOWN"


def load_assistants(skills_root):
    assistants = {}
    for d in discover_skill_dirs(skills_root):
        rec = load_skill(d)
        if rec["frontmatter_ok"] and rec["meta"].get("assistant_id"):
            meta = dict(rec["meta"])
            meta["_assume_tested"] = True  # فحص منطق التنسيق لا قفل الاختبار
            assistants[rec["meta"]["assistant_id"]] = meta
    return assistants


def parse_trace(trace):
    out = []
    for t in trace:
        try:
            aid, rest = t.split(":", 1)
            score = float(rest.split("/", 1)[0])
            out.append((aid, score))
        except ValueError:
            continue
    return out


def run_single_vs_multi(case, assistants):
    got, reason, trace = route(case["request"], assistants)
    candidates = parse_trace(trace)
    strong = [c for c in candidates if c[1] >= 0.6]
    mode = "SINGLE" if len(strong) == 1 else "MULTI"
    ok = mode == case["expect_mode"]
    if ok and mode == "SINGLE" and "expect_assistant" in case:
        ok = strong[0][0] == case["expect_assistant"]
    detail = f"mode={mode} got={got} candidates={candidates}"
    return ok, detail


def run_dependency_order(case, assistants):
    subset = set(case["assistants"])
    edges = {a: set() for a in subset}
    for aid in subset:
        meta = assistants.get(aid, {})
        for b in as_list(meta.get("can_delegate_to")):
            if b in subset:
                edges.setdefault(aid, set()).add(b)
        for c in as_list(meta.get("skill_dependencies")):
            if c in subset:
                edges.setdefault(c, set()).add(aid)

    def reachable(start, end):
        seen, stack = set(), [start]
        while stack:
            n = stack.pop()
            if n == end:
                return True
            if n in seen:
                continue
            seen.add(n)
            stack.extend(edges.get(n, []))
        return False

    missing = [p for p in case["expect_before"]
               if not reachable(p["before"], p["after"])]
    ok = not missing
    return ok, f"edges={edges} missing_pairs={missing}"


def run_target_exists(case, assistants):
    aid = case["assistant"]
    meta = assistants.get(aid)
    routable_like = meta and meta.get("status") in ("ACTIVE", "TESTING", "PILOT")
    got = "OK" if routable_like else "BLOCKED"
    return got == case["expect"], f"got={got}"


def run_circular_detection(case, assistants):
    if "graph" in case:
        graph = case["graph"]
    elif "graph_from_metadata" in case:
        # يبني الرسم الحقيقي الكامل من can_delegate_to (نفس منطق validate_system.py)
        known = set(assistants)
        graph = {k: [t for t in as_list(v.get("can_delegate_to")) if t in known]
                 for k, v in assistants.items()}
    else:
        return False, "no graph source"
    cycles = detect_circular(graph)
    got = "CIRCULAR" if cycles else "NO_CYCLE"
    return got == case["expect"], f"got={got} cycles={cycles}"


def run_legacy_alias(case, assistants):
    resolved = None
    for aid, meta in assistants.items():
        if case["old_id"] in as_list(meta.get("legacy_aliases")):
            resolved = aid
            break
    return resolved == case["expect_canonical"], f"resolved={resolved}"


def run_schema_check(case, handoff_schema_meta):
    h = case["handoff"]
    problems = []
    for k in HANDOFF_REQUIRED_TOP:
        if k not in h:
            problems.append(f"missing top-level: {k}")
    for k in HANDOFF_REQUIRED_OUTPUT:
        if k not in (h.get("output") or {}):
            problems.append(f"missing output.{k}")
    for k in HANDOFF_REQUIRED_SAFETY:
        if k not in (h.get("safety") or {}):
            problems.append(f"missing safety.{k}")
    for k in HANDOFF_REQUIRED_EXEC:
        if k not in (h.get("execution") or {}):
            problems.append(f"missing execution.{k}")

    exec_status = (h.get("execution") or {}).get("status")
    if exec_status not in STATUS_CODES:
        problems.append(f"execution.status غير معروف: {exec_status}")

    safety_status = (h.get("safety") or {}).get("status")
    if safety_status == "SAFETY_BLOCK" and exec_status != "SAFETY_BLOCK":
        problems.append("safety.status=SAFETY_BLOCK يستلزم execution.status=SAFETY_BLOCK")

    if handoff_schema_meta:
        want = str(handoff_schema_meta.get("schema_version"))
        got = str(h.get("schema_version"))
        if got != want:
            problems.append(f"schema_version {got} ≠ {want}")

    got_verdict = "SCHEMA_INVALID" if problems else "VALID"
    return got_verdict == case["expect"], f"got={got_verdict} problems={problems}"


def run_safety_classify(case):
    got = classify_safety(case["phrase"])
    ok = got == case["expect"]
    return ok, f"got={got}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skills", required=True)
    ap.add_argument("--orchestration", default="governance/evals/orchestration-golden-set.yaml")
    ap.add_argument("--handoff", default="governance/evals/handoff-golden-set.yaml")
    ap.add_argument("--safety", default="governance/evals/safety-golden-set.yaml")
    ap.add_argument("--edge-cases", default="governance/evals/edge-cases.yaml")
    ap.add_argument("--handoff-schema", default="governance/handoff-schema.yaml")
    ap.add_argument("--json")
    args = ap.parse_args()

    assistants = load_assistants(Path(args.skills).expanduser().resolve())

    handoff_schema_meta = None
    if Path(args.handoff_schema).is_file():
        handoff_schema_meta = (yaml.safe_load(
            Path(args.handoff_schema).read_text(encoding="utf-8")) or {}).get("meta")

    results = []

    def load_cases(path):
        p = Path(path)
        if not p.is_file():
            return []
        return (yaml.safe_load(p.read_text(encoding="utf-8")) or {}).get("cases") or []

    for path in (args.orchestration, args.edge_cases):
        for case in load_cases(path):
            ctype = case.get("type")
            if ctype == "single_vs_multi":
                ok, detail = run_single_vs_multi(case, assistants)
            elif ctype == "dependency_order":
                ok, detail = run_dependency_order(case, assistants)
            elif ctype == "target_exists":
                ok, detail = run_target_exists(case, assistants)
            elif ctype == "circular_detection":
                ok, detail = run_circular_detection(case, assistants)
            elif ctype == "legacy_alias":
                ok, detail = run_legacy_alias(case, assistants)
            else:
                ok, detail = None, f"نوع '{ctype}' يحتاج تشغيلة حية — لا فحص آلي هنا"
            results.append({"suite": Path(path).stem, "id": case.get("id"),
                             "type": ctype, "ok": ok, "detail": detail})

    for case in load_cases(args.handoff):
        ok, detail = run_schema_check(case, handoff_schema_meta)
        results.append({"suite": "handoff-golden-set", "id": case.get("id"),
                         "type": "schema_check", "ok": ok, "detail": detail})

    for case in load_cases(args.safety):
        ok, detail = run_safety_classify(case)
        results.append({"suite": "safety-golden-set", "id": case.get("id"),
                         "type": "safety_classify", "ok": ok, "detail": detail})

    checked = [r for r in results if r["ok"] is not None]
    passed = sum(1 for r in checked if r["ok"])
    skipped = [r for r in results if r["ok"] is None]

    print("\nاختبارات التنسيق\n" + "═" * 74)
    for r in results:
        mark = "SKIP" if r["ok"] is None else ("PASS" if r["ok"] else "FAIL")
        print(f"  {mark}  [{r['suite']}] {r['id']}")
        if r["ok"] is False:
            print(f"        {r['detail']}")
    print("═" * 74)
    print(f"النتيجة: {passed}/{len(checked)} ناجح · {len(checked) - passed} فاشل · "
          f"{len(skipped)} يحتاج تشغيلة حية\n")

    if args.json:
        Path(args.json).write_text(json.dumps(
            {"total": len(checked), "passed": passed, "failed": len(checked) - passed,
             "skipped_needs_live_run": len(skipped), "results": results},
            ensure_ascii=False, indent=2), encoding="utf-8")

    return 1 if passed < len(checked) else 0


if __name__ == "__main__":
    sys.exit(main())
