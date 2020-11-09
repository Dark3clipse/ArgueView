#!/bin/bash
set -e
pipenv-setup sync
python3 setup.py sdist

DOCKER_IMAGE=quay.io/pypa/manylinux2014_x86_64
PLAT=manylinux1_x86_64
docker run --rm -e PLAT=$PLAT -v `pwd`:/io $DOCKER_IMAGE $PRE_CMD /io/build-wheels.sh
