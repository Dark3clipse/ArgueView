#!/bin/bash
set -e
pipenv-setup sync
python3 setup.py sdist
