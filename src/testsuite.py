# -*- coding: utf-8 -*-

"""All available tests == test suite.
"""

import os
from . import dkenv, testfile


class TestSuite(object):
    def __init__(self, dkroot=dkenv.DKROOT):
        """Use py.test --collectonly to find all test files.
           Yield the largest first (in the hope that long running tests will get
           started early in the test run.
        """
        self.test_modules = []
        for root, dirs, files in os.walk(dkroot):
            for d in dirs:
                if d.startswith(('_', '.')) or d in dkenv.SKIPDIRS:
                    dirs.remove(d)
            for f in files:
                if f.startswith('test_') and f.endswith('.py'):
                    abspath = os.path.join(root, f)
                    relpath = abspath[len(dkroot)+1:].replace('\\', '/')
                    self.test_modules.append(testfile.Testfile(relpath))

    def __len__(self):
        return len(self.test_modules)

    def __iter__(self):
        return iter(self.test_modules)
