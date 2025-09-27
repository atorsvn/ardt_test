"""Entrypoint script for running StarBot."""

from starbot.discord_bot import run
from starbot.logging_config import configure_logging


if __name__ == "__main__":
    configure_logging()
    run()
