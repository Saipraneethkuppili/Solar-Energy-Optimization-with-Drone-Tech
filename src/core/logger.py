"""
Production logging utilities.
"""

import logging
from pathlib import Path


def get_logger(
    name: str = "solar_inspection",
    log_file: str | Path = "logs/mission.log",
) -> logging.Logger:
    """Create or return the application logger."""

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(name)s : %(message)s"
    )

    file_handler = logging.FileHandler(
        log_path,
        encoding="utf-8",
    )

    console_handler = logging.StreamHandler()

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
