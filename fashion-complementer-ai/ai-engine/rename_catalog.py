"""
rename_catalog.py
Renames all catalog images to: {style}_{category}_{number}.{ext}
Run from anywhere: python rename_catalog.py
"""

import os
from pathlib import Path

CATALOG_DIR = Path(__file__).parent.parent / "catalog" / "images"

# Default style assigned per category (can be extended)
CATEGORY_STYLES = {
    "shoes":       ["casual", "casual", "formal", "formal", "sporty", "sporty", "casual", "formal", "sporty", "casual",
                    "casual", "formal", "sporty", "casual", "casual", "formal", "sporty", "casual", "formal", "sporty",
                    "casual", "casual", "formal", "sporty", "casual", "casual", "formal", "sporty", "casual", "formal",
                    "sporty", "casual", "casual", "formal", "sporty", "casual", "casual", "formal", "sporty", "casual",
                    "formal", "sporty", "casual", "casual", "sporty"],
    "bags":        ["casual", "formal", "casual", "formal", "sporty", "casual", "formal", "casual", "formal", "sporty",
                    "casual", "formal", "casual", "formal", "sporty", "casual", "formal", "casual", "formal", "sporty"],
    "watches":     ["casual", "formal", "casual", "formal", "sporty", "casual", "formal", "casual", "formal", "sporty",
                    "casual", "formal", "casual", "formal", "sporty", "casual", "formal", "casual", "formal", "sporty"],
    "shirts":      ["casual", "casual", "formal", "casual", "sporty", "casual", "casual", "casual", "casual", "casual",
                    "casual", "formal", "casual", "casual", "casual", "casual", "casual", "casual", "casual", "casual",
                    "formal", "formal", "sporty", "casual", "casual", "casual", "casual", "casual", "casual", "casual"],
    "pants":       ["casual", "casual", "formal", "casual", "casual", "sporty", "casual", "formal", "sporty", "casual"],
    "jackets":     ["casual", "casual", "formal", "casual", "sporty", "casual", "casual", "formal", "casual", "sporty",
                    "casual", "formal", "casual", "casual", "casual", "sporty", "formal", "casual", "casual", "casual", "casual"],
    "accessories": ["casual", "casual", "boho", "casual", "formal", "casual", "sporty", "casual", "formal", "casual",
                    "boho", "casual", "formal", "casual", "sporty", "casual", "formal", "casual", "boho", "casual",
                    "casual", "formal", "casual", "boho", "casual", "sporty", "casual", "formal", "casual", "boho",
                    "casual", "formal", "casual", "boho", "casual", "sporty", "casual", "formal", "casual", "boho",
                    "casual", "boho", "casual", "formal", "casual", "sporty", "casual", "formal", "casual", "boho",
                    "casual", "formal", "casual", "boho", "casual"],
}

SUPPORTED_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".avif"}

def rename_category(category_dir: Path, category: str):
    files = sorted(
        [f for f in category_dir.iterdir() if f.suffix.lower() in SUPPORTED_EXTS],
        key=lambda f: f.name
    )

    styles = CATEGORY_STYLES.get(category, [])

    renamed = 0
    for i, file in enumerate(files):
        style = styles[i] if i < len(styles) else "casual"
        new_ext = file.suffix.lower()
        # normalize .jpeg -> .jpg
        if new_ext == ".jpeg":
            new_ext = ".jpg"
        new_name = f"{style}_{category}_{str(i + 1).zfill(2)}{new_ext}"
        new_path = category_dir / new_name

        if file.name == new_name:
            continue  # already correct

        # avoid collision
        if new_path.exists() and new_path != file:
            new_name = f"{style}_{category}_{str(i + 1).zfill(2)}_v2{new_ext}"
            new_path = category_dir / new_name

        file.rename(new_path)
        print(f"  {file.name}  ->  {new_name}")
        renamed += 1

    print(f"[{category}] renamed {renamed}/{len(files)} files\n")


def main():
    for category_dir in sorted(CATALOG_DIR.iterdir()):
        if not category_dir.is_dir():
            continue
        category = category_dir.name.lower()
        print(f"--- {category} ---")
        rename_category(category_dir, category)

    print("Done. All files renamed.")


if __name__ == "__main__":
    main()
