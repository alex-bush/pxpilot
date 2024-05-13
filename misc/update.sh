#!/bin/bash
# Copyright (c) 2024 ghostkaa
# Author: ghostkaa
# License: MIT
# https://github.com/ghostkaa/pxpilot/raw/main/LICENSE

VENV_NAME="venv"
GITHUB_REPO="https://github.com/ghostkaa/pxpilot"
TAR_FILE="pxpilot.tar.gz"
PROJECT_DIR="pxpilot"
BACKUP_DIR="${PROJECT_DIR}_backup"
UPDATE_DIR="pxpilot_update"

echo "Downloading the latest release..."
bash download_latest.sh $GITHUB_REPO $TAR_FILE
#wget "$RELEASE_URL" -O $TAR_FILE

if [ -d "$UPDATE_DIR" ]; then
    echo "Removing existing directory $UPDATE_DIR..."
    rm -rf "$UPDATE_DIR"
fi
mkdir $UPDATE_DIR

echo "Extracting the downloaded file to $UPDATE_DIR..."
tar -xzf $TAR_FILE --strip-components=1 -C $UPDATE_DIR

echo "Copying config file from $PROJECT_DIR to $UPDATE_DIR..."
cp -f $PROJECT_DIR/config.yaml $UPDATE_DIR/config.yaml

if [ -d "$BACKUP_DIR" ]; then
    echo "Removing existing directory $BACKUP_DIR..."
    rm -rf "$BACKUP_DIR"
fi

mv $PROJECT_DIR $BACKUP_DIR
mv $UPDATE_DIR $PROJECT_DIR

bash misc/create_venv.sh $VENV_NAME

echo "All done"
