import argparse

from .__about__ import __version__
from pxpilot.pilot import main
from pxpilot.config_validator import validate_config


if __name__ == "__main__":
    print(f"Running pxpilot version '{__version__}'")

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--validate_config", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument("-s", "--status_mode", action=argparse.BooleanOptionalAction, default=False)
    args = parser.parse_args()

    if args.validate_config:
        validate_config()
    else:
        main(args.status_mode)
