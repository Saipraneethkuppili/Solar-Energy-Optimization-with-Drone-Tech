"""
Application entry point.
"""

from src.core.constants import APP_NAME, VERSION


class Application:
    """Main application."""

    def start(self) -> None:
        """Start the application."""

        print("=" * 50)
        print(APP_NAME)
        print(f"Version : {VERSION}")
        print("=" * 50)