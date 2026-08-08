from collections import Counter


class MissionAnalytics:

    def __init__(self):

        self.counter = Counter()

    def add(self, cls):

        self.counter[cls] += 1

    def report(self):

        print()

        print("=" * 60)

        print("MISSION SUMMARY")

        print("=" * 60)

        total = sum(self.counter.values())

        print(f"Total Detections : {total}")

        print()

        for key, value in self.counter.items():

            print(f"{key:<15} : {value}")
