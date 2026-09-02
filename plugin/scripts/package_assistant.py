#!/usr/bin/env python3
"""تغليف مساعد كملف .skill جاهز للتثبيت والمشاركة.

الاستخدام:
    python3 package_assistant.py <مسار مجلد المساعد> [مجلد الإخراج]

ينتج <name>.skill (أرشيف zip) في مجلد الإخراج (الافتراضي: نفس المجلد الأب).
يشغّل الفحص البنيوي أولاً ويرفض التغليف إن فشل.
"""

import subprocess
import sys
import zipfile
from pathlib import Path

EXCLUDE_NAMES = {".DS_Store", "__pycache__", ".git", "node_modules", ".ipynb_checkpoints"}


def should_skip(path: Path) -> bool:
    return any(part in EXCLUDE_NAMES or part.endswith(".pyc") for part in path.parts)


def main():
    if len(sys.argv) < 2:
        print("الاستخدام: package_assistant.py <مسار مجلد المساعد> [مجلد الإخراج]")
        return 2

    root = Path(sys.argv[1]).expanduser().resolve()
    if not (root / "SKILL.md").is_file():
        print(f"✗ لا يوجد SKILL.md في {root}")
        return 1

    validator = Path(__file__).with_name("validate_assistant.py")
    if validator.is_file():
        result = subprocess.run(
            [sys.executable, str(validator), str(root)],
            capture_output=True,
            text=True,
        )
        print(result.stdout, end="")
        if result.returncode != 0:
            print("✗ التغليف متوقف: أصلح الأخطاء أعلاه ثم أعد المحاولة.")
            return 1

    out_dir = Path(sys.argv[2]).expanduser().resolve() if len(sys.argv) > 2 else root.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{root.name}.skill"

    count = 0
    with zipfile.ZipFile(out_file, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(root.rglob("*")):
            if not path.is_file() or should_skip(path.relative_to(root)):
                continue
            zf.write(path, path.relative_to(root.parent))
            count += 1

    size_kb = out_file.stat().st_size / 1024
    print(f"✓ تم التغليف: {out_file}")
    print(f"  {count} ملف · {size_kb:.1f} كيلوبايت")
    return 0


if __name__ == "__main__":
    sys.exit(main())
