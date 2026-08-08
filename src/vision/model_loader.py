"""
Model Loader
-------------
Loads the trained YOLOv8 model and provides a singleton instance.
"""

from pathlib import Path

from ultralytics import YOLO


class ModelLoader:
    """Loads and manages the YOLO model."""

    def __init__(self, model_path: str = "models/weights/best.pt"):
        self.model_path = Path(model_path)
        self.model = None

    def load(self):
        """Load the YOLO model."""
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model not found: {self.model_path}")

        self.model = YOLO(str(self.model_path))
        print(f"[INFO] Model loaded successfully: {self.model_path}")

    def get_model(self):
        """Return the loaded model."""
        if self.model is None:
            raise RuntimeError("Model has not been loaded.")
        return self.model
