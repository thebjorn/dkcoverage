# -*- coding: utf-8 -*-
from dkcoverage.utils.digest import file_digest


class PathInfo(object):
    def __init__(self, pth):
        self.relname = pth.as_posix()
        self.absname = pth.absolute().as_posix()
        self.filename = pth.name
        self.name = pth.stem
        self.stat = self._stat(pth)
        self.digest = file_digest(self.absname)

    @property
    def cachename(self):
        return self.relname.replace('/', '$')[:-3]

    def _stat(self, p):
        stat = p.stat()
        return dict(
            size=stat.st_size,
            atime=stat.st_atime,    # most recent access
            mtime=stat.st_mtime,    # last modification
            created=stat.st_ctime,  # windows creation time
        )

    def __json__(self):
        return dict(
            relname=str(self.relname),
            absname=str(self.absname),
            filename=str(self.filename),
            name=str(self.name),
            stat=self.stat,
            digest=self.digest,
        )

    def __str__(self):
        return self.relname

    def __repr__(self):
        import pprint
        return pprint.pformat(self.__dict__)
