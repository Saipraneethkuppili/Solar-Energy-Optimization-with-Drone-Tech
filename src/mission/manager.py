"""
Mission Manager
Creates a new mission directory for every inspection.
"""

from pathlib import Path
from datetime import datetime


class MissionManager:

    def __init__(self):
        self.root = Path("missions")
        self.root.mkdir(exist_ok=True)

    def create(self):

        mission_name = datetime.now().strftime(
            "mission_%Y%m%d_%H%M%S"
        )

        mission = self.root / mission_name

        (mission / "images").mkdir(parents=True, exist_ok=True)
        (mission / "annotated").mkdir(exist_ok=True)
        (mission / "reports").mkdir(exist_ok=True)
        (mission / "telemetry").mkdir(exist_ok=True)

        return mission