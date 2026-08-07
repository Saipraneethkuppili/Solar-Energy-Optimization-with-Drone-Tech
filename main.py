"""
Main application launcher.
"""

from src.core.application import Application


def main() -> None:
    app = Application()
    app.start()


if __name__ == "__main__":
    main()