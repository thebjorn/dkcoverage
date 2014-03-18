# -*- coding: utf-8 -*-

"""Utility functions for shell-like programming::

      for line in run('cat foo') | grep('hello'):
          print line

   New 'commands' only need to have a feed(lines) method that should return
   a Lines instance.
"""

# pylint:disable=R0903,R0201

# R0903: Too few public methods
# R0201: method could be a function

import re
import shlex
import pprint
from subprocess import Popen, PIPE


def runcmd(cmd, *args):
    "helper function to grab output of a shell command."
    if args:
        cmd = cmd + ' ' + ' '.join(args)

    output = Popen(shlex.split(cmd), stdout=PIPE).communicate()[0]
    return output.splitlines()


def _grep(pattern, lines):
    "return the lines that match pattern."
    return [line for line in lines if re.search(pattern, line)]


def extract_line(pattern, lines):
    "return first line that matches pattern."
    return _grep(pattern, lines)[0]


def _split(lines):
    "Split each line into columns."
    return [line.split() for line in lines]


def _field(n, lines):
    "Return the nth column."
    return [cols[n] for cols in _split(lines)]


class Lines(object):
    "Pipe contents."

    def __init__(self, lines):
        self.lines = lines

    def __nonzero__(self):
        return bool(self.lines)

    def __len__(self):
        return len(self.lines)

    def __repr__(self):
        return pprint.pformat(self.lines)

    __str__ = __repr__

    def __iter__(self):
        return iter(self.lines)

    def __or__(self, nextcmd):
        return nextcmd.feed(self.lines)

    def __getitem__(self, key):
        return self.lines[key]


def run(cmd, *args, **kw):
    "Convenience function to get runcmd output into pipeable format."
    if kw.get('verbose'):
        print cmd,
        if args:
            print args
        else:
            print
    return Lines(runcmd(cmd, *args))


class Sort(object):
    "similar to unix sort command."

    def feed(self, lines):
        "sort lines"
        return Lines(sorted(lines))


sort = Sort()


class grep(object):
    "similar to unix grep command."

    def __init__(self, pattern):
        self.pattern = pattern

    def feed(self, lines):
        "get input from pipe"
        return Lines([line for line in lines if re.search(self.pattern, line)])


class grepv(object):
    "similar to unix `grep -v` command (return lines that don't match."

    def __init__(self, pattern):
        self.pattern = pattern

    def feed(self, lines):
        "get input from pipe"
        return Lines([line for line in lines
                      if not re.search(self.pattern, line)])


class fn(object):
    "call function on each line."

    def __init__(self, function):
        self.defun = function

    def feed(self, lines):
        "get input from pipe"
        return Lines([self.defun(line) for line in lines])


class PrintLines(object):
    "Print lines."

    def feed(self, lines):  # pylint:disable=R0201
        "Print lines."
        for line in lines:
            print line
        return len(lines)

# aliases
cat = PrintLines()
printlines = PrintLines()


class Split(object):
    """Split input lines into columns, optionally specify token to split on. 
       Normally used through the `split' object.
    """

    def __init__(self, token=None):
        self.token = token

    def feed(self, lines):
        "get input from pipe"
        return Lines([line.split(self.token) for line in lines])


split = Split()


class field(object):
    "Extract column #n."

    def __init__(self, n):
        self.n = n

    def feed(self, lines):
        "get input from pipe"
        return Lines([cols[self.n] for cols in _split(lines)])


class lineno(object):
    "Extract line #n."

    def __init__(self, n):
        self.n = n

    def feed(self, lines):
        "get input from pipe"
        return lines[self.n]


first = lineno(0)
second = lineno(1)
last = lineno(-1)


class head(object):
    "Extract first n lines."

    def __init__(self, n):
        self.n = n

    def feed(self, lines):
        "get input from pipe"
        return Lines(lines[:self.n])
