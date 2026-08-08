"""
Solar Inspection REST API.
"""

from pathlib import Path
import csv
import json

from fastapi import FastAPI, HTTPException


MISSIONS_DIR = Path("missions")

app = FastAPI(
    title="Solar Panel Inspection API",
    version="0.8.0",
    description="REST API for solar-panel inspection missions.",
)


def mission_path(mission_id: str) -> Path:
    """Validate and return a mission directory."""

    path = MISSIONS_DIR / mission_id

    if not path.is_dir():
        raise HTTPException(
            status_code=404,
            detail=f"Mission not found: {mission_id}",
        )

    return path


def read_csv(path: Path):
    """Read CSV records."""

    if not path.exists():
        return []

    with path.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as file:
        return list(csv.DictReader(file))


def read_json(path: Path):
    """Read JSON data."""

    if not path.exists():
        return {}

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "solar-inspection-api",
        "version": "0.8.0",
    }


@app.get("/missions")
def list_missions():
    if not MISSIONS_DIR.exists():
        return {"count": 0, "missions": []}

    missions = sorted(
        path.name
        for path in MISSIONS_DIR.iterdir()
        if path.is_dir()
        and path.name.startswith("mission_")
    )

    return {
        "count": len(missions),
        "missions": missions,
    }


@app.get("/missions/{mission_id}")
def get_mission(mission_id: str):
    mission = mission_path(mission_id)

    return {
        "mission_id": mission_id,
        "metadata": read_json(
            mission / "metadata.json"
        ),
        "report": read_json(
            mission
            / "reports"
            / "inspection_report.json"
        ),
    }


@app.get("/missions/{mission_id}/detections")
def get_detections(mission_id: str):
    mission = mission_path(mission_id)

    detections = read_csv(
        mission
        / "reports"
        / "detections.csv"
    )

    return {
        "mission_id": mission_id,
        "count": len(detections),
        "detections": detections,
    }


@app.get("/missions/{mission_id}/telemetry")
def get_telemetry(mission_id: str):
    mission = mission_path(mission_id)

    telemetry = read_csv(
        mission
        / "telemetry"
        / "telemetry.csv"
    )

    return {
        "mission_id": mission_id,
        "count": len(telemetry),
        "telemetry": telemetry,
    }


@app.get("/missions/{mission_id}/report")
def get_report(mission_id: str):
    mission = mission_path(mission_id)

    report = read_json(
        mission
        / "reports"
        / "inspection_report.json"
    )

    if not report:
        raise HTTPException(
            status_code=404,
            detail="Inspection report not found.",
        )

    return report
