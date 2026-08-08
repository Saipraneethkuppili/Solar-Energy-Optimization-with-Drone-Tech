"""
SHT31 Temperature & Humidity Sensor Manager
"""

from src.core.logger import get_logger


class SHT31Manager:
    """Manages the SHT31 sensor."""

    def __init__(self):
        self.logger = get_logger("SHT31")
        self.connected = False

    def connect(self):
        self.connected = True
        self.logger.info("SHT31 connected.")

    def disconnect(self):
        self.connected = False
        self.logger.info("SHT31 disconnected.")

    def is_connected(self):
        return self.connected

    def read(self):
        """
        Placeholder values.
        Real USB communication will be added later.
        """
        return {
            "temperature": 27.5,
            "humidity": 63.2,
        }
