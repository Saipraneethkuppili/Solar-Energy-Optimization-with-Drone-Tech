"""
Base class for all hardware sensors.

Author: Sai Praneeth Kuppili
Project: Solar Energy Optimization with Drone Tech
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseSensor(ABC):
    """Abstract base class for all sensors."""

    def __init__(self, sensor_name: str):
        self.sensor_name = sensor_name
        self.connected = False

    @abstractmethod
    def connect(self) -> bool:
        """Initialize the sensor."""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Disconnect the sensor."""
        pass

    @abstractmethod
    def read(self) -> Dict[str, Any]:
        """Read data from the sensor."""
        pass

    def is_connected(self) -> bool:
        """Return sensor connection status."""
        return self.connected