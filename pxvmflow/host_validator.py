import requests
from pythonping import ping

from pxvmflow.config import HealthCheckOptions, ValidationType
from pxvmflow.exceptions import UnknownHealthcheckException
from pxvmflow.logging_config import LOGGER


class HostValidator:
    _PING_COUNT = 1
    _REQUEST_TIMEOUT = 2

    def validate(self, healthcheck: HealthCheckOptions) -> bool:
        if healthcheck.type.value == ValidationType.PING.value:
            return self.validate_ping(healthcheck)
        elif healthcheck.type.value == ValidationType.HTTP.value:
            return self.validate_request(healthcheck)

        raise UnknownHealthcheckException(f"Unknown healthcheck type: {healthcheck.type}")

    def validate_ping(self, healthcheck: HealthCheckOptions) -> bool:
        try:
            LOGGER.debug(f"Ping: {healthcheck.address}")
            response = ping(healthcheck.address, count=self._PING_COUNT, verbose=True)
            return response.success()
        except ConnectionError:
            LOGGER.debug(f"Validate. Error occurred during ping URL {healthcheck.address}.")
            return False

    def validate_request(self, healthcheck: HealthCheckOptions) -> bool:
        try:
            LOGGER.debug(f"Http request: {healthcheck.address}")
            response = requests.get(healthcheck.address, timeout=self._REQUEST_TIMEOUT)
            if 200 <= response.status_code < 400:
                return True
            else:
                return False
        except requests.RequestException:
            LOGGER.debug(f"Validate. Error occurred during requesting URL {healthcheck.address}.")
            return False
