import argparse

import pxpilot
from pxpilot import logging_config
from pxpilot.common import config_validator
from .__about__ import __version__


CONFIG_FILE = "config.yaml"

if __name__ == "__main__":
    print(f"Running pxpilot version '{__version__}'")
    logging_config.setup_logging()

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--validate_config", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument("-s", "--status_mode", action=argparse.BooleanOptionalAction, default=False)
    args = parser.parse_args()

    if args.validate_config:
        config_validator.validate_config(CONFIG_FILE)
    else:
        pxpilot.start(CONFIG_FILE)
