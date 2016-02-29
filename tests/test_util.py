# -*- encoding: utf8 -*-

from linguistica.util import (vprint, check_py_version)

def test_vprint():
    assert vprint('x', verbose=False) is None
    assert vprint('x', verbose=True) is None

def test_check_py_version():
    assert check_py_version() is None
