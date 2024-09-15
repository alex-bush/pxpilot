import logging

import requests
from ping3 import ping
#from pythonping import ping

from pxpilot.models.configuration.vm_start_settings import HealthCheckOptions, HealthcheckType

logger = logging.getLogger(__name__)


class UnknownHealthcheckError(Exception):
    pass


class HostValidator:
    _PING_COUNT = 1
    _REQUEST_TIMEOUT = 2

    def validate(self, healthcheck: HealthCheckOptions) -> bool:
        if healthcheck.check_method.value == HealthcheckType.PING.value:
            return self._validate_ping(healthcheck)
        elif healthcheck.check_method.value == HealthcheckType.HTTP.value:
            return self._validate_request(healthcheck)

        raise UnknownHealthcheckError(f"Unknown healthcheck type: {healthcheck.check_method}")

    def _validate_ping(self, healthcheck: HealthCheckOptions) -> bool:
        """
        Performs a ping operation to check if the specified host, defined in the healthcheck parameter,
        is reachable over the network.

        :param healthcheck: An instance of HealthCheckOptions containing the necessary details
                            such as the address to ping.
        :return: True if the host responds to the ping, False if the host is unreachable or an error occurs.

        """
        try:
            logger.debug(f"Ping: {healthcheck.target_url}")
            #response = ping(healthcheck.target_url, count=self._PING_COUNT, verbose=True)
            response = ping(healthcheck.target_url)
            if not response or response is None:
                return False
            if response > 0:
                return True
            return False
        except ConnectionError:
            logger.debug(f"Validate. Error occurred during ping URL {healthcheck.target_url}.")
            return False
        except Exception as e:
            logger.error(e)

    def _validate_request(self, healthcheck: HealthCheckOptions) -> bool:
        """
            Sends an HTTP GET request to the specified URL in the healthcheck parameter to verify its accessibility.

            :param healthcheck: An instance of HealthCheckOptions which contains the URL ('address') to be tested.
            :return: True if the HTTP response status code is between 200 and 399, indicating successful contact.
                     False if the status code is outside this range or an error occurs during the request.

            """
        try:
            logger.debug(f"Http request: {healthcheck.target_url}")
            response = requests.get(healthcheck.target_url, timeout=self._REQUEST_TIMEOUT)
            if 200 <= response.status_code < 400:
                return True
            else:
                return False
        except requests.RequestException:
            logger.debug(f"Validate. Error occurred during requesting URL {healthcheck.target_url}.")
            return False
