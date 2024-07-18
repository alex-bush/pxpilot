class ProxmoxError(Exception):
    pass


class ProxmoxConfigurationError(ProxmoxError):
    pass


class FatalProxmoxError(ProxmoxError):
    pass
