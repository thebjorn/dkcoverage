# -*- coding: utf-8 -*-

"""Called from datakortet\dkcoverage.bat to record regression test
   coverage data in dashboard.
"""

import re
import os
# import sys
# import time
import glob
# from datakortet.dkdash.status import send_status
# from datakortet.utils import root
from coverage import coverage, misc
from coverage.files import find_python_files
from coverage.parser import CodeParser
from coverage.config import CoverageConfig
from . import dkenv


def linecount(fname, excludes):
    """Return the number of lines in ``fname``, counting the same way that
       coverage does.
    """
    cp = CodeParser(filename=fname,
                    exclude=re.compile(misc.join_regex(excludes)))
    lines, excluded = cp.parse_source()
    return len(lines), len(excluded)


def skiplist():
    cov = coverage(config_file=os.path.join(dkenv.DKROOT, '.coveragerc'))
    cwd = os.getcwd()
    skippatterns = [os.path.normpath(p.replace(cwd, dkenv.DKROOT)) for p in cov.omit]
    _skiplist = []
    for pat in skippatterns:
        _skiplist += glob.glob(pat)
    return set(_skiplist)


def abspath(fname):
    # cwd = os.getcwd()
    res = os.path.normcase(
        os.path.normpath(
            os.path.abspath(fname)))  #.replace(cwd, root()))))
    return res


def valid_file(fname, _skiplist=None):
    _skiplist = _skiplist or skiplist()
    if fname.endswith('.py'):
        absfname = abspath(fname)
        if absfname not in _skiplist:
            fpath, name = os.path.split(fname)
            if name != '__init__.py' or os.stat(absfname).st_size > 0:
                return absfname
    return False


def python_files(folder):
    _skiplist = skiplist()
    for fname in find_python_files(folder):
        f = valid_file(fname, _skiplist)
        if f:
            yield f


def pylinecount(rt=None, verbose=False):
    """Count Python lines the same way that coverage does.
    """
    res = 0
    cov = coverage(config_file=os.path.join(dkenv.DKROOT, '.coveragerc'))
    rt = rt or dkenv.DKROOT
    _skiplist = skiplist()

    exclude_lines = cov.get_exclude_list()

    for fname in python_files(rt):
        if os.path.normpath(fname) not in _skiplist:
            lcount, excount = linecount(fname, exclude_lines)
            if verbose:
                print '%5d %5d   %s' % (lcount, excount, fname)
            res += lcount
        else:
            if verbose:
                print '-----', fname

    return res


# def report_test_coverage(reportline, dashboard=True):
#     start = time.time()
#     parts = reportline.split()
#
#     stmts = int(parts[1])
#     skipped = int(parts[2])
#     covered = stmts - skipped
#     print >> sys.stderr, "COVERED:", covered
#
#     linecount = pylinecount()
#     print >> sys.stderr, "TOTAL:  ", linecount
#
#     coverage = 100.0 * covered / linecount
#     severity = 'green'
#     if coverage < 85:
#         severity = 'yellow'
#     if coverage < 60:
#         severity = 'red'
#
#     sys.stdout.write("Coverage: " + str(coverage) + '\n')
#
#     if dashboard:
#         send_status(tag='code.testcov',
#                     value=coverage,
#                     duration=time.time() - start,
#                     server='appsrv')


# if __name__ == "__main__":
#     intxt = sys.stdin.read()
#     report_test_coverage(intxt)
#     sys.exit(0)
