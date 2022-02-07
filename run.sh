#!/bin/bash

set -e
set -x

python3 -m venv venv
source ./venv/bin/activate
python3 -m pip install --upgrade pip
pip3 install poetry==1.0.0
pip3 install PyInstaller==4.3
poetry install
# opencv has conflicting dependencies, so can't complete conflict resolution
pip3 install opencv-python

python3 main.py parameters.json

deactivate