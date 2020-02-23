#!/bin/bash
set -e

python3 -m venv .testenv
.testenv/bin/python -m pip install -r requirements.txt
