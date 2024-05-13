import argparse

from pxpilot.pilot import main

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--validate_config", action=argparse.BooleanOptionalAction)
    args = parser.parse_args()

    if args.validate_config is None:
        main()
        exit(0)

    print("Validate config")
    pass
