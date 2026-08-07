"""
Batch Detection Engine
Processes all mission images and generates analytics.
"""

from pathlib import Path

from src.vision.model_loader import ModelLoader
from src.vision.detector import SolarPanelDetector

from src.analytics.statistics import Statistics
from src.analytics.exporter import CSVExporter


class BatchDetector:

    def __init__(self):

        loader = ModelLoader()
        loader.load()

        self.detector = SolarPanelDetector(loader.get_model())

        self.stats = Statistics()

        self.exporter = CSVExporter()
        self.exporter.initialize()

    def process_folder(self, folder: str):

        folder = Path(folder)

        images = []

        for ext in ("*.jpg", "*.jpeg", "*.png"):
            images.extend(folder.glob(ext))

        images = sorted(images)

        if not images:
            print("No images found.")
            return

        print("=" * 60)
        print("SOLAR DRONE MISSION")
        print("=" * 60)
        print(f"Images Found : {len(images)}")
        print()

        for index, image in enumerate(images, start=1):

            print(f"[{index}/{len(images)}] {image.name}")

            self.stats.add_image()

            detections = self.detector.detect(
                str(image),
                save=True
            )

            for detection in detections:

                self.stats.add_detection(
                    detection["class"]
                )

                self.exporter.add_detection(
                    image.name,
                    detection["class"],
                    detection["confidence"],
                    detection["box"]
                )

        print()

        self.stats.summary()

        print()

        print("CSV Report Saved:")
        print("reports/detections.csv")

        print()

        print("=" * 60)
        print("MISSION COMPLETED")
        print("=" * 60)