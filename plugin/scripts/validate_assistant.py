#!/usr/bin/env python3
"""فحص بنيوي لمساعد قبل التغليف.

الاستخدام:
    python3 validate_assistant.py <مسار مجلد المساعد>

يفحص: وجود SKILL.md، صحة الـ frontmatter، الحقول المطلوبة، جودة الوصف،
الطول، بقايا العناصر النائبة ⟨…⟩، ووجود أقسام السلامة الإلزامية.
"""

import re
import sys
from pathlib import Path

REQUIRED_FIELDS = ["name", "description"]
SAFETY_MARKERS = ["السلامة", "الحدود", "خصوصية", "PDPL", "موافقة", "تجهيل"]
PLACEHOLDER = re.compile(r"[⟨⟩]")
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
FENCE_RE = re.compile(r"^```.*?^```", re.DOTALL | re.MULTILINE)
# مساعد يمس المرضى أو المحتوى الطبي يلزمه قسما السلامة والحدود.
# ذكرة عابرة لا تكفي — يُشترط ٣ إشارات فأكثر حتى لا تُوسم المهارات الإدارية خطأً.
CLINICAL_RE = re.compile(r"مريض|مرضى|تشخيص|صور الحالات|صورة حالة|patient|clinical")
CLINICAL_THRESHOLD = 3
SAFETY_MIN = 2


def strip_fences(text):
    """أزل الكتل البرمجية — القوالب داخلها تحتوي عناصر نائبة مقصودة."""
    return FENCE_RE.sub("", text)


def parse_frontmatter(text):
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    raw = text[3:end]
    body = text[end + 4 :]
    data, key = {}, None
    for line in raw.splitlines():
        if not line.strip():
            continue
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m and not line.startswith(("  ", "\t")):
            key = m.group(1)
            data[key] = m.group(2).strip()
        elif key and line.startswith((" ", "\t")):
            data[key] = (data.get(key, "") + " " + line.strip()).strip()
    return data, body


def main():
    if len(sys.argv) < 2:
        print("الاستخدام: validate_assistant.py <مسار مجلد المساعد>")
        return 2

    root = Path(sys.argv[1]).expanduser().resolve()
    errors, warnings, passed = [], [], []

    if not root.is_dir():
        print(f"✗ المسار غير موجود: {root}")
        return 1

    skill_md = root / "SKILL.md"
    if not skill_md.is_file():
        print(f"✗ لا يوجد SKILL.md في {root}")
        return 1
    passed.append("SKILL.md موجود")

    text = skill_md.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)

    if fm is None:
        errors.append("frontmatter مفقود أو غير مغلق بـ ---")
        fm = {}
    else:
        passed.append("frontmatter سليم البنية")

    for field in REQUIRED_FIELDS:
        if not fm.get(field):
            errors.append(f"حقل مطلوب مفقود: {field}")

    name = fm.get("name", "")
    if name:
        if not NAME_RE.match(name):
            errors.append(f"الاسم '{name}' ليس kebab-case (حروف صغيرة وأرقام وشرطات فقط)")
        elif name != root.name:
            warnings.append(f"الاسم في الـ frontmatter '{name}' لا يطابق اسم المجلد '{root.name}'")
        else:
            passed.append(f"الاسم سليم: {name}")

    desc = fm.get("description", "")
    if desc:
        if len(desc) < 80:
            errors.append("الوصف قصير جداً — لن يُميَّز عن مهارات أخرى (المطلوب ٨٠ حرفاً فأكثر)")
        if len(desc) > 1400:
            warnings.append("الوصف طويل جداً — اختصره إلى ما دون ١٤٠٠ حرف")
        if '"' not in desc and "«" not in desc:
            errors.append("الوصف لا يحتوي عبارات تشغيل بين علامتي تنصيص")
        has_ar = bool(re.search(r"[؀-ۿ]", desc))
        has_en = bool(re.search(r"[A-Za-z]{4,}", desc))
        if not (has_ar and has_en):
            warnings.append("الوصف لا يجمع عبارات تشغيل عربية وإنجليزية معاً")
        if has_ar and has_en and '"' in desc:
            passed.append("الوصف يحتوي عبارات تشغيل ثنائية اللغة")

    words = len(body.split())
    if words > 1800:
        warnings.append(f"جسم المهارة طويل ({words} كلمة) — انقل التفاصيل إلى references/")
    elif words < 120:
        warnings.append(f"جسم المهارة قصير جداً ({words} كلمة) — غالباً ناقص")
    else:
        passed.append(f"طول الجسم مناسب ({words} كلمة)")

    prose = strip_fences(text)
    leftovers = PLACEHOLDER.findall(prose)
    if leftovers:
        errors.append(f"بقايا عناصر نائبة ⟨…⟩ في SKILL.md ({len(leftovers)} علامة) — املأها أو احذفها")
    else:
        passed.append("لا توجد عناصر نائبة غير ممتلئة")

    if len(CLINICAL_RE.findall(body)) >= CLINICAL_THRESHOLD:
        found = [m for m in SAFETY_MARKERS if m in body]
        if len(found) < SAFETY_MIN:
            errors.append(
                "المساعد يتعامل مع محتوى طبي أو بيانات مرضى وتنقصه أقسام السلامة "
                "والخصوصية (السلامة الطبية · الحدود · خصوصية المرضى / PDPL)"
            )
        else:
            passed.append(f"أقسام السلامة والخصوصية موجودة ({'، '.join(found)})")
    else:
        passed.append("مساعد غير سريري — أقسام السلامة غير مطلوبة")

    for sub in ("references", "knowledge"):
        d = root / sub
        if d.is_dir() and not any(d.iterdir()):
            warnings.append(f"المجلد {sub}/ فارغ — احذفه")

    print(f"\nفحص المساعد: {root.name}\n" + "─" * 44)
    for p in passed:
        print(f"  ✓ {p}")
    for w in warnings:
        print(f"  ! {w}")
    for e in errors:
        print(f"  ✗ {e}")

    print("─" * 44)
    if errors:
        print(f"النتيجة: فشل — {len(errors)} خطأ، {len(warnings)} تنبيه\n")
        return 1
    print(f"النتيجة: نجح — {len(warnings)} تنبيه\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
