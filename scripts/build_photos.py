#!/usr/bin/env python3
"""photos/ 폴더의 사진 목록을 photos.json으로 만든다.

photos/ 바로 아래 사진은 앨범 없음, photos/<앨범이름>/ 아래 사진은 그 앨범에 속한다.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PHOTOS = ROOT / "photos"
EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".avif", ".bmp", ".svg"}

items = []
if PHOTOS.is_dir():
    for path in sorted(PHOTOS.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in EXTS:
            continue
        rel = path.relative_to(ROOT).as_posix()
        parts = path.relative_to(PHOTOS).parts
        items.append({
            "src": rel,
            "name": path.stem,
            "album": parts[0] if len(parts) > 1 else "",
        })

(ROOT / "photos.json").write_text(
    json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(f"{len(items)} photos -> photos.json")
