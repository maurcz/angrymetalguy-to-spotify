import logging

def get_logger():

    logger = logging.getLogger("amg-to-spotify")

    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s %(message)s")

        handler = logging.StreamHandler()
        handler.setFormatter(formatter)

        logger.addHandler(handler)

    return logger
