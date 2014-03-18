# -*- coding: utf-8 -*-

"""All available tests == test suite.
"""
import copy
import json
import os
from . import dkenv, path
import shlex
import subprocess
import time


class Testfile(object):
    def __init__(self, fname):
        """fname should be relative to DKROOT.
        """
        self.relname = fname
        self.absname = path.normpath(os.path.join(dkenv.DKROOT, fname), '/')
        self.path, self.filename = os.path.split(self.absname)
        self.name, self.ext = os.path.splitext(self.filename)
        self.abscache = None
        self.cachename = self.relname.replace('\\', '/').replace('/', '$')[:-3]
        self.start = self.end = self.elapsed = self.result = None

    def write_status(self):
        assert self.abscache
        with open(os.path.join(self.abscache, 'status.txt'), 'w') as fp:
            fp.write(json.dumps(self.__dict__, indent=4))

    def run(self, testenv):
        "Spawn a process to run this test."
        env = copy.copy(os.environ)
        env['DKMAILNAME'] = os.path.join(testenv.work, self.cachename, self.name)
        cmd = dkenv.COVERAGE.replace('{FILENAME}', self.filename)
        self.start = time.time()
        self.result = subprocess.Popen(
            shlex.split(cmd),
            stdout=subprocess.PIPE,
            stderr=open(os.devnull, 'w'),
            cwd=self.abscache,
            env=env).communicate()[0]
        self.end = time.time()
        self.elapsed = self.end - self.start

    def __str__(self):
        return self.relname

    def __repr__(self):
        import pprint
        return pprint.pformat(self.__dict__)
