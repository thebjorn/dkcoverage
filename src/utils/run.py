# -*- coding: utf-8 -*-

from concurrent import futures
import os
import shlex
import subprocess
import time


def async(f):
    def _wrap(*args, **kwargs):
        with futures.ThreadPoolExecutor(max_workers=2) as executor:
            return executor.submit(f, *args, **kwargs)

    return _wrap


def cmd(c, cwd='.', env=os.environ):
    return subprocess.Popen(
        shlex.split(c),
        stdout=subprocess.PIPE,
        stderr=open(os.devnull, 'w'),
        cwd=cwd,
        env=env
    ).communicate()[0]


asyncmd = async(cmd)


def waiting():
    import sys
    sys.stderr.write('\n\nwaiting\n\n')
    sys.stderr.flush()


if __name__ == "__main__":
    from future import Future
    print 'start'
    f = Future(cmd, 'grep -R foobar /work/dev/datakortet *')
    res = f(waiting)
    print 'done:', len(res)
    # print cmd('grep -R foobar *')

    # asyncmd1 = asyncmd('grep -R foobar /work/dev/datakortet *')
    # while asyncmd1.running():
    #     print '=======',
    #
    # print len(asyncmd1.result())
    # print asyncmd1
