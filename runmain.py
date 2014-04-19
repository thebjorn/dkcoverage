# -*- coding: utf-8 -*-

# dev
# dk
# python c:\work\github\dkcoverage\runmain.py

import time
from pathlib import Path
from dkcoverage import db, dkenv, srcfile


def file_changed(fname, cn, root):
    current = srcfile.Sourcefile(fname, root)
    dbver = srcfile.Sourcefile.fetch(fname, root, cn)
    return current != dbver


def find_changed_files(cn):
    root = Path(dkenv.DKROOT)
    for i, fname in enumerate(root.glob('**/*.py')):
        current = srcfile.Sourcefile(fname, root)
        dbver = srcfile.Sourcefile.fetch(fname, root, cn)
        # if 'afr\\models\\user' in str(fname.absolute()):
        #     print "..", i, fname
        #     print repr(current)
        #     print repr(dbver)
        #     print current == dbver
        if current != dbver:  # if changed..
            yield i, current


def find_tests_to_run(fname, cn):
    c = cn.cursor()
    c.execute("""
         select distinct srcfile
         from dependencies
         where imports = ?
    """, [fname.relname])
    res = set(rec[0] for rec in c.fetchall())
    # print fname.relname
    # print "FOUND:", res
    return res


if __name__ == "__main__":
    start = time.time()
    tests = set()
    cn = db.connect()
    for i, fname in find_changed_files(cn):
        # print i, fname
        print "File changed:", fname, 'must run:'
        testfiles = find_tests_to_run(fname, cn)
        for f in sorted(testfiles):
            print '    ', f
        tests |= testfiles

    print "\n\nPotential tests that need to be run..:"
    for t in sorted(tests):
        print '    ', t

    print
    print len(tests), 'tests to run..'

    # fname = Path('adofix.py').absolute()
    # root = Path(dkenv.DKROOT).absolute()
    # print "FNAME:", fname
    # print "ROOT:", root
    # a = srcfile.Sourcefile.fetch(fname, root, db.connect())
    # b = srcfile.Sourcefile(fname, root)
    # print a
    # print b
    # print "EQUAL:", a == b
    print 'done:', time.time() - start



#proj = Project()


    # wait for all threads to finish
    # for i, p in enumerate(procs):
    #     print "JOINING:", i
    #     p.join()


    # with open('proj.txt', 'w') as fp:
    #
    #     for fname in root.glob('**/*.py'):
    #         f = srcfile.Sourcefile(fname, root)
    #         #self.files[f.file.absname] = f
    #         val = jason.dumps(f)
    #         print >>fp, val
    #         print val
    #         fp.flush()
    # for i, f in enumerate(proj.pyfiles):
    #     print repr(f)
    #     print
    #     if i> 15: break

    #tsuite = TestSuite()
    #env = TestEnvironment(tsuite)

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
