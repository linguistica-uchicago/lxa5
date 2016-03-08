#!/bin/env bash

set -e

# This script is called by the "install" step defined in
# .travis.yml. See http://docs.travis-ci.com/ for more details.
# The script is to install all dependencies for both the Linguistica library
# and its tests.

# Deactivate the travis-provided virtual environment and setup a
# conda-based environment instead
deactivate

# Use the miniconda installer for faster download / install of conda
# itself
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    -O miniconda.sh
chmod +x miniconda.sh
./miniconda.sh -b -p $HOME/miniconda
export PATH="$HOME/miniconda/bin:$PATH"
conda config --set always_yes yes --set changeps1 no
conda update -q conda
conda info -a
conda create -q -n test-environment python=$TRAVIS_PYTHON_VERSION numpy scipy networkx

source activate test-environment
which python

# Install packages needed for running tests and measuring test coverage
python -m pip python-coveralls coverage nose
