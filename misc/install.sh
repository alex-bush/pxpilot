#!/bin/bash
# Copyright (c) 2024 ghostkaa
# Author: ghostkaa
# License: MIT
# https://github.com/ghostkaa/pxpilot/raw/main/LICENSE

VERSION="0.1.4"
GITHUB_REPO="https://github.com/ghostkaa/pxpilot"
RELEASE_URL="$GITHUB_REPO/archive/refs/tags/v$VERSION.tar.gz"
TAR_FILE="pxpilot.tar.gz"
UNZIP_DIR="pxpilot"

echo "Downloading the latest release from $RELEASE_URL ..."
wget "$RELEASE_URL" -O $TAR_FILE

mkdir $UNZIP_DIR

echo "Extracting the downloaded file..."
tar -xzf $TAR_FILE --strip-components=1 -C $UNZIP_DIR

echo "Changing directory to $UNZIP_DIR..."
cd $UNZIP_DIR || exit

echo "Running setup_service.sh script..."
bash setup_service.sh

echo "Cleanup downloaded and temporary files..."
cd ..
#rm -rf $TAR_FILE $UNZIP_DIR

echo "Installation and setup completed!"
