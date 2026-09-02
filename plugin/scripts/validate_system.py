#!/usr/bin/env python3
"""فاحص النظام الكامل — يفشل البناء عند أي خرق للحوكمة.

الاستخدام:
    python3 validate_system.py --skills <مجلد>
                               [--policy <ملف>]...
                               [--knowledge-root <مجلد>] [--json <ملف>]

--policy يُكرَّر لكل ملف GLOBAL_POLICY (افتراضياً identity/house-rules.md
و identity/clinical-firewall.md إن لم يُمرَّر شيء). كلاهما بنفس المرتبة؛
غياب أيّهما = فشل global_policy_present.

يطبّق فحوص المخطط ودورة الحياة والإصدارات والمراجع والتوجيه والسياسة العامة
والنطاق (domain_out_of_scope)، ويكشف التداخل بين المساعدين. الخروج بـ 1 عند أي خطأ.
"""

import argparse
import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent))
from lib_studio import (  # noqa: E402
    DOMAINS, GLOBAL_POLICY_IDS, ID_RE, KNOWN_POLICY_IDS, LIFECYCLE,
    OUT_OF_SCOPE_DOMAINS, REQUIRED_FIELDS, ROUTABLE, SAFETY_LEVELS,
    SEMVER_RE, as_list, detect_circular, discover_skill_dirs, jaccard,
    load_skill, overlap_band, parse_frontmatter, token_set,
)

DEFAULT_POLICY_PATHS = [
    "identity/house-rules.md",
    "identity/clinical-firewall.md",
]

DEFAULT_HANDOFF_SCHEMA = "governance/handoff-schema.yaml"

SAFETY_BODY_MARKERS = ["السلامة", "الحدود", "خصوصية", "PDPL", "موافقة"]


class Report:
    def __init__(self):
        self.errors, self.warnings, self.checks = [], [], {}

    def err(self, check, msg):
        self.errors.append((check, msg))
        self.checks.setdefault(check, "FAIL")
        self.checks[check] = "FAIL"

    def warn(self, check, msg):
        self.warnings.append((check, msg))
        self.checks.setdefault(check, "PASS")

    def ok(self, check):
        self.checks.setdefault(check, "PASS")


def load_all(skills_root: Path):
    items = {}
    problems = []
    for d in discover_skill_dirs(skills_root):
        rec = load_skill(d)
        ident = rec["name"] or d.name
        if not rec["frontmatter_ok"]:
            problems.append((ident, rec["parse_error"]))
            continue
        items.setdefault(ident, []).append(rec)
    return items, problems


def validate(skills_root, policy_paths, knowledge_root, handoff_schema_path=DEFAULT_HANDOFF_SCHEMA):
    r = Report()
    items, problems = load_all(skills_root)

    for ident, why in problems:
        r.err("frontmatter", f"{ident}: {why}")
    r.ok("frontmatter")

    # ── السياسة العامة (قد تكون أكثر من ملف بنفس المرتبة) ──────────────────────
    policy_paths = list(policy_paths) or list(DEFAULT_POLICY_PATHS)
    seen_policy_ids = set()
    for pp in policy_paths:
        if not (pp and Path(pp).is_file()):
            r.err("global_policy_present", f"ملف سياسة عامة مفقود: {pp}")
            continue
        fm, _ = parse_frontmatter(Path(pp).read_text(encoding="utf-8"))
        policy_meta = fm or {}
        pid = policy_meta.get("policy_id") or Path(pp).stem
        if policy_meta.get("type") != "GLOBAL_POLICY":
            r.err("global_policy_present", f"{pp}: ليس مصنّفاً type: GLOBAL_POLICY")
        elif policy_meta.get("scope") != "ALL_ASSISTANTS":
            r.err("global_policy_present", f"{pp}: نطاق السياسة ليس ALL_ASSISTANTS")
        else:
            seen_policy_ids.add(pid)
        if policy_meta.get("override_allowed") is not False:
            r.err("global_policy_override", f"{pp}: override_allowed يجب أن تكون false صراحة")
        if str(policy_meta.get("priority", "")).upper() != "HIGHEST":
            r.err("global_policy_override", f"{pp}: priority يجب أن تكون HIGHEST")

    missing_policies = set(GLOBAL_POLICY_IDS) - seen_policy_ids
    if missing_policies:
        r.err("global_policy_present",
              f"سياسات عامة مطلوبة غير موجودة أو غير صالحة: {'، '.join(sorted(missing_policies))}")
    else:
        r.ok("global_policy_present")
    r.ok("global_policy_override")

    # ── فحص كل مساعد ─────────────────────────────────────────────────────────
    canonical = {}
    all_legacy = {}
    for ident, recs in items.items():
        if len(recs) > 1:
            paths = "، ".join(x["file_path"] for x in recs)
            r.err("duplicate_assistant_id", f"{ident}: معرّف مكرر في {paths}")
        rec = recs[0]
        meta = rec["meta"]
        aid = meta.get("assistant_id")

        if not meta:
            r.err("schema_required_fields", f"{ident}: بلا كتلة metadata")
            continue

        for field in REQUIRED_FIELDS:
            if field not in meta or meta[field] in (None, "", []):
                r.err("schema_required_fields", f"{ident}: حقل مطلوب ناقص أو فارغ — {field}")

        if aid != ident:
            r.err("id_consistency", f"{ident}: assistant_id ({aid}) لا يطابق name")
        if Path(rec["file_path"]).parent.name != ident:
            r.err("id_consistency", f"{ident}: اسم المجلد لا يطابق المعرّف")
        if not ID_RE.match(ident):
            r.err("id_format", f"{ident}: لا يطابق صيغة kebab-case أو يبدأ برقم")

        if meta.get("domain") not in DOMAINS:
            r.err("domain_vocabulary", f"{ident}: domain غير معروف — {meta.get('domain')}")
        if meta.get("domain") in OUT_OF_SCOPE_DOMAINS:
            r.err("domain_out_of_scope",
                  f"{ident}: domain={meta.get('domain')} خارج نطاق هذه الإضافة "
                  "(إدارة عيادة وتسويق فقط) — انظر governance/scope-boundary.md")

        status = meta.get("status")
        if status not in LIFECYCLE:
            r.err("lifecycle_status", f"{ident}: حالة غير معروفة — {status}")

        version = str(meta.get("version", ""))
        if not SEMVER_RE.match(version):
            r.err("semver_format", f"{ident}: إصدار غير صالح — {version}")

        ltv = meta.get("last_tested_version")
        if status in ROUTABLE:
            if not ltv:
                r.err("active_requires_tested",
                      f"{ident}: ACTIVE بلا last_tested_version")
            elif str(ltv) != version:
                r.err("active_version_tested",
                      f"{ident}: ACTIVE بإصدار {version} واختبار {ltv} — الحالة الصحيحة TESTING")

        prio = meta.get("routing_priority")
        if not isinstance(prio, int) or not (0 <= prio <= 100):
            r.err("routing_priority_range", f"{ident}: routing_priority خارج 0–100 — {prio}")

        if meta.get("safety_level") not in SAFETY_LEVELS:
            r.err("safety_level_vocabulary", f"{ident}: safety_level غير معروف")
        elif meta["safety_level"] in ("HIGH", "CRITICAL"):
            found = [m for m in SAFETY_BODY_MARKERS if m in rec["body"]]
            if len(found) < 2:
                r.err("safety_body_sections",
                      f"{ident}: مستوى {meta['safety_level']} بلا أقسام سلامة وخصوصية في الجسم")

        pdeps_here = as_list(meta.get("policy_dependencies"))
        missing_pol = [p for p in GLOBAL_POLICY_IDS if p not in pdeps_here]
        if missing_pol:
            r.err("policy_inheritance",
                  f"{ident}: لا يرث السياسة/السياسات العامة — {'، '.join(missing_pol)}")

        negs = meta.get("negative_triggers")
        if not isinstance(negs, list) or not negs:
            r.err("negative_triggers_required", f"{ident}: negative_triggers فارغة أو مفقودة")
        else:
            for n in negs:
                if not isinstance(n, dict) or "match" not in n or "route_to" not in n:
                    r.err("negative_triggers_required",
                          f"{ident}: عنصر negative_trigger بلا match/route_to")

        desc = rec["description"]
        if len(desc) < 80:
            r.err("description_routable", f"{ident}: وصف أقصر من أن يُطابَق")
        if '"' not in desc and "«" not in desc:
            r.err("description_routable", f"{ident}: وصف بلا عبارات تشغيل مقتبسة")

        # ── حد فعلي مكتشَف بالتجربة المباشرة (رفع حقيقي فشل): واجهة رفع الإضافات
        # في Cowork ترفض أي SKILL.md بحقل description أطول من ١٠٢٤ حرفاً — قيد لا
        # تفرضه أي وثيقة حوكمة هنا، فيمر هذا الفحص محلياً وتفشل الإضافة كاملة عند
        # الرفع الفعلي. لا توثيق رسمي لهذا الحد وقت الكتابة؛ ١٠٢٤ هو الرقم الحرفي
        # من رسالة الخطأ.
        if len(desc) > 1024:
            r.err("description_length",
                  f"{ident}: description بطول {len(desc)} حرفاً — يتجاوز حد ١٠٢٤ حرفاً الذي تفرضه واجهة رفع الإضافات فعلياً")

        # ── description يجب أن يعكس status حرفياً — المحرّك الفعلي (Cowork/Claude)
        # يقرأ فقط حقل description في الـ frontmatter وقت اختيار مهارة؛ لا يقرأ
        # metadata.status. مساعد غير ACTIVE بوصف لا يفصح عن ذلك يُستدعى تلقائياً
        # تماماً كأي مساعد ACTIVE رغم أن lifecycle-versioning.md يمنع ذلك صراحة.
        # انظر governance/proposals/2026-08-28-description-status-visibility.md
        if status == "DEPRECATED":
            expected = f"[STATUS: DEPRECATED → {meta.get('deprecated_by')}]"
            if not desc.startswith(expected):
                r.err("description_reflects_status",
                      f"{ident}: DEPRECATED بلا وسم '{expected}' في بداية description")
        elif status in ("TESTING", "PILOT", "DRAFT", "ARCHIVED"):
            expected = f"[STATUS: {status}]"
            if not desc.startswith(expected):
                r.err("description_reflects_status",
                      f"{ident}: {status} بلا وسم '{expected}' في بداية description")
        elif status == "ACTIVE" and desc.lstrip().startswith("[STATUS:"):
            r.err("description_reflects_status",
                  f"{ident}: ACTIVE لكن description يحمل وسم status متبقٍّ من حالة سابقة")

        for alias in as_list(meta.get("legacy_aliases")):
            all_legacy.setdefault(alias, []).append(ident)

        canonical[ident] = meta

    for check in ("duplicate_assistant_id", "schema_required_fields", "id_consistency",
                  "id_format", "domain_vocabulary", "domain_out_of_scope",
                  "lifecycle_status", "semver_format",
                  "active_requires_tested", "active_version_tested",
                  "routing_priority_range", "safety_level_vocabulary",
                  "safety_body_sections", "policy_inheritance",
                  "negative_triggers_required", "description_routable",
                  "description_reflects_status", "description_length"):
        r.ok(check)

    known = set(canonical)

    # ── معرّف قديم يُستخدم كمعرّف كانوني ──────────────────────────────────────
    for alias, owners in all_legacy.items():
        if alias in known:
            r.err("legacy_as_canonical",
                  f"{alias}: معرّف قديم مستخدم كمعرّف كانوني (يملكه {'، '.join(owners)})")
        if len(owners) > 1:
            r.err("legacy_alias_collision",
                  f"{alias}: alias مملوك لأكثر من مساعد — {'، '.join(owners)}")
    r.ok("legacy_as_canonical")
    r.ok("legacy_alias_collision")

    # ── المراجع ──────────────────────────────────────────────────────────────
    external_ok = set()
    for ident, meta in canonical.items():
        refs = (as_list(meta.get("can_delegate_to")) + as_list(meta.get("cannot_delegate_to"))
                + as_list(meta.get("skill_dependencies"))
                + [n.get("route_to") for n in (meta.get("negative_triggers") or [])
                   if isinstance(n, dict)])
        for target in refs:
            if not target:
                continue
            if target in known or target in external_ok:
                continue
            # مرجع خارج نطاق الحوكمة: يُقبل كتحذير لا كخطأ، ويُسجَّل
            r.warn("external_reference",
                   f"{ident} → {target}: مرجع خارج نطاق الاستوديو (مهارة حساب غير مُرحَّلة)")

        for kdep in as_list(meta.get("knowledge_dependencies")):
            if knowledge_root:
                p = Path(knowledge_root) / kdep.replace("knowledge/", "")
                if not (p.exists() or str(kdep).endswith("/")):
                    r.warn("knowledge_reference",
                           f"{ident}: مرجع معرفة غير موجود محلياً — {kdep}")
        for pdep in as_list(meta.get("policy_dependencies")):
            if pdep not in KNOWN_POLICY_IDS:
                r.err("policy_reference", f"{ident}: سياسة غير معروفة — {pdep}")
    r.ok("external_reference")
    r.ok("knowledge_reference")
    r.ok("policy_reference")

    # ── دورات التفويض ────────────────────────────────────────────────────────
    graph = {k: [t for t in as_list(v.get("can_delegate_to")) if t in known]
             for k, v in canonical.items()}
    cycles = detect_circular(graph)
    for c in cycles:
        r.err("circular_delegation", "دورة تفويض: " + " → ".join(c))
    r.ok("circular_delegation")

    for ident, meta in canonical.items():
        forbidden = set(as_list(meta.get("cannot_delegate_to")))
        actual = set(as_list(meta.get("can_delegate_to")))
        clash = forbidden & actual
        if clash:
            r.err("delegation_contradiction",
                  f"{ident}: {'، '.join(clash)} في can و cannot معاً")
    r.ok("delegation_contradiction")

    # ── هدف تفويض غير صالح — can_delegate_to استدعاء فعلي، يجب أن يشير إلى ─────
    # مساعد كانوني معروف داخل الحوكمة. مغاير عن external_reference (تحذير) لأن
    # skill_dependencies/negative_triggers قد تشير خارج النطاق بقرار موثَّق
    # (migration-spec.yaml deferred)، لكن استدعاءً فعلياً وقت التنفيذ لا يجوز
    # أن يستهدف شيئاً غير موجود في النظام المحوكَم إطلاقاً.
    for ident, meta in canonical.items():
        for target in as_list(meta.get("can_delegate_to")):
            if target not in known:
                r.err("invalid_delegation_target",
                      f"{ident} → {target}: can_delegate_to يستهدف معرّفاً غير كانوني/غير موجود")
    r.ok("invalid_delegation_target")

    # ── اعتمادية على مساعد DEPRECATED ────────────────────────────────────────
    # أي مرجع فعلي (تفويض أو استهلاك مخرَج أو إحالة توجيه) يجب أن يستهدف البديل
    # الكانوني، لا معرّفاً DEPRECATED — حتى لو ظل موجوداً لعدم كسر الطلبات القديمة.
    for ident, meta in canonical.items():
        refs = (as_list(meta.get("can_delegate_to")) + as_list(meta.get("skill_dependencies"))
                + [n.get("route_to") for n in (meta.get("negative_triggers") or [])
                   if isinstance(n, dict)])
        for target in refs:
            tmeta = canonical.get(target)
            if tmeta and tmeta.get("status") == "DEPRECATED":
                repl = tmeta.get("deprecated_by") or "—"
                r.err("deprecated_as_dependency",
                      f"{ident} → {target}: مرجع لمساعد DEPRECATED — البديل الكانوني {repl}")
    r.ok("deprecated_as_dependency")

    # ── مساعد معزول — orphan_assistant (تحذير لا خطأ) ───────────────────────
    # لا مرجع وارد إليه (لا can_delegate_to ولا skill_dependencies ولا
    # negative_triggers.route_to من أي مساعد آخر) ولا مرجع صادر منه. مساعد
    # مستقل يُستدعى مباشرة من المستخدمة فقط وهذا سليم غالباً — لذا تحذير
    # للمراجعة البشرية، لا فشل بناء.
    referenced_targets = set()
    for meta in canonical.values():
        referenced_targets.update(as_list(meta.get("can_delegate_to")))
        referenced_targets.update(as_list(meta.get("skill_dependencies")))
        referenced_targets.update(
            n.get("route_to") for n in (meta.get("negative_triggers") or [])
            if isinstance(n, dict))
    for ident, meta in canonical.items():
        # role: orchestrator مستثنى عمداً: يستهدف أي مساعد ACTIVE في الدليل الحي
        # وقت التشغيل (توجيه ديناميكي)، لا مجموعة مقفلة سلفاً في can_delegate_to/
        # skill_dependencies — هذا موثَّق صراحة في handoff_contract.notes الخاص به،
        # فتعليمه للفاحص أدق من تحذير كاذب متكرر عليه في كل تشغيلة.
        if meta.get("role") == "orchestrator":
            continue
        has_outgoing = bool(as_list(meta.get("can_delegate_to"))
                             or as_list(meta.get("skill_dependencies")))
        if ident not in referenced_targets and not has_outgoing:
            r.warn("orphan_assistant",
                   f"{ident}: لا مرجع وارد ولا صادر في رسم الاعتماديات — تحقق أنه ليس منسياً")
    r.ok("orphan_assistant")

    # ── عقد التسليم ──────────────────────────────────────────────────────────
    handoff_schema_meta = None
    if handoff_schema_path and Path(handoff_schema_path).is_file():
        try:
            hs = yaml.safe_load(Path(handoff_schema_path).read_text(encoding="utf-8"))
            handoff_schema_meta = (hs or {}).get("meta")
            if handoff_schema_meta and handoff_schema_meta.get("schema_version"):
                r.ok("handoff_schema_present")
            else:
                r.err("handoff_schema_present",
                      f"{handoff_schema_path}: بلا meta.schema_version صالح")
        except yaml.YAMLError as e:
            r.err("handoff_schema_present", f"{handoff_schema_path}: YAML غير صالح — {e}")
    else:
        r.err("handoff_schema_present", f"ملف عقد التسليم مفقود: {handoff_schema_path}")

    for ident, meta in canonical.items():
        hc = meta.get("handoff_contract")
        if not isinstance(hc, dict):
            continue
        expect_accepts = set(as_list(meta.get("skill_dependencies")))
        expect_delegates = set(as_list(meta.get("can_delegate_to")))
        got_accepts = set(as_list(hc.get("accepts_from")))
        got_delegates = set(as_list(hc.get("delegates_to")))
        if got_accepts != expect_accepts:
            r.err("handoff_contract_consistency",
                  f"{ident}: handoff_contract.accepts_from لا يطابق skill_dependencies")
        if got_delegates != expect_delegates:
            r.err("handoff_contract_consistency",
                  f"{ident}: handoff_contract.delegates_to لا يطابق can_delegate_to")
        if set(as_list(hc.get("required_inputs"))) != set(as_list(meta.get("required_inputs"))):
            r.err("handoff_contract_consistency",
                  f"{ident}: handoff_contract.required_inputs لا يطابق required_inputs")
        if set(as_list(hc.get("guaranteed_outputs"))) != set(as_list(meta.get("outputs"))):
            r.err("handoff_contract_consistency",
                  f"{ident}: handoff_contract.guaranteed_outputs لا يطابق outputs")
        if handoff_schema_meta:
            sv = hc.get("schema_version")
            if sv and str(sv) != str(handoff_schema_meta.get("schema_version")):
                r.err("incompatible_schema_version",
                      f"{ident}: handoff_contract.schema_version={sv} "
                      f"≠ {handoff_schema_meta.get('schema_version')} الحالي")
    r.ok("handoff_contract_consistency")
    r.ok("incompatible_schema_version")

    # ── سلامة توليد الدليل — تشغيلة جافة، لا كتابة فعلية ────────────────────
    # يمثّل نفس التنسيق الذي يستخدمه build_registry.py — إن رمى استثناءً هنا
    # سيرميه هناك أيضاً وقت التوليد الفعلي.
    try:
        for m in canonical.values():
            " · ".join(f"«{v}»" for v in as_list(m.get("triggers"))[:3])
            " · ".join(f"«{n.get('match')}» ← `{n.get('route_to')}`"
                       for n in (m.get("negative_triggers") or [])[:3]
                       if isinstance(n, dict))
        r.ok("registry_generation_sane")
    except (TypeError, AttributeError) as e:
        r.err("registry_generation_sane", f"توليد الدليل سيفشل: {e}")

    # ── التداخل ──────────────────────────────────────────────────────────────
    overlaps = []
    idents = sorted(canonical)
    for i, a in enumerate(idents):
        for b in idents[i + 1:]:
            ma, mb = canonical[a], canonical[b]
            sa = token_set(ma.get("purpose"), " ".join(as_list(ma.get("triggers"))),
                           " ".join(as_list(ma.get("outputs"))))
            sb = token_set(mb.get("purpose"), " ".join(as_list(mb.get("triggers"))),
                           " ".join(as_list(mb.get("outputs"))))
            score = jaccard(sa, sb)
            band = overlap_band(score)
            if band == "LOW":
                continue
            routes_a = {n.get("route_to") for n in (ma.get("negative_triggers") or [])
                        if isinstance(n, dict)}
            routes_b = {n.get("route_to") for n in (mb.get("negative_triggers") or [])
                        if isinstance(n, dict)}
            separated = (b in routes_a) or (a in routes_b)
            overlaps.append({"a": a, "b": b, "score": round(score, 3),
                             "band": band, "separated": separated})
            both_active = ma.get("status") in ROUTABLE and mb.get("status") in ROUTABLE
            if band == "PROBABLE_DUPLICATE" and both_active and not separated:
                r.err("active_overlapping_roles",
                      f"{a} ~ {b}: تشابه {score:.2f} وكلاهما ACTIVE بلا فصل بـ negative_triggers")
            elif band == "HIGH" and both_active and not separated:
                r.warn("active_overlapping_roles",
                       f"{a} ~ {b}: تشابه {score:.2f} بلا سطر فصل صريح")
    r.ok("active_overlapping_roles")

    counts = {"total": len(canonical)}
    for st in LIFECYCLE:
        counts[st] = sum(1 for m in canonical.values() if m.get("status") == st)

    return r, canonical, overlaps, counts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skills", required=True)
    ap.add_argument("--policy", action="append", default=[],
                     help="يُكرَّر لكل ملف GLOBAL_POLICY؛ افتراضياً house-rules.md و clinical-firewall.md")
    ap.add_argument("--knowledge-root")
    ap.add_argument("--handoff-schema", default=DEFAULT_HANDOFF_SCHEMA)
    ap.add_argument("--json")
    args = ap.parse_args()

    r, canonical, overlaps, counts = validate(
        Path(args.skills).expanduser().resolve(), args.policy, args.knowledge_root,
        args.handoff_schema)

    print("\nفحص النظام\n" + "═" * 58)
    for check in sorted(r.checks):
        print(f"  {r.checks[check]:4s}  {check}")
    print("═" * 58)
    print(f"مساعدون: {counts['total']} · " +
          " · ".join(f"{k}:{v}" for k, v in counts.items() if k != "total" and v))

    if r.warnings:
        print(f"\nتنبيهات ({len(r.warnings)}):")
        for c, m in r.warnings:
            print(f"  ! [{c}] {m}")
    if r.errors:
        print(f"\nأخطاء ({len(r.errors)}):")
        for c, m in r.errors:
            print(f"  ✗ [{c}] {m}")

    if overlaps:
        print(f"\nتداخل مرصود ({len(overlaps)}):")
        for o in sorted(overlaps, key=lambda x: -x["score"])[:12]:
            mark = "مفصول" if o["separated"] else "غير مفصول"
            print(f"  {o['band']:20s} {o['score']:.2f}  {o['a']} ~ {o['b']}  [{mark}]")

    verdict = "FAIL" if r.errors else ("PASS WITH WARNINGS" if r.warnings else "PASS")
    print(f"\nالنتيجة: {verdict}\n")

    if args.json:
        Path(args.json).write_text(json.dumps({
            "verdict": verdict, "checks": r.checks, "counts": counts,
            "errors": [{"check": c, "message": m} for c, m in r.errors],
            "warnings": [{"check": c, "message": m} for c, m in r.warnings],
            "overlaps": overlaps,
        }, ensure_ascii=False, indent=2), encoding="utf-8")

    return 1 if r.errors else 0


if __name__ == "__main__":
    sys.exit(main())
