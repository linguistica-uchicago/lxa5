# -*- encoding: utf8 -*-

from linguistica.util import (vprint, check_py_version)


def test_vprint():
    assert vprint(False, 'x') is None
    assert vprint(True, 'x') is None


def test_check_py_version():
    assert check_py_version() is None
