import argparse
import sys

from core import logging_config
from pxpilot.config import config_validator
from pxpilot.pilot import start_from_config
from core.__about__ import __version__

# from api import api as fast_api


CONFIG_FILE = "config.yaml"


def main():
    print(f"Running pxpilot cli version '{__version__}'")

    logging_config.setup_logging()

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--validate_config", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument("-a", "--api", action=argparse.BooleanOptionalAction, default=False)
    args = parser.parse_args()

    if args.validate_config:
        config_validator.validate_config(CONFIG_FILE)
        sys.exit(0)
    # elif args.api:
    #     import uvicorn
    #
    #     uvicorn.run(fast_api, host="0.0.0.0", port=8000)
    #     sys.exit(0)

    start_from_config(CONFIG_FILE)
