#!/bin/bash
# Copyright (c) 2024 ghostkaa
# Author: ghostkaa
# License: MIT
# https://github.com/ghostkaa/pxpilot/raw/main/LICENSE

GITHUB_REPO="https://github.com/ghostkaa/pxpilot"
TAR_FILE="pxpilot.tar.gz"
UNZIP_DIR="pxpilot"

echo "Downloading the latest release..."

LATEST_RELEASE_URL=$(wget -S --spider "$GITHUB_REPO"/releases/latest 2>&1 | grep "Location:" | tail -n 1 | awk '{print $2}' | tr -d '\r')

if [ -z "$LATEST_RELEASE_URL" ]; then
    echo "Failed to retrieve the latest release URL."
    exit 1
fi

VERSION=$(echo "$LATEST_RELEASE_URL" | grep -oP 'tag/\K[^/]*')

if [ -z "$VERSION" ]; then
    echo "Failed to parse version from URL: $LATEST_RELEASE_URL"
    exit 1
fi

ARCHIVE_URL="$GITHUB_REPO/archive/refs/tags/$VERSION.tar.gz"

echo "Downloading file $ARCHIVE_URL..."
wget "$ARCHIVE_URL" -O "$TAR_FILE"

if [ $? -ne 0 ]; then
    echo "Failed to download the archive."
    exit 1
fi

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
