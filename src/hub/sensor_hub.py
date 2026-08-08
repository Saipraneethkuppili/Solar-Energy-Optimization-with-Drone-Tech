"""
Sensor Hub

Collects data from all hardware modules.
"""

from src.hardware.lidar.manager import TFLunaManager
from src.hardware.pixhawk.manager import PixhawkManager
from src.hardware.sht31.manager import SHT31Manager
from src.hardware.tsl2591.manager import TSL2591Manager


class SensorHub:
    """Central manager for all onboard sensors."""

    def __init__(self):
        self.pixhawk = PixhawkManager("/dev/ttyACM0")
        self.lidar = TFLunaManager()
        self.sht31 = SHT31Manager()
        self.tsl2591 = TSL2591Manager()

    def initialize(self):
        """Initialize all sensors."""

        self.sht31.connect()
        self.tsl2591.connect()

    def read_all(self):
        """Read all available sensor data."""

        return {
            "environment": self.sht31.read(),
            "light": self.tsl2591.read(),
        }

    def shutdown(self):
        """Shutdown all sensors."""

        self.sht31.disconnect()
        self.tsl2591.disconnect()
