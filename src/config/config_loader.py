"""
Configuration loader for the Solar Energy Optimization with Drone Tech project.
"""

from pathlib import Path

import yaml


class ConfigLoader:
    """Loads and provides access to the project configuration."""

    def __init__(self, config_path: str = "configs/config.yaml"):
        self.config_path = Path(config_path)
        self.config = {}

    def load(self) -> dict:
        """Load the YAML configuration file."""

        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")

        with self.config_path.open("r", encoding="utf-8") as file:
            self.config = yaml.safe_load(file)

        return self.config

    def get(self, *keys):
        """Retrieve nested configuration values."""

        value = self.config

        for key in keys:
            if key not in value:
                raise KeyError(f"Missing configuration key: {' -> '.join(keys)}")
            value = value[key]

        return value
