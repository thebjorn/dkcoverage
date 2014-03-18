# -*- coding: utf-8 -*-

"""Setup the test environment so it's ready to start running tests.
"""

import os
from . import shell, dkenv, path, rtestcover
import sys
import time
import copy
import os
from . import dkenv
import shlex
import subprocess
import multiprocessing
import datetime
from .path import make_path, normpath, timestamp


class TestEnvironment(object):
    def __init__(self, suite):
        self.timestamp = datetime.datetime.now()
        # Create work folder
        os.chdir(dkenv.DKROOT)
        self.work = make_path(os.path.join('_coverage', '_covroot'))
        os.chdir(self.work)
        self.cache = make_path('cache')
        os.chdir(self.cache)

        for i, tfile in enumerate(suite):
            tfile.abscache = make_path(tfile.cachename)
            print "running:", tfile
            tfile.write_status()
            #tfile.run(self)
            if i > 5:
                break

        # self.test_output = make_path(os.path.join(work, 'test_output'))
        # self._covcache = make_path(os.path.join(work, '_covcache'))
        # self.emails = make_path(os.path.join(work, 'emails'))
        # self.logs = make_path(os.path.join(work, 'logs'))
        # self.work = canonical_path(os.path.join(dkenv.DKROOT, work))


