from unittest.mock import MagicMock, patch

import logging
import pytest

from pxpilot.pxtool import VMService, VirtualMachine
from pxpilot.pxtool.models import VMType, VMState
from pxpilot.vm_management.host_validator import HostValidator
from pxpilot.vm_management.models import VMContext, StartStatus, VMLaunchSettings
from pxpilot.vm_management.vm_starter import VMStarter


@pytest.fixture
def mock_vm_service():
    mock_service = MagicMock(spec=VMService)
    return mock_service


@pytest.fixture
def mock_host_validator():
    mock_hv = MagicMock(spec=HostValidator)
    return mock_hv


@pytest.fixture
def mock_logger():
    with patch('pxpilot.logging_config.LOGGER', autospec=True) as mock_log:
        yield mock_log


@pytest.fixture
def mock_logger1():
    with patch('logging.getLogger', autospec=True) as mock_get_logger:
        logger = MagicMock(spec=logging.Logger)
        mock_get_logger.return_value = logger
        yield logger


def flow_item():
    context = VMContext(vm_id=100, status=StartStatus.UNKNOWN,
                        vm_info=VirtualMachine(vm_id=100, vm_type=VMType.LXC, node="test", name="test",
                                               status=VMState.STOPPED),
                        vm_launch_settings=VMLaunchSettings(vm_id=100, node="test"))
    return context


def test_start(mock_logger, mock_vm_service):
    starter = VMStarter(mock_vm_service, mock_host_validator)
    with patch.object(starter, '_start_vm_and_wait'):
        starter.start(flow_item())


def test_start_start_info_missed(mock_logger1, mock_vm_service, mock_host_validator):
    context = VMContext(vm_id=100, status=StartStatus.UNKNOWN,
                        vm_info=VirtualMachine(vm_id=100, vm_type=VMType.LXC, node="test", name="test",
                                               status=VMState.STOPPED),
                        vm_launch_settings=None)

    starter = VMStarter(mock_vm_service, mock_host_validator)
    with patch.object(starter, '_start_vm_and_wait', return_value=None) as mock_start_wait:
        result = starter.start(context)

        assert result.status == StartStatus.INFO_MISSED
        mock_start_wait.assert_not_called()


def test_start_disabled(mock_logger1, mock_vm_service, mock_host_validator):
    context = VMContext(vm_id=100, status=StartStatus.UNKNOWN,
                        vm_info=VirtualMachine(vm_id=100, vm_type=VMType.LXC, node="test", name="test",
                                               status=VMState.STOPPED),
                        vm_launch_settings=VMLaunchSettings(vm_id=100, node="test", enabled=False))

    starter = VMStarter(mock_vm_service, mock_host_validator)
    with patch.object(starter, '_start_vm_and_wait', return_value=None) as mock_start_wait:
        result = starter.start(context)

        assert result.status == StartStatus.DISABLED
        mock_start_wait.assert_not_called()


def test_start_already_runned(mock_logger1, mock_vm_service, mock_host_validator):
    context = VMContext(vm_id=100, status=StartStatus.STARTED,
                        vm_info=VirtualMachine(vm_id=100, vm_type=VMType.LXC, node="test", name="test",
                                               status=VMState.RUNNING),
                        vm_launch_settings=VMLaunchSettings(vm_id=100, node="test"))

    starter = VMStarter(mock_vm_service, mock_host_validator)
    with patch.object(starter, '_start_vm_and_wait', return_value=None) as mock_start_wait:
        result = starter.start(context)

        assert result.status == StartStatus.ALREADY_STARTED
        mock_start_wait.assert_not_called()
