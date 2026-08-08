"""
Application entry point.
"""

from src.core.constants import APP_NAME, VERSION
from src.core.logger import get_logger


class Application:
    """Main application."""

    def __init__(self):
        self.logger = get_logger("Application")

    def start(self) -> None:
        """Start the application."""

        self.logger.info("Application starting...")

        print("=" * 60)
        print(APP_NAME)
        print(f"Version : {VERSION}")
        print("=" * 60)

        self.logger.info("Application initialized successfully.")
