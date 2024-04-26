import logging

LOGGER = logging.getLogger(__name__)


def setup_logging(handler):
    #LOGGER.addHandler(handler)
    LOGGER.setLevel(logging.DEBUG)
