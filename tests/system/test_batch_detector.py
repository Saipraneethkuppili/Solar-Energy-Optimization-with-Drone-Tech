from src.vision.batch_detector import BatchDetector


def main():

    detector = BatchDetector()

    detector.process_folder("datasets/mission")


if __name__ == "__main__":
    main()
