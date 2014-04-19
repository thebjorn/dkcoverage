# -*- coding: utf-8 -*-

from multiprocessing import Process, JoinableQueue
import time
from pathlib import Path
from dkcoverage import srcfile, dkenv


def queue_worker(q):
    while 1:
        try:
            item = q.get()
            if item is None:
                # print "QUITTING"
                return
            i, fname = item
            f = srcfile.Sourcefile.fetch(fname, dkenv.DKROOT)
            f.save()
        finally:
            q.task_done()


def initdb():
    """Initialize the db with data for all source files and dependencies
       from tests to sources.  Only needs to be run once.
    """
    root = Path(dkenv.DKROOT)
    # Sqlite is single-access (need to handle locked errors before
    # increasing this value).
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
