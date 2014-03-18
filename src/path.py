# -*- coding: utf-8 -*-

import os
import errno
import datetime


def timestamp():
    "Return a timestamp for the work folder."
    return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")


def normpath(p, slash=None):
    """Return a canonical version of path ``p``.
    """
    res = os.path.normcase(os.path.normpath(os.path.abspath(p)))
    if slash is None:
        return res
    else:
        return res.replace('\\', slash)


def make_path(path):
    """Make all the directories in path.
    """
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            pass
        else:
            raise
    return normpath(path)
