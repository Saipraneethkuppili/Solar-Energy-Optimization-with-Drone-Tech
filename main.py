"""
Main application launcher for Solar Energy Optimization with Drone Tech.
"""

import subprocess
import sys

from src.core.application import Application


def main() -> None:
    """Start the application or execute a mission."""
    application = Application()
    application.start()

    if "--mission" in sys.argv:
        print("\nStarting inspection mission...\n")
        result = subprocess.run(
            [sys.executable, "run_mission.py"],
            check=False,
        )

        if result.returncode != 0:
            raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()
