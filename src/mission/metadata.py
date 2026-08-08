"""
Mission Metadata

Stores information describing an inspection mission.
"""

import json
from datetime import datetime, timezone
from pathlib import Path


class MissionMetadata:
    """Create and save mission metadata."""

    def save(
        self,
        mission: Path,
        image_count: int = 0,
        detection_count: int = 0,
        telemetry_source: str = "simulation",
        status: str = "completed",
    ) -> Path:
        """Save metadata.json for a mission."""

        now = datetime.now(
            timezone.utc
        )

        metadata = {

            "mission_id":
                mission.name,

            "created_at":
                now.isoformat(),

            "status":
                status,

            "drone": {
                "flight_controller":
                    "Pixhawk",
                "telemetry_source":
                    telemetry_source,
            },

            "camera": {
                "model":
                    "Raspberry Pi Camera V3",
            },

            "vision": {
                "model":
                    "YOLOv8",
                "image_size":
                    640,
                "confidence_threshold":
                    0.25,
            },

            "mission": {
                "image_count":
                    image_count,
                "detection_count":
                    detection_count,
            },

            "software": {
                "version":
                    "0.6",
            },
        }

        output_file = (
            mission / "metadata.json"
        )

        with output_file.open(
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                metadata,
                file,
                indent=4,
            )

        return output_file