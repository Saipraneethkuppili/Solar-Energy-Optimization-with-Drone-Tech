"""
YOLOv8 Solar Panel Detector
Runs inference on images using the trained YOLOv8 model.
"""

from pathlib import Path
from ultralytics import YOLO


class SolarPanelDetector:
    """YOLOv8 detector for solar panel inspection."""

    def __init__(self, model: YOLO):
        self.model = model

    def detect(self, image_path: str, save: bool = True):
        """
        Run inference on an image.

        Args:
            image_path: Path to input image.
            save: Save annotated image.

        Returns:
            List of detections.
        """

        image = Path(image_path)

        if not image.exists():
            raise FileNotFoundError(f"Image not found: {image}")

        results = self.model.predict(
            source=str(image),
            conf=0.25,
            imgsz=640,
            save=save,
            verbose=True,
        )

        detections = []

        result = results[0]

        names = result.names

        for box in result.boxes:

            class_id = int(box.cls.item())

            detections.append(
                {
                    "class": names[class_id],
                    "confidence": float(box.conf.item()),
                    "box": box.xyxy[0].tolist()
                }
            )

        return detections