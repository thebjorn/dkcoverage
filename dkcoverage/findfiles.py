# -*- coding: utf-8 -*-

from pathlib import Path
from . import dkenv, srcfile, db


def fetch_mtimes(cn=None):
    cn = cn or db.connect()
    return {rec['absname']: rec['stat_mtime'] for
            rec in cn.execute("select absname, stat_mtime from srcfiles")}


_all_files = {}


def all_files(root):
    global _all_files
    if _all_files is None:
        _all_files = {}
        for fname in root.glob('**/*.py'):
            sfile = srcfile.Sourcefile(fname, root)
            _all_files[sfile.relname] = sfile
    return _all_files


def file_changed(fname, root=dkenv.DKROOT, cn=None):
    cn = cn or db.connect()
    current = srcfile.Sourcefile(fname, root)
    dbver = srcfile.Sourcefile.fetch(fname, root, cn)
    return current != dbver


def find_changed_files(cn=None):
    cn = cn or db.connect()
    mtimes = fetch_mtimes(cn)
    root = Path(dkenv.DKROOT)
    #for fname, current in all_files(root).items():
    for i, fname in enumerate(root.glob('**/*.py')):
        current = srcfile.Sourcefile(fname, root)
        _all_files[fname] = current
        if current.stat_mtime == mtimes.get(current.absname):
            continue
        dbver = srcfile.Sourcefile.fetch(current.absname, root, cn)
        if current != dbver:  # if changed..
            yield current


def find_tests_to_run(fname, cn=None):
    c = (cn or db.connect()).cursor()
    c.execute("""
         select distinct srcfile
         from dependencies
         where imports = ?
    """, [fname.relname])
    res = set(rec[0] for rec in c.fetchall())
    return res

