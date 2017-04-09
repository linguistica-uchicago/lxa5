#!/usr/bin/env python3
# -*- encoding: utf8 -*-

import sys

import linguistica as lxa
from linguistica.cli import main as cli_main

try:
    from linguistica.gui import main as gui_main
    pyqt5_available = True
except ImportError:
    gui_main = None
    pyqt5_available = False

lxa_version = lxa.__version__


def main():
    # --------------------------------------------------------------------------
    # ensure lxa_mode is one of the modes in MODES

    MODES = {'cli', 'gui'}

    try:
        lxa_mode = sys.argv[1].lower()
    except IndexError:
        lxa_mode = None
        error_msg_template = 'Error: no running mode specified.' \
                             '\n\nRun one of the following:\n\n{}'

        sys.exit(error_msg_template.format(
            '\n'.join('linguistica ' + mode for mode in sorted(MODES))))

    if lxa_mode not in MODES:
        sys.exit('Unrecognized mode: ' + sys.argv[1])

    # --------------------------------------------------------------------------
    # launch graphical user interface

    if lxa_mode == 'gui':

        if pyqt5_available:
            print('Running the graphical user interface of Linguistica {}...'
                  .format(lxa_version))
            gui_main()

        else:
            sys.exit('Unable to import PyQt5. '
                     'Graphical user interface cannot be launched.')

    # --------------------------------------------------------------------------
    # launch command line interface

    if lxa_mode == 'cli':
        cli_main()


if __name__ == '__main__':
    main()
