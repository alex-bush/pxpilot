import argparse

from .__about__ import __version__
from pxpilot.pilot import main, validate_config


if __name__ == "__main__":
    print(f"Running pxpilot version '{__version__}'")

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--validate_config", action=argparse.BooleanOptionalAction)
    args = parser.parse_args()

    if args.validate_config is None:
        main()
    else:
        validate_config()
