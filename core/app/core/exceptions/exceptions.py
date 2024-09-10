class NotFoundError(Exception):
    def __init__(self, message: str = "Not found"):
        self.message = message
        super().__init__(self.message)


class DatabaseError(Exception):
    def __init__(self, message: str = "Not found"):
        self.message = message
        super().__init__(self.message)


class ProxmoxError(Exception):
    pass


class ProxmoxConfigurationError(ProxmoxError):
    pass


class FatalProxmoxError(ProxmoxError):
    pass


class HttpError(Exception):
    def __init__(self, message: str = "", status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

    status_code: int


class NotAuthorizedError(HttpError):
    def __init__(self, message: str = "Not Authorized", status_code: int = 401):
        super().__init__(message, status_code)


class SettingsError(Exception):
    pass


class ArgumentError(Exception):
    pass
