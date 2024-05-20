import logging
import sys

from .__about__ import __title__, __version__
from .notifications import log as notifications_log


def setup_logging():
    logger = logging.getLogger('pxpilot')
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    notifications_log.set_metadata(__title__, __version__)
    notifications_log.setup_logging(stream_handler)

    logging.getLogger('requests').setLevel(logging.WARNING)

    return logger


LOGGER = setup_logging()
