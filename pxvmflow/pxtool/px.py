import proxmoxer
from proxmoxer import ProxmoxAPI


class ProxmoxClient:
    _proxmox: ProxmoxAPI

    def __init__(self, host, port, user, realm, password, verify_ssl):
        self._host = host
        self._port = port
        self._user = user
        self._realm = realm
        self._password = password
        self._verify_ssl = verify_ssl

    def build_client(self):
        if "@" in self._user:
            user_id = self._user
        else:
            user_id = f"{self._user}@{self._realm}"

        self._proxmox = proxmoxer.ProxmoxAPI(
            self._host,
            port=self._port,
            user=user_id,
            password=self._password,
            verify_ssl=self._verify_ssl,
            timeout=30,
        )

        return self._proxmox

    def get_client(self):
        return self._proxmox

    def get(self, command):
        return self._proxmox(command).get()

    def post(self, command):
        return self._proxmox(command).post()
