#!/bin/bash
cd "$(dirname $0)"
echo "Switched to path $(dirname $0)"
git pull
cd ..
git pull
/usr/bin/python3 UAFAssets-Updater/scripts/pallas-get-UAFAssets.py
