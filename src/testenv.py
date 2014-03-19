# -*- coding: utf-8 -*-

"""Setup the test environment so it's ready to start running tests.
"""

import os
from . import shell, dkenv, path, rtestcover
import sys
import threading
import time
import copy
import os
from . import dkenv
import shlex
import subprocess
import multiprocessing
import datetime
import psutil
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

        running = []
        def show_running():
            current = list(sorted(set(int(t.name.split('-')[1]) for t in threading.enumerate() if '-' in t.name)))
            if running != current:
                print len(current), current
                running[:] = current

        for i, tfile in enumerate(suite):
            show_running()
            while psutil.cpu_percent(.5) > 85 or threading.active_count() > 60:
                time.sleep(.5)

            threading.Thread(
                target=tfile.run_test,
                args=(self,)
            ).start()

        while 1:
            n = threading.active_count()
            if n == 1:
                break
            time.sleep(1)
            show_running()

        # self.test_output = make_path(os.path.join(work, 'test_output'))
        # self._covcache = make_path(os.path.join(work, '_covcache'))
        # self.emails = make_path(os.path.join(work, 'emails'))
        # self.logs = make_path(os.path.join(work, 'logs'))
        # self.work = canonical_path(os.path.join(dkenv.DKROOT, work))


