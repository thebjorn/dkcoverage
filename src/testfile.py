# -*- coding: utf-8 -*-

"""All available tests == test suite.
"""
from collections import namedtuple
import copy
import json
import os
from . import dkenv, path
import re
import shlex
import subprocess
import time


class pset(dict):
    def __init__(self, *args, **kwargs):
        super(pset, self).__init__(*args, **kwargs)
        self.__dict__ = self


class PathInfo(object):
    def __init__(self, fname):
        self.relname = fname
        self.absname = path.normpath(os.path.join(dkenv.DKROOT, fname), '/')
        self.path, self.filename = os.path.split(self.absname)
        self.name, self.ext      = os.path.splitext(self.filename)


class CacheInfo(object):
    def __init__(self, appname, pinfo):
        self.abspath = None
        self.name = pinfo.relname.replace('\\', '/').replace('/', '$')[:-3]
        self.reldir = os.path.join(appname, self.name) if appname else self.name


class Timer(object):
    def __init__(self):
        self.start = self.stop = self.elapsed = None

    def begin(self):
        self.start = time.time()

    def end(self):
        self.stop = time.time()
        self.elapsed = self.stop - self.start
        return self.elapsed


import sys


def mods(): return {n for n in sys.modules.keys() if
                    '.' in n and not n.startswith('_')}

class Testfile(object):
    def __init__(self, fname):
        """fname should be relative to DKROOT.
        """
        self.appname = re.split(r'\\|/', fname, 1)[0]
        self.file = PathInfo(fname)
        self.cache = CacheInfo(self.appname, self.file)
        self.timer = Timer()
        self.result = None
        self.imports = []

    def write_status(self):
        assert self.cache.abspath
        with open(os.path.join(self.cache.abspath, 'status.txt'), 'w') as fp:
            fp.write(json.dumps(self, sort_keys=True,
                                default=lambda o:o.__dict__,
                                indent=4))

    def find_modules(self):
        allimports = eval(subprocess.check_output(shlex.split(
            'python -c "import sys, %s;print sys.modules.keys()"' % self.file.name),
            cwd=self.file.path
        ))
        # self.imports = list(sorted(set(imp for imp in allimports if imp.startswith('datakortet.'))))
        self.imports = list(sorted(set(imp for imp in allimports if self.appname in imp)))

    def run_test(self, testenv):
        "Spawn a process to run this test."
        self.cache.abspath = path.make_path(os.path.join(testenv.cache, self.cache.reldir))
        self.find_modules()
        # print "IMPORTS:", self.imports
        env = copy.copy(os.environ)
        env['DKMAILNAME'] = os.path.join(self.cache.abspath, self.file.name)
        cmd = dkenv.COVERAGE.replace('{FILENAME}', self.file.absname)
        cmd = cmd.replace('{WORKDIR}', os.path.join(self.cache.abspath, 'pytestlog.txt').replace('\\', '/'))
        # print "CMD:", cmd
        self.timer.begin()
        self.result = subprocess.Popen(
            shlex.split(cmd),
            stdout=subprocess.PIPE,
            stderr=open(os.devnull, 'w'),
            cwd=self.cache.abspath,
            env=env).communicate()[0]
        self.timer.end()
        self.write_status()

    def __str__(self):
        return self.file.relname

    def __repr__(self):
        import pprint
        return pprint.pformat(self.__dict__)
