# -*- coding: utf-8 -*-


class PathInfo(object):
    def __init__(self, pth):
        self.relname = pth
        self.absname = pth.absolute().as_posix()
        self.path = pth.parent
        self.filename = pth.name
        self.ext = pth.suffix
        self.name = pth.stem

        # self.absname = pth.normpath(os.path.join(dkenv.DKROOT, pth), '/')
        # self.path, self.filename = os.path.split(self.absname)
        # self.name, self.ext = os.path.splitext(self.filename)
