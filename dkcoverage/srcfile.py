# -*- coding: utf-8 -*-
from pathlib import Path
from .utils.future import Future
from .utils.dependencies import dependencies
from .utils.digest import file_digest
from .utils.pathinfo import PathInfo
from . import db


class Sourcefile(object):
    FIELDS = """relname absname appname digest
                stat_atime stat_created stat_mtime size
                """.split()
    
    @classmethod
    def fetch(cls, pth, root):
        p = pth.relative_to(root)
        cn = db.connect()
        c = cn.cursor()
        c.execute("""
          select $FIELDS$
          from srcfiles
          where relname = ?
        """.replace('$FIELDS$', ', '.join(cls.FIELDS)), [str(p)])
        recs = c.fetchall()
        if len(recs) == 0:
            return cls(pth, root)
        rec = dict(zip(cls.FIELDS, recs[0]))
        return cls(pth, root, **rec)

    def __init__(self, pth, root, **kw):
        pth = pth.relative_to(Path(root))
        self.root = root
        self._dependencies = None
        self.relname = kw.get('relname', pth.as_posix())
        self.absname = kw.get('absname', pth.absolute().as_posix())
        self.appname = kw.get('appname', pth.parts[0] if pth.name != pth.parts[0] else "")
        self.digest = kw.get('digest') or file_digest(self.absname)

        stat = pth.stat()
        self.size = kw.get('size', stat.st_size)
        # most recent access
        self.stat_atime = kw.get('stat_atime', stat.st_atime)      
        # last modification
        self.stat_mtime = kw.get('stat_mtime', stat.st_mtime)
        # windows creation time
        self.stat_created = kw.get('stat_created', stat.st_ctime)

        # self.stat = self._stat(pth)
        self.filename = kw.get('filename', pth.name)
        self.name = kw.get('name', pth.stem)

    def save(self):
        cn = db.connect()
        c = cn.cursor()
        c.execute("""
            insert or replace into srcfiles ($FIELDS$) values ($VALUES$)
        """.replace("$FIELDS$",
                    ', '.join(self.FIELDS)
        ).replace('$VALUES$',
                  ','.join(['?'] * len(self.FIELDS))
        ), [self.relname,
            self.absname,
            self.appname,
            self.digest,
            self.stat_atime,
            self.stat_created,
            self.stat_mtime,
            self.size])
        if self.name.startswith('test_'):
            for dep in self.dependencies:
                c.execute("""
                    insert or replace into dependencies (
                      srcfile, imports
                    ) values (?, ?)
                """, [self.relname, dep])
        cn.commit()

    @property
    def cachename(self):
        return self.relname.replace('/', '$')[:-3]

    def __json__(self):
        return dict(
            relname=str(self.relname),
            absname=str(self.absname),
            filename=str(self.filename),
            name=str(self.name),
            # stat=self.stat,
            digest=self.digest,
        )

    @property
    def dependencies(self):
        if not isinstance(self._dependencies, list):
            # wait for Future to finish.
            self._dependencies = dependencies(self.absname, self.root)
        return self._dependencies
