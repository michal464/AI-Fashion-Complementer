"""
generate_embeddings.py
Run once (or re-run to update catalog) from the ai-engine/ directory:
    python generate_embeddings.py
"""

import os
import sys
from pathlib import Path
from pymongo import MongoClient, UpdateOne
from dotenv import load_dotenv

# Load .env from server/
load_dotenv(Path(__file__).parent.parent / "server" / ".env")

sys.path.insert(0, str(Path(__file__).parent))
from feature_extractor import FeatureExtractor

# ── Config ────────────────────────────────────────────────────────────────────
MODEL_PATH   = str(Path(__file__).parent.parent / "fashion_style_model.h5")
CATALOG_DIR  = Path(__file__).parent.parent / "catalog" / "images"
MONGO_URI    = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME      = os.getenv("DB_NAME", "fashion_db")
BATCH_SIZE   = 32
IMG_EXTS     = {".jpg", ".jpeg", ".png", ".webp"}

# Style is encoded in the filename prefix: casual_*, formal_*, sporty_*, boho_*
def _parse_style(filename: str) -> str:
    name = filename.lower()
    for s in ("casual", "formal", "sporty", "boho"):
        if name.startswith(s):
            return s
    return "casual"

def _build_name(filename: str) -> str:
    stem = Path(filename).stem
    return stem.replace("_", " ").title()

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("Loading feature extractor...")
    extractor = FeatureExtractor(MODEL_PATH)

    client = MongoClient(MONGO_URI)
    collection = client[DB_NAME]["fashion_items"]

    # Index: unique on image_path, vector search on embedding
    collection.create_index("image_path", unique=True)
    collection.create_index("category")
    collection.create_index("style")

    # Collect all images
    items = []
    for category_dir in sorted(CATALOG_DIR.iterdir()):
        if not category_dir.is_dir():
            continue
        category = category_dir.name.lower()
        for img_file in sorted(category_dir.iterdir()):
            if img_file.suffix.lower() in IMG_EXTS:
                items.append((category, img_file))

    if not items:
        print(f"No images found in {CATALOG_DIR}. Add images and re-run.")
        return

    print(f"Found {len(items)} images. Generating embeddings in batches of {BATCH_SIZE}...")

    ops = []
    for i, (category, img_path) in enumerate(items):
        try:
            embedding = extractor.extract_from_path(str(img_path))
        except Exception as e:
            print(f"  [SKIP] {img_path.name}: {e}")
            continue

        relative_path = f"images/{category}/{img_path.name}"
        doc = {
            "name":       _build_name(img_path.name),
            "category":   category,
            "style":      _parse_style(img_path.name),
            "image_path": relative_path,
            "embedding":  embedding,
        }

        # Upsert: update if exists (re-running is safe), insert if new
        ops.append(UpdateOne(
            {"image_path": relative_path},
            {"$set": doc},
            upsert=True
        ))

        if len(ops) >= BATCH_SIZE:
            result = collection.bulk_write(ops)
            print(f"  Batch {i // BATCH_SIZE}: upserted={result.upserted_count} modified={result.modified_count}")
            ops = []

    if ops:
        result = collection.bulk_write(ops)
        print(f"  Final batch: upserted={result.upserted_count} modified={result.modified_count}")

    total = collection.count_documents({})
    print(f"\nDone. Total items in fashion_items collection: {total}")
    client.close()


if __name__ == "__main__":
    main()
