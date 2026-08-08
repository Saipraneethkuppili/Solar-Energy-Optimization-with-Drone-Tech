"""
Mission Report Generator

Generates a human-readable inspection report from
YOLO detection analytics.
"""

from pathlib import Path

from src.analytics.detection_analyzer import DetectionAnalyzer


class MissionReport:
    """Generate a solar-panel inspection report."""

    def __init__(self, mission_directory):
        self.mission = Path(mission_directory)

        if not self.mission.exists():
            raise FileNotFoundError(
                f"Mission directory not found: {self.mission}"
            )

        self.detection_file = (
            self.mission / "reports" / "detections.csv"
        )

        self.report_file = (
            self.mission / "reports" / "inspection_report.txt"
        )

        self.analyzer = DetectionAnalyzer(
            self.detection_file
        )

    def generate(self):
        """Generate and save the inspection report."""

        summary = self.analyzer.summary()
        counts = summary["class_counts"]

        panel_count = counts.get("panel", 0)
        cracked_count = counts.get("cracked", 0)
        dusty_count = counts.get("dusty", 0)
        bird_drop_count = counts.get("bird_drop", 0)

        status = summary["inspection_status"]

        if status == "CRITICAL":
            recommendation = (
                "Immediate inspection of detected damaged "
                "panel regions is recommended."
            )

        elif status == "ATTENTION REQUIRED":
            recommendation = (
                "Cleaning and follow-up inspection of dusty "
                "panel regions is recommended."
            )

        else:
            recommendation = (
                "No critical defects were detected. "
                "Continue routine inspection."
            )

        report = f"""
SOLAR PANEL INSPECTION REPORT
============================================================

MISSION INFORMATION
------------------------------------------------------------
Mission ID           : {self.mission.name}
Images inspected    : {summary["images_inspected"]}
Objects detected    : {summary["total_detections"]}

DETECTION SUMMARY
------------------------------------------------------------
Panel               : {panel_count}
Cracked             : {cracked_count}
Dusty               : {dusty_count}
Bird Drop           : {bird_drop_count}

MODEL PERFORMANCE
------------------------------------------------------------
Average confidence  : {summary["average_confidence"]:.2%}

CRITICAL FINDINGS
------------------------------------------------------------
Cracked detections  : {cracked_count}
Bird-drop detections: {bird_drop_count}
Critical detections : {summary["critical_detections"]}

INSPECTION STATUS
------------------------------------------------------------
{status}

RECOMMENDATION
------------------------------------------------------------
{recommendation}

============================================================
END OF REPORT
============================================================
""".strip()

        self.report_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.report_file.write_text(
            report,
            encoding="utf-8"
        )

        return self.report_file
