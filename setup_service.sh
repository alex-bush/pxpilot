#!/bin/bash

if ! command -v sudo &>/dev/null; then
    apt-get update && apt-get install sudo -y
fi
sudo apt-get update
sudo apt-get install python3.11-venv python3-pip -y

PROJECT_DIR=$(cd $(dirname "$0") && pwd)

VENV_NAME="venv"
PYTHON_PATH="$PROJECT_DIR/$VENV_NAME/bin/python3"
SERVICE_NAME="pxpilot.service"
SERVICE_PATH="/etc/systemd/system/$SERVICE_NAME"

echo "Creating a virtual environment and installing dependencies..."
python3 -m venv $VENV_NAME
. $VENV_NAME/bin/activate
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Failed to install Python dependencies."
    exit 1
fi
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
if [ $? -ne 0 ]; then
    echo "Failed to enable the systemd service."
    exit 1
fi
#sudo systemctl start $SERVICE_NAME
#if [ $? -ne 0 ]; then
#    echo "Failed to start the systemd service."
#    exit 1
#fi

echo "Installation is complete! Service $SERVICE_NAME is configured for autorun."
