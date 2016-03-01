# -*- encoding: utf8 -*-

import sys
import shutil
import subprocess


# determine the nosetests command

if shutil.which('nosetests3'):
    nosetests_command = 'nosetests3'
elif shutil.which('nosetests'):
    nosetests_command = 'nosetests'
else:
    sys.exit('Error: The Python library "nose" is not installed.')

# run nosetests

subprocess.call((nosetests_command, '--where=tests', '--with-coverage', '-v'))
