#!/bin/bash

VERSION="0.1.2"
GITHUB_REPO="https://github.com/ghostkaa/pxpilot"
RELEASE_URL="$GITHUB_REPO/archive/refs/tags/v$VERSION.tar.gz"
TAR_FILE="pxpilot.tar.gz"
UNZIP_DIR="pxpilot-$VERSION"

echo "Downloading the latest release from $RELEASE_URL ..."
wget "$RELEASE_URL" -O $TAR_FILE

echo "Extracting the downloaded file..."
tar -xzf $TAR_FILE

echo "Changing directory to $UNZIP_DIR..."
cd $UNZIP_DIR || exit

echo "Running setup_service.sh script..."
bash setup_service.sh

echo "Cleanup downloaded and temporary files..."
cd ..
#rm -rf $TAR_FILE $UNZIP_DIR

echo "Installation and setup completed!"
