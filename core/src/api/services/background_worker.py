import logging
import time
from concurrent.futures import ThreadPoolExecutor

from pxpilot.pilot import start


logger = logging.getLogger(__name__)


def pxpilot_worker():
    time.sleep(5)
    logger.debug(f'pxpilot worker started')

    start("config.yaml")


def run_pxpilot_worker() -> ThreadPoolExecutor:
    executor = ThreadPoolExecutor(max_workers=1)
    executor.submit(pxpilot_worker)

    return executor
