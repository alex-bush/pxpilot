#!/bin/bash

PROJECT_DIR=$(pwd)

VENV_NAME="venv"
PYTHON_PATH="$PROJECT_DIR/$VENV_NAME/bin/python3"
SERVICE_NAME="pxpilot.service"
SERVICE_PATH="/etc/systemd/system/$SERVICE_NAME"

echo "Creating a virtual environment and installing dependencies..."
python3 -m venv $VENV_NAME
source $VENV_NAME/bin/activate
pip install -r requirements.txt
deactivate

echo "Creating a systemd service file in $SERVICE_PATH"
sudo bash -c "cat > $SERVICE_PATH" << EOF
[Unit]
Description=PxPilot Service
After=network.target

[Service]
Type=oneshot
User=root
WorkingDirectory=$PROJECT_DIR
ExecStart=$PYTHON_PATH -m pxpilot
RemainAfterExit=true

[Install]
WantedBy=multi-user.target
EOF

echo "Rebooting systemd and activating the service..."
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME

echo "Installation is complete! Service $SERVICE_NAME is configured for autorun."
