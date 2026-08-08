"""
Mission Health Analyzer

Converts inspection detection statistics into
a mission-level health status and recommendation.
"""

from dataclasses import dataclass


@dataclass
class MissionHealth:
    """
    Mission health result.
    """

    total_detections: int
    panel_detections: int
    cracked_detections: int
    dusty_detections: int
    defect_detections: int
    defect_ratio: float
    status: str
    recommendation: str


class MissionHealthAnalyzer:
    """
    Analyze mission detection statistics.

    Important:
    Detection counts represent model detections.
    They are not automatically equivalent to unique
    physical solar panels.
    """

    def __init__(self, detection_summary: dict[str, int]):
        self.summary = detection_summary

    def analyze(self) -> MissionHealth:
        """
        Calculate mission health.
        """

        panel_count = self.summary.get(
            "panel",
            0,
        )

        cracked_count = self.summary.get(
            "cracked",
            0,
        )

        dusty_count = self.summary.get(
            "dusty",
            0,
        )

        total_detections = sum(self.summary.values())

        defect_detections = cracked_count + dusty_count

        if total_detections > 0:
            defect_ratio = defect_detections / total_detections
        else:
            defect_ratio = 0.0

        # --------------------------------------------------
        # Mission severity
        # --------------------------------------------------

        if cracked_count > 0:

            status = "CRITICAL"

            recommendation = (
                "Immediate inspection of "
                "areas associated with cracked "
                "detections."
            )

        elif dusty_count > 0:

            status = "WARNING"

            recommendation = (
                "Schedule cleaning and "
                "follow-up inspection for "
                "dust-affected areas."
            )

        elif panel_count > 0:

            status = "HEALTHY"

            recommendation = (
                "No critical defects detected. " "Continue routine monitoring."
            )

        else:

            status = "UNKNOWN"

            recommendation = (
                "No recognized solar-panel "
                "detections were found. "
                "Manual verification recommended."
            )

        return MissionHealth(
            total_detections=total_detections,
            panel_detections=panel_count,
            cracked_detections=cracked_count,
            dusty_detections=dusty_count,
            defect_detections=defect_detections,
            defect_ratio=round(
                defect_ratio,
                4,
            ),
            status=status,
            recommendation=recommendation,
        )
