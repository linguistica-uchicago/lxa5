#!/bin/bash

# based on:
# - https://github.com/rhiever/tpot
# - http://conda.pydata.org/docs/travis.html

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
chmod +x miniconda.sh
bash miniconda.sh -b -p $HOME/miniconda
export PATH="$HOME/miniconda/bin:$PATH"
conda config --set always_yes yes --set changeps1 no
conda update -q conda
# Useful for debugging any issues with conda
conda info -a

conda create -q -n testenv --yes python=$PYTHON_VERSION numpy scipy networkx

source activate testenv

# Install packages for running tests and measuring test coverage
python -m pip install python-coveralls coverage nose

# Install Linguistica
python --version
python -c "import numpy; print('numpy %s' % numpy.__version__)"
python -c "import scipy; print('scipy %s' % scipy.__version__)"
python -c "import networkx; print('networkx %s' % networkx.__version__)"
python setup.py install
