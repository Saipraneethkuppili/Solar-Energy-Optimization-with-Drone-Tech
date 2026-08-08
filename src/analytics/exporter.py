import csv
from pathlib import Path


class CSVExporter:

    def __init__(self):

        self.output = Path("reports")

        self.output.mkdir(exist_ok=True)

        self.file = self.output / "detections.csv"

    def initialize(self):

        with open(self.file, "w", newline="") as csvfile:

            writer = csv.writer(csvfile)

            writer.writerow(["Image", "Class", "Confidence", "X1", "Y1", "X2", "Y2"])

    def add_detection(self, image, cls, conf, box):

        with open(self.file, "a", newline="") as csvfile:

            writer = csv.writer(csvfile)

            writer.writerow(
                [
                    image,
                    cls,
                    round(conf, 3),
                    round(box[0], 2),
                    round(box[1], 2),
                    round(box[2], 2),
                    round(box[3], 2),
                ]
            )
