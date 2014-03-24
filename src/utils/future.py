# -*- coding: utf-8 -*-

"""From Easy threading with Futures
   http://code.activestate.com/recipes/84317-easy-threading-with-futures/

   With my improvements to the exception handling (from the comments).
"""

from threading import *
import copy
import sys


class Future(object):
    def __init__(self, func, *param):
        # Constructor
        self.__done = 0
        self.__result = None
        self.__status = 'working'
        self.__excpt = None

        self.__C = Condition()  # Notify on this Condition when result is ready

        # Run the actual function in a separate thread
        self.__T = Thread(target=self.wrapper, args=(func, param))
        self.__T.setName("FutureThread")
        self.__T.start()

    def __repr__(self):
        return '<Future at ' + hex(id(self)) + ':' + self.__status + '>'

    def __call__(self, waitfn=None, *args, **kwargs):
        self.__C.acquire()
        sys.stdout.write("aquire\n")
        sys.stdout.flush()
        while self.__done == 0:
            sys.stdout.write("waiting\n")
            sys.stdout.flush()
            if waitfn:
                waitfn(*args, **kwargs)
            self.__C.wait()
        sys.stdout.write("release\n")
        sys.stdout.flush()
        self.__C.release()
        if self.__excpt: raise self.__excpt
        # We deepcopy __result to prevent accidental tampering with it.
        a = copy.deepcopy(self.__result)
        return a

    def wrapper(self, func, param):
        # Run the actual function, and let us housekeep around it
        self.__C.acquire()
        try:
            self.__result = func(*param)
        except Exception as e:
            self.__excpt = e
        except:
            self.__result = "Unknown exception raised within Future"
        self.__done = 1
        self.__status = `self.__result`
        self.__C.notify()
        self.__C.release()
