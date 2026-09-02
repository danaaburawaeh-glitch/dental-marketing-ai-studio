#!/usr/bin/env python3
"""ماسح الاعتماديات — Dependency Scanner (v1.3.0 Standalone)

يبحث في كامل الحزمة عن: أسماء مساعدين/Skills خارج الحزمة، مسارات مطلقة،
معرّفات حساب شخصية، روابط خاصة، أسرار/مفاتيح API صريحة. هذا هو الفحص الآلي
الذي يثبت — لا يفترض — أن `Required unresolved dependencies: 0`.

الاستخدام:
    python3 tests/dependency-scan.py --root . [--json out.json]

يعيد 0 عند صفر اعتماديات Required غير محلولة، 1 عند أي وجود.
ملاحظات (مثل حقول migration-spec.yaml التاريخية الموثَّقة كاستثناء صريح في
governance/portability.md) تُبلَّغ منفصلة ولا تُحسَب ضمن العدد الحاسم.
"""

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from lib_studio import as_list, discover_skill_dirs, load_skill  # noqa: E402

# ── أنماط الفحص ──────────────────────────────────────────────────────────────

ABS_PATH_RE = re.compile(r"(?:/home/[a-zA-Z0-9_.\-]+|/Users/[a-zA-Z0-9_.\-]+|/root/[a-zA-Z0-9_.\-]*|[A-Za-z]:\\\\[A-Za-z0-9_.\-\\\\]+)")
SECRET_RE = re.compile(
    r"api[_-]?key\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{8,}|"
    r"secret\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{8,}|"
    r"\btoken\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{12,}|"
    r"Bearer [A-Za-z0-9_\-\.]{10,}|"
    r"sk-[A-Za-z0-9]{16,}",
    re.IGNORECASE,
)
PERSONAL_NAME_RE = re.compile(r"دانا|Dana\b|أبورواعه|Aburawaeh", re.IGNORECASE)
OWNER_PERSONAL_RE = re.compile(r"^\s*owner:\s*(?!clinic-owner\b)([a-zA-Z؀-ۿ][\w؀-ۿ-]*)\s*$",
                                re.MULTILINE)
PRIVATE_URL_RE = re.compile(r"instagram\.com/[a-zA-Z0-9_.]{3,}|wa\.me/\d{6,}|\+9665\d{8}")

# مسارات مستثناة صراحة — موثَّقة في governance/portability.md § الاستثناءات الموثَّقة.
# كل استثناء هنا مذكور بنفس الاسم وبنفس السبب في ذلك الجدول — لا استثناء صامت.
DOCUMENTED_EXCEPTIONS = {
    "governance/migration-spec.yaml",  # حقول source: التاريخية — provenance جامد
    "DEPENDENCIES.md",                  # يوثّق أسماء المشكلات المكتشفة والمُصلَحة عمداً
    "RELEASE-AUDIT-v1.3.0.md",          # تقرير تدقيق الإصدار — نفس منطق DEPENDENCIES.md بالضبط
    "governance/assistant-id-migration-map.md",   # سجل ترحيل تاريخي — Type D، لا مرجع تشغيلي
    "README.md",                                   # سجل تغييرات تاريخي (changelog) — سرد ماضٍ لما أُصلح
    "CHANGELOG.md",                                 # نفس المنطق — سجل إصدارات رسمي، يوثّق الإصلاح لا يعتمد عليه
    "governance/evals/exclusions-golden-set.yaml",  # يثبت EXTERNAL:... أي أن الموجّه يُقصيها فعلاً
    "governance/evals/regression-baseline.yaml",    # نفس المنطق — حالتان معروفتان موثَّقتان في رأس الملف
    "tests/dependency-scan.py",       # نص الأنماط نفسه (بادئات مسارات الجذر) جزء من تعريف الفحص لا بيانات مسرَّبة
    "governance/foundation-validation-report.md",   # تقرير تدقيق تاريخي (2026-08-21) — لا تُمَسّ محتواه
    "governance/proposals/2026-08-28-standalone-external-reference-removal.md",  # ACP يوثّق الإصلاح نفسه
    "governance/routing-tests.yaml",   # تعليقات توضيحية على حالات R4 — لا تؤثر في منطق التوجيه
    "knowledge/assistants-registry.md",  # مُولَّد آلياً من migration-spec.yaml § deferred — انظر ذلك الملف
    "governance/portability.md",       # هذا الملف نفسه — جدول الاستثناءات الموثَّقة يذكر الأسماء كأمثلة
    "scripts/inventory.py",  # نمط رصد أسماء شخصية (LEGACY_PATTERNS) — يحمل النص المرصود في تعريفه، تماماً كهذا الماسح
    "skills/system-update-checker/SKILL.md",  # رابط مستودع التوزيع العام للمنتج — موثّق في portability.md
    "scripts/check_update.py",  # نفس نقطة التوزيع العامة؛ لا بيانات مستخدم ولا سر
}


def scan_text_patterns(root: Path):
    """يفحص كل ملف نصي في الحزمة عن مسارات مطلقة/أسرار/أسماء شخصية/روابط خاصة."""
    findings = {"absolute_paths": [], "secrets": [], "personal_names": [],
                "personal_owner_fields": [], "private_urls": []}
    text_exts = {".md", ".yaml", ".yml", ".json", ".py"}
    for p in sorted(root.rglob("*")):
        if not p.is_file() or p.suffix not in text_exts:
            continue
        rel = str(p.relative_to(root))
        if rel.startswith(".git/"):
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        documented = rel in DOCUMENTED_EXCEPTIONS

        # الاستثناء يغطي فقط ما هو موثَّق فعلاً في governance/portability.md: مسارات مطلقة
        # (نص أنماط الماسح نفسه) وأسماء شخصية في سجل تاريخي/بيانات اختبار إقصاء. لا يُعفى
        # أي ملف — موثَّقاً أو لا — من فحص الأسرار/حقول owner/الروابط الخاصة.
        if not documented:
            for m in ABS_PATH_RE.finditer(text):
                findings["absolute_paths"].append(f"{rel}: {m.group(0)}")
            for m in PERSONAL_NAME_RE.finditer(text):
                findings["personal_names"].append(f"{rel}: «{m.group(0)}»")
        for m in SECRET_RE.finditer(text):
            findings["secrets"].append(f"{rel}: {m.group(0)[:40]}…")
        for m in OWNER_PERSONAL_RE.finditer(text):
            findings["personal_owner_fields"].append(f"{rel}: owner: {m.group(1)}")
        for m in PRIVATE_URL_RE.finditer(text):
            findings["private_urls"].append(f"{rel}: {m.group(0)}")
    return findings


def scan_metadata_references(skills_root: Path):
    """يفحص كل SKILL.md عن route_to/can_delegate_to/skill_dependencies غير محلولة داخلياً."""
    assistants = {}
    for d in discover_skill_dirs(skills_root):
        rec = load_skill(d)
        if rec["frontmatter_ok"] and rec["meta"].get("assistant_id"):
            assistants[rec["meta"]["assistant_id"]] = rec

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
        for target in as_list(meta.get("skill_dependencies")):
            if target not in known:
                unresolved.append(f"{aid}.skill_dependencies → {target}")
    return unresolved, len(assistants)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--json")
    args = ap.parse_args()

    root = Path(args.root).expanduser().resolve()
    skills_root = root / "skills"

    unresolved_refs, n_assistants = scan_metadata_references(skills_root)
    text_findings = scan_text_patterns(root)

    print("\nماسح الاعتماديات — Dependency Scanner\n" + "═" * 74)
    print(f"مساعدون مفحوصون: {n_assistants}")
    print()

    def report(label, items, critical):
        mark = "PASS" if not items else ("FAIL" if critical else "WARN")
        print(f"  {mark}  {label}: {len(items)}")
        for it in items[:20]:
            print(f"        - {it}")
        if len(items) > 20:
            print(f"        … و{len(items) - 20} إضافية")

    report("مراجع route_to/can_delegate_to/skill_dependencies غير محلولة داخلياً", unresolved_refs, critical=True)
    report("مسارات مطلقة خارج الاستثناءات الموثَّقة", text_findings["absolute_paths"], critical=True)
    report("أسرار/مفاتيح API صريحة", text_findings["secrets"], critical=True)
    report("أسماء شخصية (دانا/Dana/أبورواعه) خارج الاستثناءات الموثَّقة", text_findings["personal_names"], critical=True)
    report("حقول owner: تحمل اسماً شخصياً بدل دور عام", text_findings["personal_owner_fields"], critical=True)
    report("روابط خاصة (Instagram/WhatsApp حقيقية)", text_findings["private_urls"], critical=True)

    required_unresolved = (len(unresolved_refs) + len(text_findings["absolute_paths"])
                            + len(text_findings["secrets"]) + len(text_findings["personal_names"])
                            + len(text_findings["personal_owner_fields"]) + len(text_findings["private_urls"]))

    print("═" * 74)
    print(f"Required unresolved dependencies: {required_unresolved}\n")

    if args.json:
        Path(args.json).write_text(json.dumps(
            {"assistants_scanned": n_assistants,
             "unresolved_metadata_references": unresolved_refs,
             "text_findings": text_findings,
             "required_unresolved_dependencies": required_unresolved},
            ensure_ascii=False, indent=2), encoding="utf-8")

    return 1 if required_unresolved else 0


if __name__ == "__main__":
    sys.exit(main())
