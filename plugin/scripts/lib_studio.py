#!/usr/bin/env python3
"""مكتبة مشتركة لأدوات حوكمة استوديو المساعدين.

تُستخدم من inventory.py و validate_system.py و build_registry.py و routing_tests.py.
"""

import json
import re
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

# ── ثوابت المخطط ─────────────────────────────────────────────────────────────

ID_RE = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")
LIFECYCLE = ["DRAFT", "TESTING", "PILOT", "ACTIVE", "DEPRECATED", "ARCHIVED"]
ROUTABLE = ["ACTIVE"]
SAFETY_LEVELS = ["LOW", "MODERATE", "HIGH", "CRITICAL"]
SEMVER_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")

DOMAINS = [
    "system", "instagram", "marketing", "content", "patient",
    "clinical", "research", "management", "finance", "sales",
    "legal", "operations",
]

REQUIRED_FIELDS = [
    "assistant_id", "display_name", "domain", "role", "purpose",
    "triggers", "negative_triggers", "outputs",
    "policy_dependencies", "routing_priority", "safety_level",
    "status", "version", "owner", "last_updated",
]

# الحقول التي يجوز أن تكون فارغة دون أن يُعد ذلك نقصاً
NULLABLE_FIELDS = [
    "optional_inputs", "knowledge_dependencies", "skill_dependencies",
    "tool_dependencies", "can_delegate_to", "cannot_delegate_to",
    "legacy_aliases", "deprecated_by", "notes", "evaluation_suite",
]

# سياستان عامتان بنفس المرتبة (priority: HIGHEST · override_allowed: false).
# كلتاهما إلزاميتان في policy_dependencies لكل مساعد. GLOBAL_POLICY_ID أُبقي
# للتوافق مع أدوات قديمة قد تستورده مباشرة؛ الفحص الفعلي يستخدم الـ tuple.
GLOBAL_POLICY_IDS = ("house-rules", "clinical-firewall")
GLOBAL_POLICY_ID = GLOBAL_POLICY_IDS[0]

# أسماء وثائق السياسة/الحوكمة المعروفة — لفحص policy_reference. أي policy_dependencies
# تذكر اسماً خارج هذه القائمة تُرفض.
KNOWN_POLICY_IDS = GLOBAL_POLICY_IDS + ("routing-policy", "scope-boundary")

# مجالات ممنوعة داخل هذه الإضافة تحديداً (assistant-studio = عيادة وتسويق فقط).
# موجودة في DOMAINS العام أعلاه لأنها مفردات مخطط عامة قد تُستخدم خارج هذه الإضافة؛
# الفحص هنا إضافي وخاص. انظر governance/scope-boundary.md.
OUT_OF_SCOPE_DOMAINS = ("clinical", "patient", "research")


# ── قراءة الملفات ────────────────────────────────────────────────────────────

def parse_frontmatter(text):
    """يعيد (frontmatter dict, body str). frontmatter = None إن غاب أو فسد."""
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    raw = text[3:end]
    body = text[end + 4:]
    if yaml is None:
        return {}, body
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError:
        return None, body
    return (data if isinstance(data, dict) else None), body


def load_skill(skill_dir: Path):
    """يقرأ مجلد مهارة ويعيد سجلاً موحداً."""
    skill_md = skill_dir / "SKILL.md"
    rec = {
        "file_path": str(skill_md),
        "dir_name": skill_dir.name,
        "exists": skill_md.is_file(),
        "frontmatter_ok": False,
        "name": None,
        "description": "",
        "meta": {},
        "body": "",
        "parse_error": None,
    }
    if not rec["exists"]:
        rec["parse_error"] = "SKILL.md مفقود"
        return rec

    text = skill_md.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    rec["body"] = body
    rec["raw"] = text
    if fm is None:
        rec["parse_error"] = "frontmatter مفقود أو غير صالح كـ YAML"
        return rec

    rec["frontmatter_ok"] = True
    rec["name"] = fm.get("name")
    rec["description"] = (fm.get("description") or "").strip()
    meta = fm.get("metadata")
    rec["meta"] = meta if isinstance(meta, dict) else {}
    return rec


def discover_skill_dirs(root: Path):
    """يعيد كل مجلد يحتوي SKILL.md تحت الجذر المعطى (بعمق ٣ مستويات)."""
    if not root.is_dir():
        return []
    found = []
    for depth in ("SKILL.md", "*/SKILL.md", "*/*/SKILL.md", "*/*/*/SKILL.md"):
        for p in root.glob(depth):
            if p.is_file():
                found.append(p.parent)
    return sorted(set(found), key=lambda p: str(p))


# ── تحليل ────────────────────────────────────────────────────────────────────

def as_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return [v for v in value if v not in (None, "")]
    return [value]


def find_references(text, known_ids, self_id=None):
    """يعيد مجموعة المعرّفات المذكورة داخل النص."""
    hits = set()
    for ident in known_ids:
        if ident == self_id:
            continue
        if re.search(r"(?<![A-Za-z0-9_-])" + re.escape(ident) + r"(?![A-Za-z0-9-])", text):
            hits.add(ident)
    return hits


def detect_circular(graph):
    """يعيد قائمة الدورات في رسم التفويض {id: [ids]}."""
    cycles, stack, seen = [], [], set()

    def walk(node, path):
        if node in path:
            cycle = path[path.index(node):] + [node]
            key = tuple(sorted(set(cycle)))
            if key not in seen:
                seen.add(key)
                cycles.append(cycle)
            return
        for nxt in graph.get(node, []):
            if nxt in graph:
                walk(nxt, path + [node])

    for start in graph:
        walk(start, [])
    return cycles


def token_set(*values):
    """يحوّل نصوصاً إلى مجموعة رموز للمقارنة الدلالية التقريبية."""
    text = " ".join(str(v) for v in values if v)
    text = re.sub(r"[^\w؀-ۿ]+", " ", text.lower())
    return {t for t in text.split() if len(t) > 2}


def jaccard(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def overlap_band(score):
    if score >= 0.62:
        return "PROBABLE_DUPLICATE"
    if score >= 0.42:
        return "HIGH"
    if score >= 0.25:
        return "MEDIUM"
    return "LOW"


def write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
