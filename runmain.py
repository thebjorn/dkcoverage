# -*- coding: utf-8 -*-

# dev
# dk
# python c:\work\github\dkcoverage\runmain.py

#from Queue import Queue
import glob
import multiprocessing
from multiprocessing import Process, Queue, JoinableQueue
#from threading import Thread

import time
from pathlib import Path
from dkcoverage import dkcoverage
from dkcoverage.project import Project
from dkcoverage.testenv import TestEnvironment
from dkcoverage.testsuite import TestSuite
from dkcoverage.utils import jason
from dkcoverage import srcfile, dkenv


def dumpjson(n, fname):
    f = srcfile.Sourcefile.fetch(fname, dkenv.DKROOT)
    f.save()
    # val = jason.dumps(f)
    # with open('_coverage/_covroot/srcfiles/' + f.file.cachename + '.txt', 'w') as fp:
    #     print >> fp, val
    #     print "%5d %s" % (n, f.file.absname)


def queue_worker(q):
    while 1:
        try:
            item = q.get()
            if item is None:
                print "QUITTING"
                return
            i, fname = item
            dumpjson(i, fname)
        finally:
            q.task_done()


def find_files():
    root = Path(dkenv.DKROOT)
    # PCOUNT = multiprocessing.cpu_count()
    PCOUNT = 1
    q = JoinableQueue(maxsize=PCOUNT)

    # start consumer threads
    procs = []
    for i in range(PCOUNT):
        p = Process(target=queue_worker, args=(q,))
        procs.append(p)
        p.start()

    # push work onto queue
    for i, fname in enumerate(root.glob('**/*.py')):
        q.put((i, fname))

    # post harakiri payload..
    for i in range(PCOUNT):
        q.put(None)

    # wait for everyone to die..
    while not q.empty():
        time.sleep(1)


if __name__ == "__main__":
    start = time.time()
    find_files()
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
