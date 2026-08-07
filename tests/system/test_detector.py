from src.vision.model_loader import ModelLoader
from src.vision.detector import SolarPanelDetector


def main():
    loader = ModelLoader()
    loader.load()

    detector = SolarPanelDetector(loader.get_model())

    results = detector.detect(
        "datasets/sample/test.jpg",
        save=True
    )

    print("\n" + "=" * 60)
    print("SOLAR PANEL INSPECTION REPORT")
    print("=" * 60)

    total = 0

    for result in results:
        names = result.names

        for box in result.boxes:
            cls = int(box.cls.item())
            conf = float(box.conf.item())

            print(f"{names[cls]:<12}  Confidence : {conf:.2%}")
            total += 1

    print("-" * 60)
    print(f"Total Objects Detected : {total}")
    print("=" * 60)


if __name__ == "__main__":
    main()