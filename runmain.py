# -*- coding: utf-8 -*-

# dev
# dk
# python c:\work\github\dkcoverage\runmain.py
import glob

import time
from src import dkcoverage
from src.testenv import TestEnvironment
from src.testsuite import TestSuite

if __name__ == "__main__":
    tsuite = TestSuite()
    env = TestEnvironment(tsuite)

    # # tf1 = dkcoverage.Testfile('tt3/tests/test_dg_checkin.py')
    # # tf2 = dkcoverage.Testfile('tt3/tests/test_dg_empday.py')
    # tests = [dkcoverage.Testfile(f) for f in glob.glob('tt3/tests/test_*.py')]
    #
    # tr = dkcoverage.TestRun()
    # for tst in tests:
    #     tr.start(tst)
    #
    # while tr._running:
    #     tr.check_running()
    #     time.sleep(1)
    #
    # for tst in tests:
    #     print tst
    #     print
