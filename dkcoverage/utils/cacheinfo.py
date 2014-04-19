# -*- coding: utf-8 -*-
from pathlib import Path


class CacheInfo(object):
    def __init__(self, appname, pinfo):
        self.abspath = None
        self.name = Path(pinfo.relname.as_posix().replace('/', '$')[:-3])
        self.reldir = appname / self.name if appname else self.name
