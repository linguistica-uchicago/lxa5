"""Smoke tests for the PyQt5 GUI.

These self-skip when PyQt5 / PyQtWebEngine are not installed (the default for the
core test suite and CI ``test`` job). A dedicated headless ``gui`` CI job installs
the ``gui`` extra and runs them under ``QT_QPA_PLATFORM=offscreen``.
"""

import os

import pytest

# Run headless so the tests never pop a real window (locally or in CI).
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

pytest.importorskip("PyQt5")
pytest.importorskip("PyQt5.QtWebEngineWidgets")


def test_gui_imports():
    # The GUI fails to import as a whole if QWebEngineView (PyQtWebEngine) is
    # missing, so importing MainWindow exercises the real dependency chain.
    from linguistica.gui.main_window import MainWindow
    from PyQt5.QtWebEngineWidgets import QWebEngineView

    assert MainWindow is not None
    assert QWebEngineView is not None


@pytest.fixture(scope="module")
def qapp():
    from PyQt5.QtWidgets import QApplication

    app = QApplication.instance() or QApplication([])
    yield app


def test_qwebengineview_instantiates(qapp):
    # Confirms the Qt + Chromium (QtWebEngine) stack actually initializes, not
    # just that the import resolves.
    from PyQt5.QtWebEngineWidgets import QWebEngineView

    view = QWebEngineView()
    assert view is not None
