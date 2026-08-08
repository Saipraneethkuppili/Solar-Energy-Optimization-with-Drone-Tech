from src.vision.model_loader import ModelLoader


def main():
    loader = ModelLoader()
    loader.load()

    model = loader.get_model()

    print("=" * 50)
    print("YOLO Model Loaded Successfully")
    print(model)
    print("=" * 50)


if __name__ == "__main__":
    main()
