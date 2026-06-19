import os
import sys
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import preprocess_input

# נתיב למודל המאומן ביחס לתיקיית ה-server
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "fashion_style_model.h5")

STYLE_CLASSES = ["Boho", "Casual", "Formal", "Sporty"]

RECOMMENDATIONS = {
    "Casual":  "שלב עם ג'ינס ונעלי ספורט לסגנון יומיומי נוח.",
    "Formal":  "שלב עם מכנסיים מחויטים ונעלי עקב למראה עסקי.",
    "Sporty":  "שלב עם טייץ ונעלי ריצה לפעילות ספורטיבית.",
    "Boho":    "שלב עם חצאית קפלים ותכשיטים אתניים לסגנון בוהמייני.",
}

_model = None

def _load_model():
    global _model
    if _model is None:
        _model = tf.keras.models.load_model(MODEL_PATH)
    return _model


def predict_from_bytes(image_bytes: bytes) -> dict:
    img_array = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("לא ניתן לפענח את התמונה.")

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (224, 224))
    img_ready = preprocess_input(np.expand_dims(image, axis=0))

    model = _load_model()
    preds = model.predict(img_ready)

    idx = int(np.argmax(preds[0]))
    style = STYLE_CLASSES[idx]
    confidence = float(preds[0][idx])

    return {
        "style": style,
        "confidence": round(confidence, 4),
        "recommendation": RECOMMENDATIONS[style],
    }
