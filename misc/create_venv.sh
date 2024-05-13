#!/bin/bash
# Copyright (c) 2024 ghostkaa
# Author: ghostkaa
# License: MIT
# https://github.com/ghostkaa/pxpilot/raw/main/LICENSE

VENV_NAME=$1

echo "Creating a virtual environment and installing dependencies..."
python3 -m venv "$VENV_NAME"
. "$VENV_NAME"/bin/activate
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Failed to install Python dependencies."
    exit 1
fi
deactivate