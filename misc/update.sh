#!/bin/bash
# Copyright (c) 2024 ghostkaa
# Author: ghostkaa
# License: MIT
# https://github.com/ghostkaa/pxpilot/raw/main/LICENSE

VERSION="0.1.3"
GITHUB_REPO="https://github.com/ghostkaa/pxpilot"
RELEASE_URL="$GITHUB_REPO/archive/refs/tags/v$VERSION.tar.gz"
TAR_FILE="pxpilot.tar.gz"
PROJECT_DIR="pxpilot"
BACKUP_DIR="${PROJECT_DIR}_backup"
UPDATE_DIR="pxpilot"

echo "Downloading the latest release from $RELEASE_URL ..."
wget "$RELEASE_URL" -O $TAR_FILE

if [ -d "$UPDATE_DIR" ]; then
    echo "Removing existing directory $UPDATE_DIR..."
    rm -rf "$UPDATE_DIR"
fi
mkdir $UPDATE_DIR

echo "Extracting the downloaded file..."
tar -xzf $TAR_FILE --strip-components=1 -C $UPDATE_DIR

echo "Copying config file..."
cp -f $PROJECT_DIR/config.yml $UPDATE_DIR/config.yml

if [ -d "$BACKUP_DIR" ]; then
    echo "Removing existing directory $BACKUP_DIR..."
    rm -rf "$BACKUP_DIR"
fi

mv $PROJECT_DIR $BACKUP_DIR
mv $UPDATE_DIR $PROJECT_DIR
