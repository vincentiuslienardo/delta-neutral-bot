import os
import sys

import structlog

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from bots.extended.src.infrastructure.logging import setup_logging


def verify_logging():
    setup_logging()
    logger = structlog.get_logger()
    logger.info("test_event", key="value", status="success")
    logger.error("test_error", error="something went wrong")


if __name__ == "__main__":
    verify_logging()
