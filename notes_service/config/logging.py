"""Logging Module"""

import logging


def configure_logger() -> logging.Logger:
    app_logger = logging.getLogger("notes_service")
    app_logger.setLevel(logging.DEBUG)

    # Create a console handler and set the log level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create a formatter and add it to the handlers
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)

    app_logger.addHandler(console_handler)

    return app_logger


logger = configure_logger()
