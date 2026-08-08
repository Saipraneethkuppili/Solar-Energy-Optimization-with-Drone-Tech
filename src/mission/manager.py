"""
Mission Manager

Creates and manages a unique directory for every inspection mission.
"""

from datetime import datetime, timezone
from pathlib import Path


class MissionManager:
    """Create and manage mission directories."""

    def __init__(self, root: str = "missions"):
        self.root = Path(root)
        self.root.mkdir(
            parents=True,
            exist_ok=True,
        )

    def create(self) -> Path:
        """Create a new mission directory."""

        mission_name = datetime.now(
            timezone.utc
        ).strftime(
            "mission_%Y%m%d_%H%M%S"
        )

        mission = self.root / mission_name

        # Avoid collision if two missions start
        # within the same second.
        if mission.exists():

            suffix = 1

            while True:

                candidate = (
                    self.root
                    / f"{mission_name}_{suffix}"
                )

                if not candidate.exists():

                    mission = candidate
                    break

                suffix += 1

        # Mission structure
        (mission / "images").mkdir(
            parents=True,
            exist_ok=True,
        )

        (mission / "annotated").mkdir(
            exist_ok=True,
        )

        (mission / "reports").mkdir(
            exist_ok=True,
        )

        (mission / "telemetry").mkdir(
            exist_ok=True,
        )

        return mission