from dataclasses import dataclass


@dataclass
class Telemetry:
    latitude: float = 0.0
    longitude: float = 0.0
    altitude: float = 0.0

    roll: float = 0.0
    pitch: float = 0.0
    yaw: float = 0.0

    battery_voltage: float = 0.0
    battery_remaining: int = 0

    flight_mode: str = "UNKNOWN"

    armed: bool = False