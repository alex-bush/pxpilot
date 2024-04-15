from pythonping import ping

from enum import Enum, auto


class ValidationType(Enum):
    PING = auto
    HTTP_REQUEST = auto


class HostValidator:
    @staticmethod
    def validate(address, validation_type: ValidationType):
        if validation_type == ValidationType.PING:
            response = ping(address, count=1, verbose=True)
            if response == "Request timed out":
                return False
            return True
