import pytest
from unittest.mock import patch, mock_open

import yaml
from yaml.parser import ParserError

from pxvmflow.config import VmFlowConfig, ValidationType, HealthCheckOptions, ProxmoxConfig


def test_successful_load():
    test_yaml_content = """
proxmox_config:
  url: 'http://example.com'
  port: 8006
  realm: 'test_realm'
  token_id: 'test_token'
  token_secret: 'secret'
  user: 'admin'
  password: 'password'
  verify_ssl: False
vms:
  - id: 1
    node: 'node1'
    healthcheck:
      address: 'http://127.0.0.1/ping'
      type: 'ping'
"""

    with patch("builtins.open", mock_open(read_data=test_yaml_content)):
        with patch("yaml.safe_load", return_value=yaml.safe_load(test_yaml_content)):
            config = VmFlowConfig().load("fake_path")
            assert isinstance(config, ProxmoxConfig)
            assert config.url == 'http://example.com'
            assert len(config.start_options) == 1
            assert config.start_options[0].healthcheck.type == ValidationType.PING


def test_yaml_parse_error():
    with patch("builtins.open", mock_open(read_data="invalid_yaml: :")):
        with patch("yaml.safe_load", side_effect=ParserError):
            #with patch("pxvmflow. logging_config") as mock_logger:
            config = VmFlowConfig().load("fake_path")
            assert config is None
                #mock_logger.exception.assert_called_once()


def test_healthcheck_parsing():
    test_yaml_content = """
proxmox_config:
  url: 'http://example.com'
  port: 8006
  realm: 'test_realm'
  token_id: 'test_token'
  token_secret: 'secret'
  user: 'admin'
  password: 'password'
  verify_ssl: False
vms:
  - id: 1
    node: 'node1'
    healthcheck:
      address: 'http://127.0.0.1/ping'
      type: 'ping'
"""

    with patch("builtins.open", mock_open(read_data=test_yaml_content)):
        with patch("yaml.safe_load", return_value=yaml.safe_load(test_yaml_content)):
            config = VmFlowConfig().load("fake_path")
            vm_healthcheck = config.start_options[0].healthcheck
            assert isinstance(vm_healthcheck, HealthCheckOptions)
            assert vm_healthcheck.address == 'http://127.0.0.1/ping'
            assert vm_healthcheck.type == ValidationType.PING
