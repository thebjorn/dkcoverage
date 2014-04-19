# -*- coding: utf-8 -*-
from pathlib import Path
from . import dkenv, srcfile


class Project(object):
    def __init__(self, root=dkenv.DKROOT):
        self.root = Path(root)
        self.files = {}
        for fname in self.root.glob('**/*.py'):
            f = srcfile.Sourcefile(fname, self.root)
            self.files[f.file.absname] = f

        # self.fnames = self.root.glob('**/*.py')
        # self.pyfiles = [srcfile.Sourcefile(f, self.root)
        #                 for f in self.root.glob('**/*.py')]
        #
        # self.files = {f.file.absname: f for f in self.pyfiles}

    def __json__(self):
        return self.files
