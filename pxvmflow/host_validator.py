import requests
from pythonping import ping

from pxvmflow.config import HealthCheckOptions, ValidationType
from pxvmflow.consts import LOGGER


class HostValidator:
    def validate(self, healthcheck: HealthCheckOptions) -> bool:
        if healthcheck.type.value == ValidationType.PING.value:
            return self.validate_ping(healthcheck)
        elif healthcheck.type.value == ValidationType.HTTP.value:
            return self.validate_request(healthcheck)

        LOGGER.debug("Unknown healthcheck type")
        return True

    def validate_ping(self, healthcheck: HealthCheckOptions) -> bool:
        try:
            LOGGER.debug(f"Ping: {healthcheck.address}")
            response = ping(healthcheck.address, count=1, verbose=True)
            return response.success()
        except ConnectionError as er:
            LOGGER.exception(er)
            return False

    def validate_request(self, healthcheck: HealthCheckOptions) -> bool:
        try:
            LOGGER.debug(f"Http request: {healthcheck.address}")
            response = requests.get(healthcheck.address, timeout=2)
            if 200 <= response.status_code < 400:
                return True
            else:
                return False
        except requests.RequestException as e:
            LOGGER.debug(f"Error checking URL {healthcheck.address}")
            return False
