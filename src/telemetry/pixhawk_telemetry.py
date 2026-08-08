"""
Pixhawk Telemetry Manager

MAVLink-based telemetry interface for Pixhawk.
Uses pymavlink instead of DroneKit.
"""

from datetime import datetime, timezone
from typing import Optional

from pymavlink import mavutil


class PixhawkTelemetry:

    def __init__(
        self,
        connection_string: str = "/dev/ttyACM0",
        baud: int = 57600,
    ):
        self.connection_string = connection_string
        self.baud = baud
        self.connection = None

    def connect(self) -> bool:
        """Connect to Pixhawk through MAVLink."""

        try:
            print(
                f"Connecting to Pixhawk: "
                f"{self.connection_string}"
            )

            self.connection = mavutil.mavlink_connection(
                self.connection_string,
                baud=self.baud,
            )

            print("Waiting for Pixhawk heartbeat...")

            self.connection.wait_heartbeat(
                timeout=10
            )

            print("Pixhawk connected successfully.")

            print(
                f"System ID : "
                f"{self.connection.target_system}"
            )

            print(
                f"Component : "
                f"{self.connection.target_component}"
            )

            return True

        except Exception as exc:

            print(
                f"Pixhawk connection failed: {exc}"
            )

            self.connection = None

            return False

    def read(self) -> dict:
        """Read one telemetry snapshot."""

        if self.connection is None:
            raise RuntimeError(
                "Pixhawk is not connected."
            )

        timestamp = datetime.now(
            timezone.utc
        ).isoformat()

        telemetry = {
            "timestamp": timestamp,
            "gps": {
                "latitude": None,
                "longitude": None,
                "altitude": None,
                "relative_altitude": None,
            },
            "attitude": {
                "roll": None,
                "pitch": None,
                "yaw": None,
            },
            "flight": {
                "mode": None,
                "armed": None,
            },
            "battery": {
                "voltage": None,
                "current": None,
                "level": None,
            },
            "speed": {
                "groundspeed": None,
                "airspeed": None,
            },
        }

        # GPS
        gps = self.connection.recv_match(
            type="GLOBAL_POSITION_INT",
            blocking=True,
            timeout=2,
        )

        if gps:

            telemetry["gps"]["latitude"] = (
                gps.lat / 1e7
            )

            telemetry["gps"]["longitude"] = (
                gps.lon / 1e7
            )

            telemetry["gps"]["altitude"] = (
                gps.alt / 1000.0
            )

            telemetry["gps"]["relative_altitude"] = (
                gps.relative_alt / 1000.0
            )

            telemetry["speed"]["groundspeed"] = (
                ((gps.vx ** 2 + gps.vy ** 2) ** 0.5)
                / 100.0
            )

        # Attitude
        attitude = self.connection.recv_match(
            type="ATTITUDE",
            blocking=False,
        )

        if attitude:

            telemetry["attitude"]["roll"] = (
                attitude.roll
            )

            telemetry["attitude"]["pitch"] = (
                attitude.pitch
            )

            telemetry["attitude"]["yaw"] = (
                attitude.yaw
            )

        # Battery
        battery = self.connection.recv_match(
            type="SYS_STATUS",
            blocking=False,
        )

        if battery:

            telemetry["battery"]["voltage"] = (
                battery.voltage_battery / 1000.0
            )

            telemetry["battery"]["current"] = (
                battery.current_battery / 100.0
            )

            telemetry["battery"]["level"] = (
                battery.battery_remaining
            )

        return telemetry

    def disconnect(self) -> None:
        """Close the Pixhawk connection."""

        if self.connection:

            self.connection.close()

            self.connection = None

            print("Pixhawk disconnected.")