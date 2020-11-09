#!/bin/bash
set -e
pipenv-setup sync
python setup.py sdist
