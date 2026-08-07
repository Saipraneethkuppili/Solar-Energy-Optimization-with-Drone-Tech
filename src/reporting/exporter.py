"""
CSV Detection Exporter
"""

import csv
from pathlib import Path


class DetectionExporter:

    def __init__(self):

        self.output = Path("reports")

        self.output.mkdir(exist_ok=True)

        self.csv_file = self.output / "detection_report.csv"

    def write_header(self):

        with open(self.csv_file, "w", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                "Image",
                "Class",
                "Confidence",
                "X1",
                "Y1",
                "X2",
                "Y2"
            ])

    def append_detection(
        self,
        image,
        cls,
        conf,
        x1,
        y1,
        x2,
        y2
    ):

        with open(self.csv_file, "a", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                image,
                cls,
                round(conf, 4),
                round(x1, 2),
                round(y1, 2),
                round(x2, 2),
                round(y2, 2)
            ])