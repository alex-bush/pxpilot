import functools
import logging
import time

logger = logging.getLogger(__name__)


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
        @functools.wraps(f)
        def retry_inner(*args, **kwargs):
            for i in range(tries):
                try:
                    return f(*args, **kwargs)
                except Exception as e:
                    if isinstance(e, excludes):
                        logger.debug(f"Skipped exception as excluded: {str(e)}")
                        raise e

                    logger.error(f"Try #{i + 1}. During execution '{f.__name__}' exception occurred: {str(e)}")

                    if i < tries - 1:
                        logger.debug(f"Waiting {delay} seconds before retrying...")
                        time.sleep(delay)

            raise Exception(f"Function '{f.__name__}' failed after {tries} attempts")

        return retry_inner

    return deco_retry
