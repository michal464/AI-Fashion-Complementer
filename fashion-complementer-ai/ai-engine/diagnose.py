import cv2
import sys
from pathlib import Path
from pymongo import MongoClient

CATALOG = Path("C:/Users/משתמש/Desktop/AI-Fashion-Complementer/fashion-complementer-ai/catalog/images")
SUPPORTED = {".jpg", ".jpeg", ".png", ".webp", ".avif"}

ok, fail, fails = 0, 0, []

for f in CATALOG.rglob("*"):
    if f.suffix.lower() not in SUPPORTED:
        continue
    img = cv2.imread(str(f))
    if img is None:
        fail += 1
        fails.append(f.parent.name + "/" + f.name)
    else:
        ok += 1

print("Images OK:", ok)
print("Images FAIL:", fail)
for x in fails[:10]:
    print("  FAIL:", x)

# Check MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["fashion_db"]
count = db["fashion_items"].count_documents({})
print("MongoDB fashion_items count:", count)

# Show sample doc
sample = db["fashion_items"].find_one()
if sample:
    print("Sample doc keys:", list(sample.keys()))
    print("Sample name:", sample.get("name"))
    print("Sample category:", sample.get("category"))
    print("Embedding length:", len(sample.get("embedding", [])))
