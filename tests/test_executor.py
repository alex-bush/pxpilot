import pytest
from unittest.mock import Mock, patch

from pxpilot.config import *
from pxpilot.executor import Executor
from pxpilot.consts import VMType


@pytest.fixture
def mock_config():
    return ProxmoxSettings(
        url='http://fake-url.com',
        port=8006,
        realm='pam',
        token_id='test-token-id',
        token_secret='test-token-secret',
        user='user',
        password='password',
        verify_ssl=False,
        start_options=[
            VMStartOptions(vm_id=100, node="node1", healthcheck=HealthCheckOptions(
                target_url="192.168.1.61", check_method="ping")),
            VMStartOptions(vm_id=301, node="node1", healthcheck=HealthCheckOptions(
                target_url="http://192.168.1.12/login", check_method="http"))
        ]
    )


class TestExecutor:
    @pytest.fixture
    def executor(self, mock_config):
        return Executor(mock_config)

    @pytest.fixture
    def mock_px_client(self):
        with patch('pxpilot.pxtool.ProxmoxClient', autospec=True) as mock:
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
        #assert all(isinstance(vm, dict) for vm in vms)

        assert vms[101].vm_id == 101
        assert vms[101].vm_type == VMType.LXC
        assert vms[101].status == 'running'

        assert vms[103].vm_id == 103
        assert vms[103].vm_type == VMType.LXC
        assert vms[103].status == 'paused'

        assert vms[102].vm_id == 102
        assert vms[102].vm_type == VMType.QEMU
        assert vms[102].status == 'stopped'

        assert vms[104].vm_id == 104
        assert vms[104].vm_type == VMType.QEMU
        assert vms[104].status == 'suspended'

        executor._px_client.get.assert_any_call("nodes/node1/lxc")
        executor._px_client.get.assert_any_call("nodes/node1/qemu")
