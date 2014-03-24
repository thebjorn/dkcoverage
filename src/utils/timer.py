# -*- coding: utf-8 -*-
import time


class Timer(object):
    def __init__(self):
        self.start = self.stop = self.elapsed = None

    def begin(self):
        self.start = time.time()

    def end(self):
        self.stop = time.time()
        self.elapsed = self.stop - self.start
        return self.elapsed
