"""
TSL2591 Light Sensor Driver

Supports:
- Raspberry Pi Hardware Mode
- GitHub Codespaces Simulation Mode
"""

from src.core.logger import get_logger

try:
    import adafruit_tsl2591
    import board
    import busio

    HARDWARE_AVAILABLE = True

except ImportError:
    HARDWARE_AVAILABLE = False


class TSL2591Manager:
    """Driver for the TSL2591 Light Sensor."""

    def __init__(self):
        self.logger = get_logger("TSL2591")
        self.sensor = None

    def connect(self):
        """
        Connect to the sensor.
        If Raspberry Pi hardware is unavailable,
        automatically switch to simulation mode.
        """

        if not HARDWARE_AVAILABLE:
            self.logger.warning(
                "TSL2591 libraries unavailable. Running in simulation mode."
            )
            return

        try:
            i2c = busio.I2C(board.SCL, board.SDA)
            self.sensor = adafruit_tsl2591.TSL2591(i2c)

            self.logger.info("TSL2591 connected successfully.")

        except Exception as e:  # noqa: BLE001
            self.logger.warning(f"Simulation Mode Enabled ({e})")
            self.sensor = None

    def disconnect(self):
        """Disconnect the sensor."""

        self.sensor = None
        self.logger.info("TSL2591 disconnected.")

    def is_connected(self):
        """Return connection status."""

        return self.sensor is not None

    def read(self):
        """
        Read sensor values.

        Returns simulated values if hardware
        is unavailable.
        """

        if self.sensor is None:
            return {
                "lux": 85000.0,
                "infrared": 240,
                "visible": 620,
                "mode": "simulation",
            }

        return {
            "lux": self.sensor.lux,
            "infrared": self.sensor.infrared,
            "visible": self.sensor.visible,
            "mode": "hardware",
        }
