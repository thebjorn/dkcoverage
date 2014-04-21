# -*- coding: utf-8 -*-

# dev
# dk
# python c:\work\github\dkcoverage\runmain.py
import time
from dkcoverage import db, findfiles, testsuite, testenv


if __name__ == "__main__":
    start = time.time()

    tests = set()
    cn = db.connect()
    for fname in findfiles.find_changed_files(cn):
        print
        if fname.is_test:
            print "Found changed test file:", fname
            fname.clear_dependencies()
            fname.save()  # finds dependencies and saves to db.
            tests.add(fname.relname)
        else:
            print "File changed:", fname, 'must run:'
            testfiles = findfiles.find_tests_to_run(fname, cn)
            for f in sorted(testfiles):
                print '    ', f
            tests |= testfiles

    print "\n\nPotential tests that need to be run..:"
    for t in sorted(tests):
        print '    ', t

    print
    print len(tests), 'tests to run..'

    tsuite = testsuite.TestSuite(tests)
    testenv.TestEnvironment(tsuite)

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
