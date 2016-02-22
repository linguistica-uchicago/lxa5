#!/usr/bin/env python3
# -*- encoding: utf8 -*-

import sys

from linguistica.gui import main as gui_main

# ------------------------------------------------------------------------------
# ensure lxa_mode is one of the modes in MODES

MODES = {'cmd', 'gui'}

try:
    lxa_mode = sys.argv[1].lower()
except IndexError:
    lxa_mode = None
    error_msg_template = 'Error: mode not specified for running Linguistica.' \
                         '\n\nRun one of the following:\n\n{}'
    command_template = 'python3 -m linguistica {}'

    sys.exit(error_msg_template.format('\n'.join([command_template.format(mode)
                                                  for mode in sorted(MODES)])))

if lxa_mode not in MODES:
    sys.exit('Unrecognized mode: ' + sys.argv[1])

# ------------------------------------------------------------------------------
# GUI mode

if lxa_mode == 'gui':
    gui_main()

# ------------------------------------------------------------------------------
# command line mode

if lxa_mode == 'cmd':
    pass
