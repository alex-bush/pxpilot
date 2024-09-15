import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

if __name__ == "__main__":
    from cli_pxpilot.main import main

    main()
