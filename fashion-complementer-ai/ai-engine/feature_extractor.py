import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.models import Model

import ssl
ssl._create_default_https_context = ssl._create_unverified_context


class FeatureExtractor:
    """
    Loads the trained ResNet50 model and removes the final Dense layer.
    The output of GlobalAveragePooling2D (2048-dim) is used as the embedding.
    All embeddings are L2-normalized so cosine similarity == dot product.
    """

    def __init__(self, model_path: str):
        full_model = tf.keras.models.load_model(model_path)

        # The architecture from train_style_model.py is:
        # ResNet50 base -> GlobalAveragePooling2D -> Dense(1024) -> Dense(4)
        # We use the Dense(1024) output as the embedding layer.
        embedding_layer = full_model.get_layer("dense")  # first Dense = 1024 units
        self.model = Model(inputs=full_model.input, outputs=embedding_layer.output)

    def extract(self, image_bytes: bytes) -> list[float]:
        """Extract normalized embedding from raw image bytes."""
        arr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Cannot decode image bytes.")
        return self._embed(img)

    def extract_from_path(self, image_path: str) -> list[float]:
        """Extract normalized embedding from a file path."""
        img = self._read_image(image_path)
        return self._embed(img)

    @staticmethod
    def _read_image(image_path: str) -> np.ndarray:
        """Read image using numpy to avoid OpenCV Unicode path issue on Windows."""
        with open(image_path, "rb") as f:
            data = f.read()
        arr = np.frombuffer(data, np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError(f"Cannot decode image: {image_path}")
        return img

    def _embed(self, img: np.ndarray) -> list[float]:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (224, 224))
        img_ready = preprocess_input(np.expand_dims(img, axis=0).astype(np.float32))
        embedding = self.model.predict(img_ready, verbose=0)[0]
        # L2 normalize so cosine similarity = dot product
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
        return embedding.tolist()
