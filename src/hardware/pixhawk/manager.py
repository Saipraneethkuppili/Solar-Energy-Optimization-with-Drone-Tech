"""
Pixhawk Flight Controller Manager

Author: Sai Praneeth Kuppili
Project: Solar Energy Optimization with Drone Tech
"""

from pymavlink import mavutil

from src.core.logger import get_logger


class PixhawkManager:
    """Handles communication with Pixhawk using MAVLink."""

    def __init__(self, port: str, baudrate: int = 115200):
        self.port = port
        self.baudrate = baudrate
        self.master = None
        self.logger = get_logger("Pixhawk")

    def connect(self):
        """Connect to the Pixhawk."""

        self.logger.info("Connecting to Pixhawk...")

        self.master = mavutil.mavlink_connection(
            self.port,
            baud=self.baudrate,
        )

        self.master.wait_heartbeat()

        self.logger.info("Heartbeat received.")
        self.logger.info(f"Connected to System {self.master.target_system}")

    def disconnect(self):
        """Disconnect from the Pixhawk."""

        if self.master:
            self.master.close()
            self.logger.info("Pixhawk disconnected.")

    def heartbeat(self):
        """Read heartbeat."""

        return self.master.recv_match(
            type="HEARTBEAT",
            blocking=True,
        )
