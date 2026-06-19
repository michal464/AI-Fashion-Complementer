import os
import sys
import numpy as np
from pathlib import Path
from pymongo.collection import Collection

# Allow importing from ai-engine
AI_ENGINE_PATH = str(Path(__file__).parent.parent.parent.parent.parent / "ai-engine")
if AI_ENGINE_PATH not in sys.path:
    sys.path.insert(0, AI_ENGINE_PATH)

import tensorflow as tf
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.models import Model
import cv2

from app.services.recommender import find_recommendations

MODEL_PATH = str(Path(__file__).parent.parent.parent.parent / "fashion_style_model.h5")

STYLE_CLASSES = ["Boho", "Casual", "Formal", "Sporty"]

# Category keywords to detect category from the dominant style cluster
# We detect category by asking the user to include it in the filename,
# but at runtime we use a simple heuristic: the predict endpoint already
# knows the style; category is derived from the DB match or passed separately.
# For the recommend flow we need the uploaded item's category.
# Strategy: run feature extractor, find top-1 match in SAME DB to get category.

_full_model = None
_extractor_model = None


def _load_models():
    global _full_model, _extractor_model
    if _full_model is None:
        _full_model = tf.keras.models.load_model(MODEL_PATH)
        embedding_layer = _full_model.get_layer("dense")
        _extractor_model = Model(inputs=_full_model.input, outputs=embedding_layer.output)
    return _full_model, _extractor_model


def _preprocess(image_bytes: bytes) -> np.ndarray:
    arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Cannot decode image.")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224, 224))
    return preprocess_input(np.expand_dims(img, axis=0).astype(np.float32))


def get_recommendations(image_bytes: bytes, collection: Collection) -> dict:
    full_model, extractor = _load_models()

    img_ready = _preprocess(image_bytes)

    # Style prediction
    preds = full_model.predict(img_ready, verbose=0)
    style_idx = int(np.argmax(preds[0]))
    predicted_style = STYLE_CLASSES[style_idx]

    # Embedding
    raw_emb = extractor.predict(img_ready, verbose=0)[0]
    norm = np.linalg.norm(raw_emb)
    embedding = (raw_emb / norm).tolist() if norm > 0 else raw_emb.tolist()

    # Detect category: find closest item in the DB (any category) to identify
    # what kind of item was uploaded, then exclude that category from results.
    uploaded_category = _detect_category(embedding, collection)

    recommendations = find_recommendations(
        query_embedding=embedding,
        uploaded_category=uploaded_category,
        uploaded_style=predicted_style.lower(),
        collection=collection,
    )

    return {
        "predicted_category": uploaded_category,
        "predicted_style": predicted_style,
        "recommendations": recommendations,
    }


def _detect_category(embedding: list[float], collection: Collection) -> str:
    """Find the closest item in the catalog and return its category."""
    query_vec = np.array(embedding, dtype=np.float32)
    best_score = -1.0
    best_category = "shirts"  # default fallback

    for doc in collection.find({}, {"category": 1, "embedding": 1, "_id": 0}):
        emb = np.array(doc["embedding"], dtype=np.float32)
        score = float(np.dot(query_vec, emb))
        if score > best_score:
            best_score = score
            best_category = doc["category"]

    return best_category
