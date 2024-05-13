#!/bin/bash
# Copyright (c) 2024 ghostkaa
# Author: ghostkaa
# License: MIT
# https://github.com/ghostkaa/pxpilot/raw/main/LICENSE

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <GitHub Repository URL> <Output File>"
    exit 1
fi

LATEST_RELEASE_URL=$(wget -S --spider "$1"/releases/latest 2>&1 | grep "Location:" | tail -n 1 | awk '{print $2}' | tr -d '\r')

if [ -z "$LATEST_RELEASE_URL" ]; then
    echo "Failed to retrieve the latest release URL."
    exit 1
fi

VERSION=$(echo "$LATEST_RELEASE_URL" | grep -oP 'tag/\K[^/]*')

if [ -z "$VERSION" ]; then
    echo "Failed to parse version from URL: $LATEST_RELEASE_URL"
    exit 1
fi

ARCHIVE_URL="$1/archive/refs/tags/$VERSION.tar.gz"

echo "Downloading file $ARCHIVE_URL..."
wget "$ARCHIVE_URL" -O "$2"

if [ $? -ne 0 ]; then
    echo "Failed to download the archive."
    exit 1
fi

echo "Downloaded to $2"