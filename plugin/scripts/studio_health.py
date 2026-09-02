#!/usr/bin/env python3
"""تقرير صحة الاستوديو — يجمع نتيجة كل بوابات release-policy.md في تقرير واحد.

الاستخدام:
    python3 studio_health.py --root <جذر assistant-studio> [--json <ملف>]

يشغّل validate_system.py، routing_tests.py، orchestration_tests.py،
dependency_graph.py، build_knowledge_index.py كعمليات فرعية (نفس ما يشغّله
مطوّر بشري يدوياً) ويجمّع خلاصة واحدة. لا يُصلح شيئاً بنفسه — قراءة فقط.
"""

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib_studio import LIFECYCLE, discover_skill_dirs, load_skill  # noqa: E402


def run(cmd, cwd=None):
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    return p.returncode, p.stdout, p.stderr


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--json")
    args = ap.parse_args()

    root = Path(args.root).expanduser().resolve()
    py = sys.executable
    scripts = root / "scripts"

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)

        # ── ١. فحص النظام ────────────────────────────────────────────────
        rc_v, _, _ = run([py, str(scripts / "validate_system.py"),
                           "--skills", str(root / "skills"),
                           "--policy", str(root / "identity/house-rules.md"),
                           "--policy", str(root / "identity/clinical-firewall.md"),
                           "--json", str(tmp / "validate.json")])
        validate = json.loads((tmp / "validate.json").read_text(encoding="utf-8"))

        # ── ٢. اختبارات التوجيه (حقيقية — بلا assume-tested) ────────────
        rc_r, _, _ = run([py, str(scripts / "routing_tests.py"),
                           "--skills", str(root / "skills"),
                           "--tests", str(root / "governance/routing-tests.yaml"),
                           "--json", str(tmp / "routing.json")])
        routing = json.loads((tmp / "routing.json").read_text(encoding="utf-8"))

        # ── ٣. اختبارات التنسيق ─────────────────────────────────────────
        rc_o, out_o, err_o = run([py, str(scripts / "orchestration_tests.py"),
                                   "--skills", str(root / "skills"),
                                   "--orchestration", str(root / "governance/evals/orchestration-golden-set.yaml"),
                                   "--handoff", str(root / "governance/evals/handoff-golden-set.yaml"),
                                   "--safety", str(root / "governance/evals/safety-golden-set.yaml"),
                                   "--edge-cases", str(root / "governance/evals/edge-cases.yaml"),
                                   "--handoff-schema", str(root / "governance/handoff-schema.yaml"),
                                   "--json", str(tmp / "orch.json")])
        if not (tmp / "orch.json").is_file():
            sys.stderr.write(f"orchestration_tests.py فشل (rc={rc_o}):\n{out_o}\n{err_o}\n")
            return 2
        orch = json.loads((tmp / "orch.json").read_text(encoding="utf-8"))

        # ── ٤. رسم الاعتماديات ──────────────────────────────────────────
        rc_d, _, _ = run([py, str(scripts / "dependency_graph.py"),
                           "--skills", str(root / "skills"),
                           "--json", str(tmp / "dep.json")])
        dep = json.loads((tmp / "dep.json").read_text(encoding="utf-8"))

        # ── ٥. انحراف الدليل — registry drift ───────────────────────────
        rc_reg, _, _ = run([py, str(scripts / "build_registry.py"),
                             "--skills", str(root / "skills"),
                             "--out", str(tmp / "registry.md"),
                             "--deferred", str(root / "governance/migration-spec.yaml"),
                             "--generated-on", "DRIFT_CHECK"])
        current_registry = root / "knowledge/assistants-registry.md"
        fresh = (tmp / "registry.md").read_text(encoding="utf-8")
        existing = current_registry.read_text(encoding="utf-8") if current_registry.is_file() else ""
        # يتجاهل سطر "تاريخ التوليد" وحده عند المقارنة — التوليد نفسه لا التاريخ هو المقياس
        def strip_date_line(t):
            return "\n".join(ln for ln in t.splitlines() if "تاريخ التوليد" not in ln)
        registry_drift = 0 if strip_date_line(fresh) == strip_date_line(existing) else 1

        # ── ٦. فهرس المعرفة ──────────────────────────────────────────────
        rc_k, _, _ = run([py, str(scripts / "build_knowledge_index.py"),
                           "--knowledge-root", str(root / "knowledge"),
                           "--out", str(tmp / "kindex.md"),
                           "--json", str(tmp / "kindex.json")])
        kindex = json.loads((tmp / "kindex.json").read_text(encoding="utf-8"))
        missing_knowledge = sum(1 for e in kindex["entries"] if e.get("status") != "ACTIVE")
        current_generated = root / "knowledge/generated-index.md"
        fresh_k = (tmp / "kindex.md").read_text(encoding="utf-8")
        existing_k = current_generated.read_text(encoding="utf-8") if current_generated.is_file() else ""
        kindex_drift = 0 if fresh_k.strip() == existing_k.strip() else 1

        # ── ٧. عدّاد الحالات ─────────────────────────────────────────────
        counts = {st: 0 for st in LIFECYCLE}
        for d in discover_skill_dirs(root / "skills"):
            rec = load_skill(d)
            if rec["frontmatter_ok"]:
                st = rec["meta"].get("status")
                if st in counts:
                    counts[st] += 1

        broken_deps = dep["counts"]["broken"]
        circular_deps = dep["counts"]["cycles"]
        orphan_skills = sum(1 for c in validate.get("warnings", []) if c["check"] == "orphan_assistant")

        safety_pass = not any(
            c in validate.get("checks", {}) and validate["checks"][c] == "FAIL"
            for c in ("safety_body_sections", "safety_level_vocabulary", "policy_inheritance",
                       "global_policy_present", "global_policy_override", "domain_out_of_scope"))

        routing_pass = routing.get("failed", 1) == 0
        orch_pass = orch.get("failed", 1) == 0
        registry_ok = rc_reg == 0
        knowledge_ok = rc_k == 0

        blockers = []
        if rc_v != 0:
            blockers.append("validate_system: أخطاء بنيوية")
        if not routing_pass:
            blockers.append("routing_tests: فشل توجيه")
        if not orch_pass:
            blockers.append("orchestration_tests: فشل تنسيق")
        if not safety_pass:
            blockers.append("فحوص سلامة/سياسة فاشلة")
        if broken_deps:
            blockers.append(f"{broken_deps} مرجع اعتمادية مكسور")
        if circular_deps:
            blockers.append(f"{circular_deps} دورة تفويض")

        status = "READY_FOR_BUILD" if not blockers else "PARTIALLY_READY"

        report = {
            "active_assistants": counts.get("ACTIVE", 0),
            "testing": counts.get("TESTING", 0),
            "pilot": counts.get("PILOT", 0),
            "deprecated": counts.get("DEPRECATED", 0),
            "archived": counts.get("ARCHIVED", 0),
            "routing_tests": "PASS" if routing_pass else "FAIL",
            "orchestration_tests": "PASS" if orch_pass else "FAIL",
            "safety_tests": "PASS" if safety_pass else "FAIL",
            "regression": "PASS" if routing_pass else "FAIL",  # نفس ملف الحالات = خط الأساس
            "broken_dependencies": broken_deps,
            "circular_dependencies": circular_deps,
            "missing_knowledge": missing_knowledge,
            "orphan_skills": orphan_skills,
            "registry_drift": registry_drift,
            "knowledge_index_drift": kindex_drift,
            "studio_status": status,
            "blockers": blockers,
        }

    print("Assistant Studio Health")
    print(f"Active assistants: {report['active_assistants']}")
    print(f"Testing: {report['testing']}")
    print(f"Pilot: {report['pilot']}")
    print(f"Deprecated: {report['deprecated']}")
    print(f"Archived: {report['archived']}")
    print(f"Routing tests: {report['routing_tests']}")
    print(f"Orchestration tests: {report['orchestration_tests']}")
    print(f"Safety tests: {report['safety_tests']}")
    print(f"Regression: {report['regression']}")
    print(f"Broken dependencies: {report['broken_dependencies']}")
    print(f"Circular dependencies: {report['circular_dependencies']}")
    print(f"Missing knowledge: {report['missing_knowledge']}")
    print(f"Orphan skills: {report['orphan_skills']}")
    print(f"Registry drift: {report['registry_drift']}")
    print(f"Knowledge index drift: {report['knowledge_index_drift']}")
    print(f"Studio status: {report['studio_status']}")
    if report["blockers"]:
        print("Blockers:")
        for b in report["blockers"]:
            print(f"  - {b}")

    if args.json:
        Path(args.json).write_text(json.dumps(report, ensure_ascii=False, indent=2),
                                    encoding="utf-8")

    return 0 if status == "READY_FOR_BUILD" else 1


if __name__ == "__main__":
    sys.exit(main())
