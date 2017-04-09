# -*- encoding: utf8 -*-

from linguistica.util import vprint


def test_vprint():
    assert vprint(False, 'x') is None
    assert vprint(True, 'x') is None
