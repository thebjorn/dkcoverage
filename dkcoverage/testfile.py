# -*- coding: utf-8 -*-

"""All available tests == test suite.
"""

import sys
import copy
import json
import os
import shlex
import subprocess

from . import dkenv, path
from .utils.cacheinfo import CacheInfo
from .utils.pathinfo import PathInfo
from .utils.timer import Timer


class Testfile(object):
    def __init__(self, pth):
        """fname should be relative to DKROOT.
        """
        self.appname = pth.parts[0]
        self.file = PathInfo(pth)
        self.cache = CacheInfo(self.appname, self.file)
        self.timer = Timer()
        self.result = None
        self.imports = []

    def write_status(self):
        """Write status info to status.txt in cache directory.
        """
        assert self.cache.abspath
        with open(os.path.join(self.cache.abspath, 'status.txt'), 'w') as fp:
            fp.write(json.dumps(self, sort_keys=True,
                                default=lambda o: o.__dict__,
                                indent=4))

    def find_modules(self):
        """Find all the modules that this test imports.
        """
        # check this in a sub-process to not invalidate our own environment.
        cmd = 'python -c "import sys, %s;print sys.modules.keys()"'
        allimports = eval(subprocess.check_output(shlex.split(
            cmd % self.file.name),
            cwd=self.file.path
        ))
        self.imports = list(sorted(set(
            imp for imp in allimports
            if imp.startswith('datakortet.') and self.appname in imp
        )))

    def run_test(self, testenv=None):
        "Spawn a process to run this test."
        cd = testenv.cache if testenv else ''
        self.cache.abspath = path.make_path(os.path.join(cd, self.cache.reldir))

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


if __name__ == "__main__":
    Testfile(sys.argv[1]).run_test()
