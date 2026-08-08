"""
Sensor Manager

Manages all sensors connected to the Raspberry Pi.
"""

from src.hardware.base_sensor import BaseSensor


class SensorManager:
    """Manages multiple sensors."""

    def __init__(self):
        self.sensors: dict[str, BaseSensor] = {}

    def register_sensor(self, sensor: BaseSensor) -> None:
        """Register a new sensor."""
        self.sensors[sensor.sensor_name] = sensor

    def connect_all(self) -> None:
        """Connect all registered sensors."""
        for sensor in self.sensors.values():
            sensor.connect()

    def disconnect_all(self) -> None:
        """Disconnect all registered sensors."""
        for sensor in self.sensors.values():
            sensor.disconnect()

    def read_all(self):
        """Read data from all sensors."""
        data = {}

        for sensor in self.sensors.values():
            if sensor.is_connected():
                data[sensor.sensor_name] = sensor.read()

        return data
