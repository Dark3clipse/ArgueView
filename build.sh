#!/bin/bash
set -e

# import environment if exists
if test -f ".env"; then
  export $(cat .env | xargs)
fi

# sync pipenv dependencies to setup.py
pipenv-setup sync

# build source egg
python3 setup.py sdist

# build wheel
python3 setup.py sdist bdist_wheel
