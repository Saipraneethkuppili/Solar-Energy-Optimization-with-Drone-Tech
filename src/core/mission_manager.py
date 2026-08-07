"""
Mission Manager
Creates and manages inspection mission directories.
"""

from pathlib import Path
from datetime import datetime


class MissionManager:

    def __init__(self):

        self.root = Path("missions")
        self.root.mkdir(exist_ok=True)

    def create_mission(self):

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        mission = self.root / f"mission_{timestamp}"

        (mission / "images").mkdir(parents=True, exist_ok=True)
        (mission / "annotated").mkdir(exist_ok=True)
        (mission / "reports").mkdir(exist_ok=True)

        return mission