"""
Simulated Pixhawk telemetry.

Used for development when physical flight hardware
is unavailable.
"""

from datetime import UTC, datetime


class SimulatedTelemetry:

    def __init__(self):

        self.connected = False

    def connect(self) -> bool:

        self.connected = True

        print("Simulated Pixhawk connected.")

        return True

    def read(self) -> dict:

        if not self.connected:
            raise RuntimeError("Simulator is not connected.")

        return {
            "timestamp": datetime.now(UTC).isoformat(),
            "gps": {
                "latitude": 18.2949,
                "longitude": 83.8938,
                "altitude": 25.0,
                "relative_altitude": 20.0,
            },
            "attitude": {
                "roll": 0.0,
                "pitch": 0.0,
                "yaw": 1.57,
            },
            "flight": {
                "mode": "AUTO",
                "armed": True,
            },
            "battery": {
                "voltage": 15.8,
                "current": 8.4,
                "level": 82,
            },
            "speed": {
                "groundspeed": 4.2,
                "airspeed": 4.5,
            },
        }

    def disconnect(self):

        self.connected = False

        print("Simulated Pixhawk disconnected.")
