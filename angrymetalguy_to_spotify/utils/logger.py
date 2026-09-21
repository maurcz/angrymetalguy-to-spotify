import logging
import sys


def get_logger():
    logger = logging.getLogger("amg-to-spotify")

    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s %(message)s")

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        handler.setFormatter(formatter)

        logger.addHandler(handler)

    return logger
