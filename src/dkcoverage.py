# -*- coding: utf-8 -*-
import time
import copy
import os
from . import dkenv
import shlex
import subprocess
import multiprocessing
import datetime
from .path import make_path, normpath, timestamp

r"dktest --result-log \work\reslog.txt --ignore node_modules --cov . --cov-config ..\.coveragerc --cov-report term"



DKCONCURRENT = 5


class TestRun(object):
    def __init__(self):
        self.timestamp = datetime.datetime.now()
        # Create work folder
        os.chdir(dkenv.DKROOT)
        work = os.path.join('_coverage', timestamp())
        self.test_output = make_path(os.path.join(work, 'test_output'))
        self._covcache = make_path(os.path.join(work, '_covcache'))
        self.emails = make_path(os.path.join(work, 'emails'))
        self.logs = make_path(os.path.join(work, 'logs'))
        self.work = normpath(os.path.join(dkenv.DKROOT, work))
        os.chdir(self.work)
        self._running = {}

    def start(self, testfile):
        while self.check_running() > 5:
            time.sleep(.5)

        env = copy.copy(os.environ)
        env['DKMAILNAME'] = os.path.join(self.work, testfile.name)
        cmd = dkenv.COVERAGE.replace('{FILENAME}', testfile.filename)
        print 'CMD:', cmd

        testfile.start = time.time()
        p = subprocess.Popen(shlex.split(cmd),
                             stdout=subprocess.PIPE,
                             stderr=open(os.devnull, 'w'),
                             cwd=testfile.path,
                             env=env)
        self._running[p] = testfile

    def check_running(self):
        print "RUNNING:", [k.name for k in self._running.values()]
        procs = self._running.keys()
        for proc in procs:
            testfile = self._running[proc]
            retcode = proc.poll()
            if retcode is None:
                pass  # still running
            else:
                del self._running[proc]
                testfile.result(proc.stdout.read())
                testfile.stop = time.time()
                testfile.elapsed = testfile.stop - testfile.start
                print testfile
                print

        return len(self._running)
