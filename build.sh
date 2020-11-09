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

# build wheels
DOCKER_IMAGE=quay.io/pypa/manylinux2014_x86_64
PLAT=manylinux2014_x86_64
docker run --rm -e PLAT=$PLAT -v `pwd`:/io $DOCKER_IMAGE $PRE_CMD /io/build-wheels.sh
