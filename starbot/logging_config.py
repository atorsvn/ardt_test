"""Logging helpers for StarBot."""

import logging
import sys


def configure_logging(level: int = logging.INFO) -> None:
    """Configure root logging for the application."""

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logging.basicConfig(level=level, handlers=[handler])
