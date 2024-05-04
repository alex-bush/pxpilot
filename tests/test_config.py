from unittest.mock import patch, mock_open

import pytest
import yaml

from pxpilot.config import ConfigManager
from pxpilot.vm_management.models import AppConfig

HOST_VALUE = "192.168.1.1:8006"
TOKEN_NAME_VALUE = "pxpilot@pve!pilot"
TOKEN_VALUE = "123"

VALID_CONFIG = f"""
proxmox_config:
  host: "{HOST_VALUE}"
  token: "{TOKEN_NAME_VALUE}"
  token_value: "{TOKEN_VALUE}"
  verify_ssl: false

settings:
  auto_start_dependency: false
  auto_shutdown: true
  self_host:
    vm_id: 100
    node: "px-test"
    type: "lxc"

notification_options:
  telegram:
    token: 1
    chat_id: 2
  email:
    email: test@email.com

vms:
  - vm_id: 100
    node: px-test
    dependencies: []
    enabled: true
    startup_parameters:
      await_running: true
      startup_timeout: 60
    healthcheck:
      target_url: "192.168.1.2"
      check_method: "ping"

  - vm_id: 101
    node: px-test
    startup_parameters:
      await_running: true
      startup_timeout: 10
    enabled: true
    dependencies: []
    healthcheck:
      target_url: "http://192.168.1.3/"
      check_method: "http"

  - vm_id: 102
    node: px-test
    enabled: true
    dependencies:
      - 101
"""


@pytest.fixture
def mock_file_open():
    with patch("builtins.open", mock_open(read_data=VALID_CONFIG)) as mock_file:
        with patch("yaml.safe_load", return_value=yaml.safe_load(VALID_CONFIG)) as mock_load:
            yield mock_file, mock_load


def test_load(mock_file_open):
    cman = ConfigManager()
    config = cman.load('fake_path')

    assert isinstance(config, AppConfig)
    assert config.proxmox_config.px_settings['host'] == HOST_VALUE
    assert config.proxmox_config.px_settings['token'] == TOKEN_NAME_VALUE
    assert config.proxmox_config.px_settings['token_value'] == TOKEN_VALUE

    assert len(config.notification_settings) == 2
    assert config.notification_settings['telegram']['token'] == 1
    assert config.notification_settings['telegram']["chat_id"] == 2

    assert len(config.proxmox_config.start_options) == 3
