import pytest
from unittest.mock import Mock, patch

from pxvmflow.config import *
from pxvmflow.executor import Executor
from pxvmflow.consts import ProxmoxType


@pytest.fixture
def mock_config():
    return ProxmoxConfig(
        url='http://fake-url.com',
        port=8006,
        realm='pam',
        token_id='test-token-id',
        token_secret='test-token-secret',
        user='user',
        password='password',
        verify_ssl=False,
        start_options=[
            VMStartOptions(id=100, name="VM1", run_timeout=60, healthcheck=HealthCheckOptions(address="192.168.1.61", type="ping")),
            VMStartOptions(id=301, name="VM2", run_timeout=120, healthcheck=HealthCheckOptions(address="http://192.168.1.12/login", type="http"))
        ]
    )


class TestExecutor:
    @pytest.fixture
    def executor(self, mock_config):
        return Executor(mock_config)

    @pytest.fixture
    def mock_px_client(self):
        with patch('pxvmflow.pxtool.ProxmoxClient', autospec=True) as mock:
            yield mock

    def test_init(self, executor):
        #config = executor._config
        assert executor._host == 'http://fake-url.com'
        assert executor._port == 8006
        assert executor._user == 'user'
        assert executor._realm == 'pam'
        assert executor._password == 'password'
        assert not executor._verify_ssl

    def test_get_all_vm(self, executor, mock_px_client):
        mock_client = Mock()

        def get_side_effect(arg):
            if "lxc" in arg:
                return [{"vmid": "101", "status": "running"}, {"vmid": "103", "status": "paused"}]
            elif "qemu" in arg:
                return [{"vmid": "102", "status": "stopped"}, {"vmid": "104", "status": "suspended"}]
            return []

        mock_client.get.side_effect = get_side_effect
        mock_px_client.build_client.return_value = mock_client
        executor._px_client = mock_client

        vms = executor.get_all_vm("node1")

        assert len(vms) == 4
        assert all(isinstance(vm, ProxmoxVMInfo) for vm in vms)

        assert vms[0].id == 101
        assert vms[0].type == ProxmoxType.LXC
        assert vms[0].status == 'running'

        assert vms[1].id == 103
        assert vms[1].type == ProxmoxType.LXC
        assert vms[1].status == 'paused'

        assert vms[2].id == 102
        assert vms[2].type == ProxmoxType.QEMU
        assert vms[2].status == 'stopped'

        assert vms[3].id == 104
        assert vms[3].type == ProxmoxType.QEMU
        assert vms[3].status == 'suspended'
