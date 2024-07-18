import argparse
import sys

from api import api as fast_api
from pxpilot import logging_config
from pxpilot.common import config_validator
from pxpilot.pilot import start
from .__about__ import __version__

CONFIG_FILE = "config.yaml"


def main():
    print(f"Running pxpilot version '{__version__}'")

    logging_config.setup_logging()

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--validate_config", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument("-a", "--api", action=argparse.BooleanOptionalAction, default=False)
    args = parser.parse_args()

    if args.validate_config:
        config_validator.validate_config(CONFIG_FILE)
        sys.exit(0)
    elif args.api:
        import uvicorn

        uvicorn.run(fast_api, host="0.0.0.0", port=8000)
        sys.exit(0)

    start(CONFIG_FILE)
