# -*- coding: utf-8 -*-
from pathlib import Path
from functools import total_ordering
# from .utils.future import Future
from .utils.dependencies import dependencies
from .utils.digest import file_digest
# from .utils.pathinfo import PathInfo
from . import db


@total_ordering
class Sourcefile(object):
    FIELDS = """relname absname appname digest
                stat_atime stat_created stat_mtime size
                lintscore
                """.split()

    @property
    def _self_attrs(self):
        "All saved attributes of self."
        return [getattr(self, attr) for attr in self.FIELDS]

    @property
    def _comma_attrs(self):
        "All fields as a comma separated string."
        return ', '.join(self.FIELDS)

    @property
    def _placeholder_attrs(self):
        "Return a comma separated string of placeholders for all attributes."
        return ','.join(['?'] * len(self.FIELDS))

    @classmethod
    def fetch(cls, pth, root, cn=None):
        p = Path(pth).relative_to(Path(root)).as_posix()
        if cn is None:
            cn = db.connect()
        c = cn.cursor()
        sql = """
          select $FIELDS$
          from srcfiles
          where relname = ?
        """.replace('$FIELDS$', ', '.join(cls.FIELDS))
        c.execute(sql, [str(p)])
        recs = c.fetchall()
        if len(recs) == 0:
            return cls(pth, root)
        rec = dict(zip(cls.FIELDS, recs[0]))
        return cls(pth, root, **rec)

    def __init__(self, pth, root, **kw):
        pth = Path(pth).relative_to(Path(root))
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
        self.lintscore = kw.get('lintscore', 0.0)

    @property
    def is_test(self):
        return self.name.startswith('test_')

    def clear_dependencies(self):
        self._dependencies = None
        cn = db.connect()
        c = cn.cursor()
        c.execute("delete from dependencies where srcfile = ?", [self.relname])

    def save(self):
        cn = db.connect()
        c = cn.cursor()
        sql = """
          insert or replace into srcfiles (
            {self._comma_attrs}
          ) values (
            {self._placeholder_attrs}
          )
        """.format(self=self)
        c.execute(sql, self._self_attrs)

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

    def __str__(self):
        return self.relname

    def __repr__(self):
        import pprint
        return pprint.pformat(self.__json__())

    def __eq__(self, other):
        return (self.size == other.size
                and self.digest == other.digest
                and self.relname == other.relname)

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return self.relname < other.relname

    def __json__(self):
        return dict(
            relname=str(self.relname),
            absname=str(self.absname),
            filename=str(self.filename),
            name=str(self.name),
            size=self.size,
            stat_atime=self.stat_atime,
            stat_mtime=self.stat_mtime,
            stat_created=self.stat_created,
            digest=self.digest,
        )

    @property
    def dependencies(self):
        if not isinstance(self._dependencies, list):
            self._dependencies = dependencies(self.absname,
                                              self.root.absolute())
        return self._dependencies
