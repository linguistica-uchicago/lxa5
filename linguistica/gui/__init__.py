# -*- encoding: utf8 -*-

# ------------------------------------------------------------------------------
#
#   major windows:
#
#                               MainWindow
#       =====================================================================
#       |                          mainSplitter                             |
#       | ================================================================= |
#       | | minorSplitter  |                MajorDisplay                  | |
#       | | ============== | ============================================ | |
#       | | |            | | |                                          | | |
#       | | |            | | |                                          | | |
#       | | |            | | |                                          | | |
#       | | |TreeWidget  | | |                                          | | |
#       | | |(lexicon)   | | |                                          | | |
#       | | |            | | |                                          | | |
#       | | |============| | |                                          | | |
#       | | |parameter   | | |                                          | | |
#       | | |window      | | |                                          | | |
#       | | ============== | ============================================ | |
#       | ================================================================= |
#       =====================================================================
#
#   How things work in general:
#
#   When a corpus text file is specified, the program checks if the expected
#   output files are there. (If not, the various components
#   {ngram, lxa5, manifold, ...}.py will be run to generate the output files.)
#
#   Then the lexicon is initialized and shown in the TreeWidget.
#   The lexicon shows names of things that the user can click.
#   The major display and parameter window change according to what has been
#   clicked.
# ------------------------------------------------------------------------------

# It is important to get PyQt5 for the python 3 distribution of your system.
# if you're on ubuntu, do the following to get PyQt5:
# sudo apt-get install python3-sip python3-pyqt5 python3-pyqt5.qtwebkit
# -- Jackson Lee, 2015-08-19

import sys
import os
import time

try:
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import (QApplication, QSplashScreen)
    from PyQt5.QtGui import QPixmap
    from linguistica.gui.main_window import MainWindow
except ImportError:
    Qt = None
    QApplication = None
    QSplashScreen = None
    QPixmap = None
    MainWindow = None

from linguistica import __version__


def main():
    app = QApplication(sys.argv)
    app.setStyle('cleanlooks')
    app.setApplicationName("Linguistica")

    # Get screen resolution
    # Why do we need to know screen resolution?
    # Because this information is useful for setting the size of particular
    # widgets, e.g., the webview for visualizing the word neighbor manifold
    # (the bigger the webview size, the better it is for visualization!)
    resolution = app.desktop().screenGeometry()
    screen_width = resolution.width()
    screen_height = resolution.height()

    # create and display splash screen
    splash_image_path = os.path.join(os.path.dirname(__file__),
                                     'lxa_splash_screen.png')
    splash_image = QPixmap(splash_image_path)
    splash_screen = QSplashScreen(splash_image, Qt.WindowStaysOnTopHint)
    splash_screen.setMask(splash_image.mask())
    splash_screen.show()
    app.processEvents()
    time.sleep(2)

    # launch graphical user interface
    form = MainWindow(screen_height, screen_width, __version__)
    form.show()
    splash_screen.finish(form)
    app.exec_()
