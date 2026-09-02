#!/usr/bin/env python3
"""اختبارات الاستقلالية — Standalone Test Suite (v1.4.0)

يحاكي مستخدماً جديداً استلم Assistant-Studio-v1.4.0-Marketing-OS-Standalone.zip فقط:
بلا أي Skill أو Assistant أو Project أو ملف معرفة أو API خاص بحساب المُنشئ
الأصلي. كل اختبار هنا فحص حتمي على مستوى الـ metadata والملفات — مطابق في
الروح لـ scripts/validate_system.py و scripts/routing_tests.py، ولا يغني عن
تشغيلة حية، لكنه يمنع انحداراً حقيقياً قبل وصوله للمستخدم.

الاستخدام:
    python3 tests/standalone/test_standalone.py --skills skills [--json out.json]

يعيد 0 عند نجاح كل الاختبارات الستة، 1 عند أي فشل.
"""

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))
from lib_studio import (  # noqa: E402
    OUT_OF_SCOPE_DOMAINS, GLOBAL_POLICY_IDS, as_list, discover_skill_dirs, load_skill,
)

import importlib.util  # noqa: E402


def _load_routing_engine(scripts_dir: Path):
    spec = importlib.util.spec_from_file_location("routing_tests", scripts_dir / "routing_tests.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_assistants(skills_root: Path):
    assistants = {}
    for d in discover_skill_dirs(skills_root):
        rec = load_skill(d)
        if rec["frontmatter_ok"] and rec["meta"].get("assistant_id"):
            assistants[rec["meta"]["assistant_id"]] = rec
    return assistants


def test_1_zero_external_assistants(assistants):
    """Test 1 — Install with zero external assistants. Expected: PASS.

    كل route_to و can_delegate_to في كل مساعد يجب أن يشير إلى assistant_id
    موجود فعلياً داخل هذه الحزمة — لا مساعد خارجي مطلوب لتشغيل أي قدرة أساسية.
    """
    known = set(assistants)
    unresolved = []
    for aid, rec in assistants.items():
        meta = rec["meta"]
        for n in meta.get("negative_triggers") or []:
            if isinstance(n, dict) and n.get("route_to") and n["route_to"] not in known:
                unresolved.append(f"{aid}.negative_triggers.route_to → {n['route_to']}")
        for target in as_list(meta.get("can_delegate_to")):
            if target not in known:
                unresolved.append(f"{aid}.can_delegate_to → {target}")
    ok = not unresolved
    detail = "0 مراجع assistant خارجية" if ok else "؛ ".join(unresolved)
    return ok, detail


def test_2_zero_external_skills(assistants):
    """Test 2 — Install with zero external Skills. Expected: PASS.

    كل skill_dependencies يجب أن يشير إلى Skill موجودة فعلياً داخل هذه الحزمة.
    """
    known = set(assistants)
    unresolved = []
    for aid, rec in assistants.items():
        for target in as_list(rec["meta"].get("skill_dependencies")):
            if target not in known:
                unresolved.append(f"{aid}.skill_dependencies → {target}")
    ok = not unresolved
    detail = "0 مراجع Skill خارجية" if ok else "؛ ".join(unresolved)
    return ok, detail


def test_3_no_whatsapp_manual_mode(assistants):
    """Test 3 — No WhatsApp integration. System uses manual mode. Expected: PASS.

    (أ) content-whatsapp-lead-responder توثّق مساراً يدوياً صريحاً عند غياب ChatPlace.
    (ب) لا مساعد يجعل chatplace/whatsapp مدخلاً *مطلوباً* (required_inputs) —
        يجب أن يبقى اختيارياً (tool_dependencies) في كل مكان.
    """
    problems = []
    rec = assistants.get("content-whatsapp-lead-responder")
    if not rec:
        return False, "content-whatsapp-lead-responder غير موجودة"
    body = rec["body"]
    manual_markers = ["لم يتوفر ChatPlace", "Manual Execution Mode", "جاهز للنسخ اليدوي"]
    if not any(m in body for m in manual_markers):
        problems.append("لا مسار يدوي صريح موثَّق في جسم content-whatsapp-lead-responder")

    chatplace_re = re.compile(r"chatplace|whatsapp|واتساب", re.IGNORECASE)
    for aid, r in assistants.items():
        for inp in as_list(r["meta"].get("required_inputs")):
            if chatplace_re.search(str(inp)):
                problems.append(f"{aid}.required_inputs يفترض ChatPlace/WhatsApp كمطلوب: {inp}")

    ok = not problems
    detail = "مسار يدوي موثَّق، لا اعتماد إلزامي على ChatPlace" if ok else "؛ ".join(problems)
    return ok, detail


def test_4_no_marketing_assistant(assistants, engine):
    """Test 4 — No marketing assistant. Internal marketing Skill handles task. Expected: PASS."""
    if "marketing-strategy-planner" not in assistants:
        return False, "marketing-strategy-planner غير موجودة"
    if assistants["marketing-strategy-planner"]["meta"].get("status") != "ACTIVE":
        return False, "marketing-strategy-planner ليست ACTIVE"
    raw = {aid: r["meta"] for aid, r in assistants.items()}
    phrase = "أنشئ خطة تسويقية كاملة"
    got, reason, _ = engine.route(phrase, raw)
    ok = got == "marketing-strategy-planner"
    return ok, f"«{phrase}» → {got} ({reason})"


def test_5_no_social_media_assistant(assistants, engine):
    """Test 5 — No social media assistant. Internal Skill handles it. Expected: PASS."""
    if "content-social-calendar-scheduler" not in assistants:
        return False, "content-social-calendar-scheduler غير موجودة"
    if assistants["content-social-calendar-scheduler"]["meta"].get("status") != "ACTIVE":
        return False, "content-social-calendar-scheduler ليست ACTIVE"
    raw = {aid: r["meta"] for aid, r in assistants.items()}
    phrase = "أنشئ تقويم محتوى أسبوعي"
    got, reason, _ = engine.route(phrase, raw)
    ok = got == "content-social-calendar-scheduler"
    return ok, f"«{phrase}» → {got} ({reason})"


def test_6_clinical_request_blocked(assistants, engine):
    """Test 6 — Clinical request. Clinical Firewall blocks it. Expected: PASS.

    ثلاثة أدلة متقاربة لا دليل واحد:
    (أ) صفر مساعد بمجال clinical/patient/research يمكنه الوجود أصلاً في هذه
        الحزمة (domain_out_of_scope، مفروض بنيوياً — governance/scope-boundary.md).
    (ب) كل مساعد يحمل clinical-firewall ضمن policy_dependencies إلزامياً
        (GLOBAL_POLICY، override_allowed: false).
    (ج) طلب سريري فعلي ("ما علاج هذا المريض؟") لا يطابق trigger لأي مساعد —
        القرار السريري خارج نطاق التوجيه العادي كلياً، ويُحال عبر
        identity/clinical-firewall.md لا عبر أي Skill.
    """
    problems = []
    for aid, r in assistants.items():
        if r["meta"].get("domain") in OUT_OF_SCOPE_DOMAINS:
            problems.append(f"{aid} بمجال ممنوع: {r['meta'].get('domain')}")
        pdeps = set(as_list(r["meta"].get("policy_dependencies")))
        if not set(GLOBAL_POLICY_IDS).issubset(pdeps):
            problems.append(f"{aid} لا يرث كل GLOBAL_POLICY: {pdeps}")

    raw = {aid: r["meta"] for aid, r in assistants.items()}
    phrase = "ما علاج هذا المريض؟"
    got, reason, _ = engine.route(phrase, raw)
    if got not in ("NO_MATCH",) and not str(got).startswith("EXTERNAL:"):
        problems.append(f"«{phrase}» طابقت مساعداً غير سريري مباشرة: {got} ({reason}) — "
                         "يجب أن تُحجب عبر clinical-firewall قبل أي توجيه")

    ok = not problems
    detail = (f"0 مساعد بمجال ممنوع، {len(assistants)}/{len(assistants)} يرث clinical-firewall إلزامياً، "
              f"الطلب السريري لا يطابق أي Skill مباشرة ({got})") if ok else "؛ ".join(problems)
    return ok, detail


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skills", required=True)
    ap.add_argument("--json")
    args = ap.parse_args()

    root = Path(args.skills).expanduser().resolve()
    scripts_dir = Path(__file__).resolve().parent.parent.parent / "scripts"
    engine = _load_routing_engine(scripts_dir)
    assistants = load_assistants(root)

    tests = [
        ("Test 1 — Install with zero external assistants", lambda: test_1_zero_external_assistants(assistants)),
        ("Test 2 — Install with zero external Skills", lambda: test_2_zero_external_skills(assistants)),
        ("Test 3 — No WhatsApp integration → manual mode", lambda: test_3_no_whatsapp_manual_mode(assistants)),
        ("Test 4 — No marketing assistant → internal Skill handles it",
         lambda: test_4_no_marketing_assistant(assistants, engine)),
        ("Test 5 — No social media assistant → internal Skill handles it",
         lambda: test_5_no_social_media_assistant(assistants, engine)),
        ("Test 6 — Clinical request → Clinical Firewall blocks it",
         lambda: test_6_clinical_request_blocked(assistants, engine)),
    ]

    print("\nاختبارات الاستقلالية — Standalone Test Suite\n" + "═" * 74)
    results, failed = [], 0
    for name, fn in tests:
        ok, detail = fn()
        mark = "PASS" if ok else "FAIL"
        if not ok:
            failed += 1
        print(f"  {mark}  {name}")
        print(f"        {detail}")
        results.append({"name": name, "ok": ok, "detail": detail})
    print("═" * 74)
    print(f"النتيجة: {len(tests) - failed}/{len(tests)} ناجح · {failed} فاشل\n")

    if args.json:
        Path(args.json).write_text(json.dumps(
            {"total": len(tests), "passed": len(tests) - failed, "failed": failed,
             "results": results}, ensure_ascii=False, indent=2), encoding="utf-8")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
