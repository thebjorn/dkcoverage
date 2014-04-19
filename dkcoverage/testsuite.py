# -*- coding: utf-8 -*-

"""All available tests == test suite.
"""

# import os
from pathlib import Path
from . import dkenv, testfile


class TestSuite(object):
    def __init__(self, dkroot=dkenv.DKROOT):
        """Use py.test --collectonly to find all test files.
           Yield the largest first (in the hope that long running tests will get
           started early in the test run.
        """
        self.root = Path(dkroot)
        self.test_modules = [testfile.Testfile(f)
                             for f in self.root.glob('**/test_*.py')]

    def __len__(self):
        return len(self.test_modules)

    def __iter__(self):
        return iter(self.test_modules)
