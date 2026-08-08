from pathlib import Path

from src.analytics.detection_analyzer import DetectionAnalyzer

MISSION = Path("missions/mission_20260808_034026")

DETECTION_FILE = MISSION / "reports" / "detections.csv"


def test_detection_file_exists():
    assert DETECTION_FILE.exists()


def test_detection_summary():
    analyzer = DetectionAnalyzer(DETECTION_FILE)

    summary = analyzer.summary()

    assert summary["images_inspected"] == 15
    assert summary["total_detections"] == 31

    assert summary["class_counts"]["panel"] == 9
    assert summary["class_counts"]["cracked"] == 20
    assert summary["class_counts"]["dusty"] == 2


def test_average_confidence():
    analyzer = DetectionAnalyzer(DETECTION_FILE)

    summary = analyzer.summary()

    assert 0.66 < summary["average_confidence"] < 0.67


def test_critical_detections():
    analyzer = DetectionAnalyzer(DETECTION_FILE)

    summary = analyzer.summary()

    assert summary["critical_detections"] == 20
    assert summary["inspection_status"] == "CRITICAL"
