#!/bin/bash
if ! command -v pipenv &> /dev/null
then
    pip install pipenv
fi
pipenv install --dev
pipenv-setup sync
python setup.py sdist
