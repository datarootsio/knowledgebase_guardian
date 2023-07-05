#!/bin/bash

python3 -m venv contradiction_detection
source contradiction_detection/bin/activate
pip install -r pyproject.toml
source setup.sh
