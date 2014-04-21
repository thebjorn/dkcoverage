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
    def __init__(self, src):
        """fname should be relative to DKROOT.
        """
        self.src = src
        # self.appname = pth.parts[0]
        # self.file = PathInfo(pth)
        # self.cache = CacheInfo(self.appname, self.file)
        self.timer = Timer()
        self.result = None
        # self.imports = []

    # def write_status(self):
    #     """Write status info to status.txt in cache directory.
    #     """
    #     assert self.cache.abspath
    #     with open(os.path.join(self.cache.abspath, 'status.txt'), 'w') as fp:
    #         fp.write(json.dumps(self, sort_keys=True,
    #                             default=lambda o: o.__dict__,
    #                             indent=4))

    def run_test(self, testenv=None):
        "Spawn a process to run this test."
        cd = testenv.cache if testenv else ''
        creldir = os.path.join(self.src.appname, self.src.name if self.src.appname else self.src.name)
        cachedir = path.make_path(os.path.join(cd, creldir))
        #self.cache.abspath = path.make_path(os.path.join(cd, self.cache.reldir))

        env = copy.copy(os.environ)
        env['DKMAILNAME'] = os.path.join(cachedir, self.src.name)
        cmd = dkenv.COVERAGE.replace('{FILENAME}', self.src.absname)
        cmd = cmd.replace('{WORKDIR}', os.path.join(cachedir, 'pytestlog.txt').replace('\\', '/'))
        # print "CMD:", cmd
        self.timer.begin()
        self.result = subprocess.Popen(
            shlex.split(cmd),
            stdout=subprocess.PIPE,
            stderr=open(os.devnull, 'w'),
            cwd=cachedir,
            env=env).communicate()[0]
        self.timer.end()
        # self.write_status()

    # def __str__(self):
    #     return self.file.relname
    #
    # def __repr__(self):
    #     import pprint
    #     return pprint.pformat(self.__dict__)


# if __name__ == "__main__":
#     Testfile(sys.argv[1]).run_test()
