"""
Main Drone Mission Runner
"""

from pathlib import Path

from src.mission.manager import MissionManager
from src.mission.metadata import MissionMetadata

from src.vision.model_loader import ModelLoader
from src.vision.detector import SolarPanelDetector


def main():

    print("=" * 60)
    print("SOLAR DRONE MISSION")
    print("=" * 60)

    manager = MissionManager()
    mission = manager.create()

    MissionMetadata().save(mission)

    print(f"Mission : {mission.name}")

    loader = ModelLoader()
    loader.load()

    detector = SolarPanelDetector(loader.get_model())

    images = sorted(Path("datasets/mission").glob("*.jpg"))

    print(f"Images : {len(images)}")
    print()

    for index, image in enumerate(images, start=1):

        print(f"[{index}/{len(images)}] {image.name}")

        detector.detect(str(image))

    print()

    print("=" * 60)
    print("MISSION COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()