import logging
import sys


def setup_logging():
    logger = logging.getLogger('pxvmflow')
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    logging.getLogger('requests').setLevel(logging.WARNING)

    return logger


LOGGER = setup_logging()
