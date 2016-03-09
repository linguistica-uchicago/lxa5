#!/bin/bash

# modified from https://github.com/rhiever/tpot

# This script is called by the "install" step defined in
# .travis.yml. See http://docs.travis-ci.com/ for more details.
# The script is to install all dependencies for both the Linguistica library
# and its tests.

set -e

# Fix the compilers to workaround avoid having the Python 3.4 build
# lookup for g++44 unexpectedly.
export CC=gcc
export CXX=g++

# Use the miniconda installer for faster download / install of conda
# itself
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    -O miniconda.sh
chmod +x miniconda.sh && ./miniconda.sh -b
export PATH=/home/travis/miniconda/bin:$PATH
conda update --yes conda

conda create -n testenv --yes python=$PYTHON_VERSION numpy scipy networkx

source activate testenv

# Install packages for running tests and measuring test coverage
python -m pip install python-coveralls coverage nose

# Install Linguistica
python setup.py install
