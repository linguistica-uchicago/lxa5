# -*- encoding: utf8 -*-

import nose

print('Running nosetests...', flush=True)
nose.run(argv=['--where=tests', '--with-coverage', '-v'])
