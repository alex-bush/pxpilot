import time
from pxpilot.logging_config import LOGGER


def retry(tries, delay, excludes):
    """
    Retry a function call if it fails.
    Args:
        tries: How many times to retry.
        delay: How many seconds to delay between retries.
        excludes: Excluded exception for which no retry

    Returns:

    """
    def deco_retry(f):
        def inner(*args, **kwargs):
            for i in range(tries):
                try:
                    return f(*args, **kwargs)
                except Exception as e:
                    if isinstance(e, excludes):
                        LOGGER.debug(f"Skipped exception: {e}")
                        raise e

                    LOGGER.exception(f"During execution {f.__name__} exception occurred: {e}")
                    LOGGER.warning(f"Retry #{i + 1}")
                    time.sleep(delay)
            raise Exception(f"Function {f.__name__} failed after {tries} attempts")

        return inner

    return deco_retry
