#!/bin/bash
absolutepath=$(dirname "$0")
cd $absolutepath
git pull
cd ..
/usr/bin/python3 UAFAssets-updater/scripts/pallas-get-UAFAssets.py
