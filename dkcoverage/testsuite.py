# -*- coding: utf-8 -*-

"""All available tests == test suite.
"""

# import os
from pathlib import Path
from . import dkenv, testfile
from .findfiles import _all_files


class TestSuite(object):
    def __init__(self, tests):
        """Tests to run.
        """
        #print _all_files.keys()
        self.test_modules = [testfile.Testfile(_all_files[Path(f).absolute()])
                             for f in tests]

    def __len__(self):
        return len(self.test_modules)

    def __iter__(self):
        return iter(self.test_modules)
