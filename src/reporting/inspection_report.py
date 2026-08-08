"""
Solar Panel Inspection Report Generator

Converts mission detection and telemetry data into
a human-readable inspection report.
"""

import csv
import json
from collections import Counter
from pathlib import Path

from src.analytics.mission_health import MissionHealthAnalyzer


class InspectionReport:
    """Generate an inspection report for a completed mission."""

    def __init__(self, mission_directory):
        self.mission = Path(mission_directory)

        self.detection_file = (
            self.mission
            / "reports"
            / "detections.csv"
        )

        self.telemetry_file = (
            self.mission
            / "telemetry"
            / "telemetry.csv"
        )

        self.metadata_file = (
            self.mission
            / "metadata.json"
        )

    # ---------------------------------------------------------
    # Load detections
    # ---------------------------------------------------------

    def load_detections(self):
        """Load YOLO detection records."""

        if not self.detection_file.exists():
            raise FileNotFoundError(
                f"Detection file not found: "
                f"{self.detection_file}"
            )

        with self.detection_file.open(
            "r",
            newline="",
            encoding="utf-8",
        ) as file:
            return list(csv.DictReader(file))

    # ---------------------------------------------------------
    # Load telemetry
    # ---------------------------------------------------------

    def load_telemetry(self):
        """Load telemetry records."""

        if not self.telemetry_file.exists():
            return []

        with self.telemetry_file.open(
            "r",
            newline="",
            encoding="utf-8",
        ) as file:
            return list(csv.DictReader(file))

    # ---------------------------------------------------------
    # Load metadata
    # ---------------------------------------------------------

    def load_metadata(self):
        """Load mission metadata."""

        if not self.metadata_file.exists():
            return {}

        with self.metadata_file.open(
            "r",
            encoding="utf-8",
        ) as file:
            return json.load(file)

    # ---------------------------------------------------------
    # Detection summary
    # ---------------------------------------------------------

    def detection_summary(self):
        """Calculate detection statistics."""

        detections = self.load_detections()

        classes = Counter(
            detection["Class"]
            for detection in detections
        )

        confidence_values = []

        for detection in detections:
            try:
                confidence_values.append(
                    float(detection["Confidence"])
                )
            except (
                KeyError,
                TypeError,
                ValueError,
            ):
                continue

        if confidence_values:
            average_confidence = (
                sum(confidence_values)
                / len(confidence_values)
            )
        else:
            average_confidence = 0.0

        return {
            "total_detections": len(detections),
            "class_counts": dict(classes),
            "average_confidence": average_confidence,
        }

    # ---------------------------------------------------------
    # Inspection status
    # ---------------------------------------------------------

    def inspection_status(self, class_counts):
        """
        Determine overall inspection status.

        cracked -> CRITICAL
        dusty   -> ATTENTION REQUIRED
        panel   -> NORMAL
        """

        cracked = class_counts.get(
            "cracked",
            0,
        )

        dusty = class_counts.get(
            "dusty",
            0,
        )

        if cracked > 0:
            return "CRITICAL"

        if dusty > 0:
            return "ATTENTION REQUIRED"

        return "NORMAL"

    # ---------------------------------------------------------
    # Generate recommendation
    # ---------------------------------------------------------

    def recommendation(self, class_counts):
        """Generate a human-readable recommendation."""

        cracked = class_counts.get(
            "cracked",
            0,
        )

        dusty = class_counts.get(
            "dusty",
            0,
        )

        if cracked > 0:
            return (
                "Immediate inspection of areas associated "
                "with cracked detections."
            )

        if dusty > 0:
            return (
                "Inspect dusty panel areas and consider "
                "cleaning before further performance analysis."
            )

        return (
            "No critical defects detected. "
            "Continue routine inspection."
        )

    # ---------------------------------------------------------
    # Generate report
    # ---------------------------------------------------------

    def generate(self):
        """Generate complete report data."""

        detections = self.load_detections()

        detection_stats = self.detection_summary()

        telemetry = self.load_telemetry()

        metadata = self.load_metadata()

        class_counts = detection_stats[
            "class_counts"
        ]

        status = self.inspection_status(
            class_counts
        )

        # -----------------------------------------------------
        # Mission health analysis
        # -----------------------------------------------------

        health_analyzer = MissionHealthAnalyzer(
            class_counts
        )

        health = health_analyzer.analyze()

        # -----------------------------------------------------
        # Calculate image count
        # -----------------------------------------------------

        images_inspected = len(
            {
                detection["Image"]
                for detection in detections
            }
        )

        # -----------------------------------------------------
        # Build report
        # -----------------------------------------------------

        report = {
            "mission_id": metadata.get(
                "mission_id",
                self.mission.name,
            ),

            "status": status,

            "images_inspected": images_inspected,

            "total_detections":
                detection_stats[
                    "total_detections"
                ],

            # Keep existing API compatibility.
            "detections_by_class":
                class_counts,

            # New analytics-compatible field.
            "class_counts":
                class_counts,

            "average_confidence":
                detection_stats[
                    "average_confidence"
                ],

            "critical_detections":
                class_counts.get(
                    "cracked",
                    0,
                ),

            "telemetry_records":
                len(telemetry),

            # Mission health information.
            "health": {
                "status": health.status,
                "total_detections":
                    health.total_detections,
                "panel_detections":
                    health.panel_detections,
                "cracked_detections":
                    health.cracked_detections,
                "dusty_detections":
                    health.dusty_detections,
                "defect_detections":
                    health.defect_detections,
                "defect_ratio":
                    health.defect_ratio,
                "recommendation":
                    health.recommendation,
            },

            "recommendation":
                self.recommendation(
                    class_counts
                ),

            "metadata":
                metadata,
        }

        return report

    # ---------------------------------------------------------
    # Save JSON report
    # ---------------------------------------------------------

    def save_json(self):
        """Save machine-readable JSON report."""

        report = self.generate()

        output = (
            self.mission
            / "reports"
            / "inspection_report.json"
        )

        with output.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                report,
                file,
                indent=4,
            )

        return output

    # ---------------------------------------------------------
    # Save text report
    # ---------------------------------------------------------

    def save_text(self):
        """Save human-readable inspection report."""

        report = self.generate()

        output = (
            self.mission
            / "reports"
            / "inspection_report.txt"
        )

        counts = report[
            "detections_by_class"
        ]

        health = report[
            "health"
        ]

        with output.open(
            "w",
            encoding="utf-8",
        ) as file:

            file.write(
                "=" * 70
                + "\n"
            )

            file.write(
                "SOLAR PANEL INSPECTION REPORT\n"
            )

            file.write(
                "=" * 70
                + "\n\n"
            )

            # -------------------------------------------------
            # Mission information
            # -------------------------------------------------

            file.write(
                f"Mission ID          : "
                f"{report['mission_id']}\n"
            )

            file.write(
                f"Inspection Status   : "
                f"{report['status']}\n"
            )

            file.write(
                f"Images Inspected    : "
                f"{report['images_inspected']}\n"
            )

            file.write(
                f"Total Detections    : "
                f"{report['total_detections']}\n"
            )

            file.write(
                f"Telemetry Records   : "
                f"{report['telemetry_records']}\n"
            )

            file.write(
                f"Average Confidence  : "
                f"{report['average_confidence']:.2%}\n"
            )

            file.write("\n")

            # -------------------------------------------------
            # Detection summary
            # -------------------------------------------------

            file.write(
                "DETECTION SUMMARY\n"
            )

            file.write(
                "-" * 70
                + "\n"
            )

            for class_name, count in sorted(
                counts.items()
            ):
                file.write(
                    f"{class_name:<20}"
                    f": {count}\n"
                )

            file.write("\n")

            # -------------------------------------------------
            # Mission health
            # -------------------------------------------------

            file.write(
                "MISSION HEALTH ANALYSIS\n"
            )

            file.write(
                "-" * 70
                + "\n"
            )

            file.write(
                f"Health Status       : "
                f"{health['status']}\n"
            )

            file.write(
                f"Panel Detections    : "
                f"{health['panel_detections']}\n"
            )

            file.write(
                f"Cracked Detections  : "
                f"{health['cracked_detections']}\n"
            )

            file.write(
                f"Dusty Detections    : "
                f"{health['dusty_detections']}\n"
            )

            file.write(
                f"Defect Detections   : "
                f"{health['defect_detections']}\n"
            )

            file.write(
                f"Defect Ratio        : "
                f"{health['defect_ratio']:.2%}\n"
            )

            file.write("\n")

            # -------------------------------------------------
            # Recommendation
            # -------------------------------------------------

            file.write(
                "RECOMMENDATION\n"
            )

            file.write(
                "-" * 70
                + "\n"
            )

            file.write(
                f"{health['recommendation']}\n"
            )

            file.write("\n")

            # -------------------------------------------------
            # Status interpretation
            # -------------------------------------------------

            file.write(
                "STATUS INTERPRETATION\n"
            )

            file.write(
                "-" * 70
                + "\n"
            )

            if counts.get(
                "cracked",
                0,
            ) > 0:

                file.write(
                    "CRITICAL: Cracked panel "
                    "detections require inspection.\n"
                )

            elif counts.get(
                "dusty",
                0,
            ) > 0:

                file.write(
                    "ATTENTION: Dusty panels "
                    "may require cleaning.\n"
                )

            else:

                file.write(
                    "NORMAL: No critical "
                    "defects detected.\n"
                )

            file.write("\n")

            file.write(
                "=" * 70
                + "\n"
            )

        return output