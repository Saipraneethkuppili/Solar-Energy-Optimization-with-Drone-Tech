"""
Telemetry recorder.

Stores telemetry snapshots as CSV during a mission.
"""

import csv
from pathlib import Path


class TelemetryRecorder:

    def __init__(self, output_file: str):

        self.output_file = Path(output_file)

        self.output_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.file = None
        self.writer = None

    def start(self):

        self.file = self.output_file.open(
            "w",
            newline="",
            encoding="utf-8",
        )

        self.writer = csv.writer(self.file)

        self.writer.writerow(
            [
                "Timestamp",
                "Latitude",
                "Longitude",
                "Altitude",
                "RelativeAltitude",
                "Roll",
                "Pitch",
                "Yaw",
                "FlightMode",
                "Armed",
                "BatteryVoltage",
                "BatteryCurrent",
                "BatteryLevel",
                "GroundSpeed",
                "AirSpeed",
            ]
        )

        self.file.flush()

    def record(self, telemetry: dict):

        if self.writer is None:
            raise RuntimeError("Telemetry recorder has not been started.")

        gps = telemetry["gps"]
        attitude = telemetry["attitude"]
        flight = telemetry["flight"]
        battery = telemetry["battery"]
        speed = telemetry["speed"]

        self.writer.writerow(
            [
                telemetry["timestamp"],
                gps["latitude"],
                gps["longitude"],
                gps["altitude"],
                gps["relative_altitude"],
                attitude["roll"],
                attitude["pitch"],
                attitude["yaw"],
                flight["mode"],
                flight["armed"],
                battery["voltage"],
                battery["current"],
                battery["level"],
                speed["groundspeed"],
                speed["airspeed"],
            ]
        )

        self.file.flush()

    def close(self):

        if self.file:

            self.file.close()

            self.file = None
            self.writer = None
