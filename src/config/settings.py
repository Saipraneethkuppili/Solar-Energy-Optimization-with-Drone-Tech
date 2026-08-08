"""
Central configuration for Solar Energy Optimization
with Drone Technology.
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class MissionConfig:
    model_path: Path = Path("models/weights/best.pt")
    image_directory: Path = Path("datasets/mission")

    confidence_threshold: float = 0.25
    image_size: int = 640

    telemetry_source: str = "simulation"

    camera_model: str = "Raspberry Pi Camera V3"
    flight_controller: str = "Pixhawk"

    software_version: str = "0.7"


DEFAULT_CONFIG = MissionConfig()
