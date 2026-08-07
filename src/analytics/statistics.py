from collections import Counter


class Statistics:

    def __init__(self):
        self.classes = Counter()
        self.images = 0

    def add_image(self):
        self.images += 1

    def add_detection(self, cls):
        self.classes[cls] += 1

    def total_objects(self):
        return sum(self.classes.values())

    def summary(self):

        print("\n" + "=" * 60)
        print("MISSION SUMMARY")
        print("=" * 60)

        print(f"Images Processed : {self.images}")
        print(f"Objects Detected : {self.total_objects()}")

        print()

        for cls, count in self.classes.items():
            print(f"{cls:<15}: {count}")

        print("=" * 60)