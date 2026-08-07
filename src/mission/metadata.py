"""
Mission Metadata
"""

import json
from datetime import datetime


class MissionMetadata:

    def save(self, mission):

        metadata = {

            "mission_id": mission.name,

            "date": datetime.now().strftime("%Y-%m-%d"),

            "time": datetime.now().strftime("%H:%M:%S"),

            "drone": "Pixhawk",

            "camera": "Raspberry Pi Camera V3",

            "model": "YOLOv8",

            "software_version": "0.6"

        }

        with open(
            mission / "metadata.json",
            "w"
        ) as f:

            json.dump(
                metadata,
                f,
                indent=4
            )