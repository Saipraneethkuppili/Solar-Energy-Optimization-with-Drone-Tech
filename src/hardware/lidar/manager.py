"""
TF-LUNA LiDAR Driver

Supports:
- UART Communication
- Distance Measurement
- Signal Strength
- Temperature
"""

import serial

from src.core.logger import get_logger


class TFLunaManager:
    """Driver for the Benewake TF-LUNA LiDAR."""

    def __init__(self, port="/dev/ttyUSB0", baudrate=115200):
        self.port = port
        self.baudrate = baudrate
        self.serial = None
        self.logger = get_logger("TF-LUNA")

    def connect(self):
        """Connect to the sensor."""

        self.serial = serial.Serial(
            self.port,
            self.baudrate,
            timeout=1,
        )

        self.logger.info("TF-LUNA connected.")

    def disconnect(self):
        """Disconnect from the sensor."""

        if self.serial:
            self.serial.close()
            self.logger.info("TF-LUNA disconnected.")

    def is_connected(self):
        return self.serial is not None
