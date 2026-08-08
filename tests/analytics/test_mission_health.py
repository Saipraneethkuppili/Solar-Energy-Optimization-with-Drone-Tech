from src.analytics.mission_health import MissionHealthAnalyzer


def test_critical_mission():
    analyzer = MissionHealthAnalyzer(
        {
            "panel": 9,
            "cracked": 20,
            "dusty": 2,
        }
    )

    health = analyzer.analyze()

    assert health.status == "CRITICAL"
    assert health.total_detections == 31
    assert health.panel_detections == 9
    assert health.cracked_detections == 20
    assert health.dusty_detections == 2
    assert health.defect_detections == 22


def test_warning_mission():
    analyzer = MissionHealthAnalyzer(
        {
            "panel": 10,
            "dusty": 3,
        }
    )

    health = analyzer.analyze()

    assert health.status == "WARNING"
    assert health.defect_detections == 3


def test_healthy_mission():
    analyzer = MissionHealthAnalyzer(
        {
            "panel": 10,
        }
    )

    health = analyzer.analyze()

    assert health.status == "HEALTHY"
    assert health.defect_detections == 0


def test_unknown_mission():
    analyzer = MissionHealthAnalyzer({})

    health = analyzer.analyze()

    assert health.status == "UNKNOWN"
