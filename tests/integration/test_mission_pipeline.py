from pathlib import Path

from src.analytics.detection_analyzer import DetectionAnalyzer
from src.analytics.mission_health import MissionHealthAnalyzer
from src.reporting.inspection_report import InspectionReport

MISSION = Path("missions/mission_20260808_034026")


def test_mission_package_exists():
    assert MISSION.exists()

    assert (MISSION / "images").is_dir()
    assert (MISSION / "annotated").is_dir()
    assert (MISSION / "reports").is_dir()
    assert (MISSION / "telemetry").is_dir()


def test_mission_images():
    images = list((MISSION / "images").glob("*.jpg"))

    annotated = list((MISSION / "annotated").glob("*.jpg"))

    assert len(images) == 15
    assert len(annotated) == 15


def test_detection_analytics():
    detection_file = MISSION / "reports" / "detections.csv"

    analyzer = DetectionAnalyzer(detection_file)

    summary = analyzer.summary()

    assert summary["images_inspected"] == 15
    assert summary["total_detections"] == 31
    assert summary["class_counts"]["panel"] == 9
    assert summary["class_counts"]["cracked"] == 20
    assert summary["class_counts"]["dusty"] == 2


def test_mission_health():
    detection_file = MISSION / "reports" / "detections.csv"

    summary = DetectionAnalyzer(detection_file).summary()

    health = MissionHealthAnalyzer(summary["class_counts"]).analyze()

    assert health.status == "CRITICAL"
    assert health.total_detections == 31
    assert health.panel_detections == 9
    assert health.cracked_detections == 20
    assert health.dusty_detections == 2
    assert health.defect_detections == 22


def test_inspection_report():
    report = InspectionReport(MISSION)

    data = report.generate()

    assert data["mission_id"] == ("mission_20260808_034026")

    assert data["status"] == "CRITICAL"
    assert data["images_inspected"] == 15
    assert data["total_detections"] == 31
    assert data["telemetry_records"] == 15

    assert data["detections_by_class"]["cracked"] == 20


def test_report_files():
    reports = MISSION / "reports"

    assert (reports / "detections.csv").exists()

    assert (reports / "inspection_report.json").exists()

    assert (reports / "inspection_report.txt").exists()

    assert (MISSION / "metadata.json").exists()

    assert (MISSION / "telemetry" / "telemetry.csv").exists()
