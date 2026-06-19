"""
recommender.py – Complementary fashion recommendation engine.

Logic:
1. Extract embedding from uploaded image.
2. Detect its category via the style classifier (reuse existing model).
3. Fetch catalog items from MongoDB (excluding same category).
4. Rank by cosine similarity (embeddings are already L2-normalized → dot product).
5. Boost items from complementary categories.
6. Return top-N results.
"""

import numpy as np
from pymongo.collection import Collection

# Which categories complement which (by uploaded item's category)
COMPLEMENTARY_MAP: dict[str, list[str]] = {
    "shirts":      ["pants", "shoes", "watches", "belts", "bags", "jackets", "accessories"],
    "pants":       ["shirts", "shoes", "bags", "jackets", "accessories"],
    "shoes":       ["pants", "shirts", "bags", "watches", "accessories"],
    "jackets":     ["shirts", "pants", "shoes", "bags", "accessories"],
    "bags":        ["shoes", "jackets", "pants", "accessories"],
    "watches":     ["shirts", "jackets", "accessories"],
    "accessories": ["shirts", "jackets", "shoes", "bags"],
}

# Priority boost for the top complementary categories (first 3 get the full boost)
PRIORITY_BOOST = 0.15


def _category_boost(uploaded_category: str, candidate_category: str) -> float:
    complements = COMPLEMENTARY_MAP.get(uploaded_category, [])
    if candidate_category not in complements:
        return 0.0
    rank = complements.index(candidate_category)
    # First 3 complements get full boost, rest get half
    return PRIORITY_BOOST if rank < 3 else PRIORITY_BOOST / 2


def find_recommendations(
    query_embedding: list[float],
    uploaded_category: str,
    uploaded_style: str,
    collection: Collection,
    top_n: int = 10,
) -> list[dict]:
    """
    Returns top_n complementary items ranked by (cosine_similarity + category_boost).
    Excludes items from the same category as the uploaded item.
    """
    query_vec = np.array(query_embedding, dtype=np.float32)

    # Exclude same category
    cursor = collection.find(
        {"category": {"$ne": uploaded_category}},
        {"_id": 0, "name": 1, "category": 1, "style": 1, "image_path": 1, "embedding": 1},
    )

    scored = []
    for doc in cursor:
        emb = np.array(doc["embedding"], dtype=np.float32)
        cosine_sim = float(np.dot(query_vec, emb))  # valid because both are L2-normalized

        boost = _category_boost(uploaded_category, doc["category"])

        # Style compatibility bonus
        style_bonus = 0.05 if doc.get("style") == uploaded_style else 0.0

        final_score = cosine_sim + boost + style_bonus

        scored.append({
            "name":       doc["name"],
            "category":   doc["category"],
            "style":      doc.get("style", ""),
            "image_path": doc["image_path"],
            "score":      round(final_score, 4),
        })

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_n]
