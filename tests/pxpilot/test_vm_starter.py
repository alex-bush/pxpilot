from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from pxpilot.models.configuration.vm_start_settings import VmStartOptions, StartOptions
from pxpilot.models.px.vms import VMContext
from pxpilot.pxtool import VMService, VirtualMachine
from pxpilot.pxtool.models import VMType, VMState
from pxpilot.vm_management.host_validator import HostValidator
from pxpilot.vm_management.models import StartStatus, StartResult
from pxpilot.vm_management.vm_starter import VMStarter


@pytest.fixture
def mock_vm_service():
    mock_service = MagicMock(spec=VMService)
    return mock_service


@pytest.fixture
def mock_host_validator():
    mock_hv = MagicMock(spec=HostValidator)
    return mock_hv


def get_full_valid_vm_context():
    context = VMContext(vm_id=100,
                        status=StartStatus.UNKNOWN,
                        vm_info=VirtualMachine(
                            vm_id=100,
                            vm_type=VMType.LXC,
                            node="test",
                            name="test",
                            status=VMState.STOPPED),
                        vm_launch_settings=VmStartOptions(
                            vm_id=100,
                            startup_parameters=StartOptions(
                                startup_timeout=5,
                                await_running=True)
                        ))
    return context


class TestStartMethod:
    def test_start_executes_successfully(self, mock_vm_service, mock_host_validator):
        starter = VMStarter(mock_vm_service, mock_host_validator)
        with patch.object(starter, '_start_vm_and_wait',
                          return_value=StartResult(status=StartStatus.STARTED)) as mock_start_wait:
            result = starter.start(get_full_valid_vm_context())

            assert result.status == StartStatus.STARTED
            mock_start_wait.assert_called_once()

    def test_launch_settings_missing_returns_info_missing(self, mock_vm_service, mock_host_validator):
        context = VMContext(vm_id=100, status=StartStatus.UNKNOWN,
                            vm_info=VirtualMachine(vm_id=100, vm_type=VMType.LXC, node="test", name="test",
                                                   status=VMState.STOPPED),
                            vm_launch_settings=None)

        starter = VMStarter(mock_vm_service, mock_host_validator)
        with patch.object(starter, '_start_vm_and_wait', return_value=None) as mock_start_wait:
            result = starter.start(context)

            assert result.status == StartStatus.INFO_MISSED
            mock_start_wait.assert_not_called()

    def test_launch_disabled_returns_disabled(self, mock_vm_service, mock_host_validator):
        context = VMContext(vm_id=100, status=StartStatus.UNKNOWN,
                            vm_info=VirtualMachine(vm_id=100, vm_type=VMType.LXC, node="test", name="test",
                                                   status=VMState.STOPPED),
                            vm_launch_settings=VmStartOptions(vm_id=100, enabled=False))

        starter = VMStarter(mock_vm_service, mock_host_validator)
        with patch.object(starter, '_start_vm_and_wait', return_value=None) as mock_start_wait:
            result = starter.start(context)

            assert result.status == StartStatus.DISABLED
            mock_start_wait.assert_not_called()

    def test_already_started_returns_already_started(self, mock_vm_service, mock_host_validator):
        context = VMContext(vm_id=100, status=StartStatus.STARTED,
                            vm_info=VirtualMachine(vm_id=100, vm_type=VMType.LXC, node="test", name="test",
                                                   status=VMState.RUNNING),
                            vm_launch_settings=VmStartOptions(vm_id=100))

        starter = VMStarter(mock_vm_service, mock_host_validator)
        with patch.object(starter, '_start_vm_and_wait', return_value=None) as mock_start_wait:
            result = starter.start(context)

            assert result.status == StartStatus.ALREADY_STARTED
            mock_start_wait.assert_not_called()


class TestStartAndWaitMethod:
    @patch('time.sleep', return_value=None)
    def test_start_executes_successfully(self, mock_vm_service, mock_host_validator):
        starter = VMStarter(mock_vm_service, mock_host_validator)
        starter.check_healthcheck = MagicMock(return_value=True)

        result = starter._start_vm_and_wait(get_full_valid_vm_context())

        assert result.status == StartStatus.STARTED

    def test_start_executes_timeout(self, mock_vm_service, mock_host_validator):
        starter = VMStarter(mock_vm_service, mock_host_validator)
        starter.check_healthcheck = MagicMock(return_value=False)

        with patch('time.sleep', return_value=None):
            with patch.object(starter, '_get_now') as mock_now:
                mock_now.side_effect = [
                    datetime(2024, 1, 1, 12, 0, 0),
                    datetime(2024, 1, 1, 12, 0, 15)
                ]
                result = starter._start_vm_and_wait(get_full_valid_vm_context())

        assert result.status == StartStatus.TIMEOUT
        mock_now.assert_called()

    def test_start_without_wait(self, mock_vm_service, mock_host_validator):
        starter = VMStarter(mock_vm_service, mock_host_validator)
        starter.check_healthcheck = MagicMock(return_value=False)
        vm_context = get_full_valid_vm_context()
        vm_context.vm_launch_settings.startup_parameters.await_running = False

        with patch('time.sleep', return_value=None) as mock_timer:
            with patch.object(starter, '_get_now') as mock_now:
                result = starter._start_vm_and_wait(vm_context)

        assert result.status == StartStatus.STARTED
        assert result.start_time == result.end_time
        mock_timer.assert_not_called()
        mock_now.assert_called_once()
