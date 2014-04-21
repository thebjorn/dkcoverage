# -*- coding: utf-8 -*-

import os
import sqlite3 as sqlite
from .. import dkenv


DBLOCATION = os.path.join(dkenv.DKROOT, '_coverage', '_covroot', 'dkcoverage.db')


def connect():
    cn = sqlite.Connection(DBLOCATION)
    cn.row_factory = sqlite.Row
    return cn


def create_table(name, ddl, cn=None):
    cn = cn or connect()
    try:
        cn.execute("select 1 from " + name)
    except sqlite.OperationalError:
        cn.execute(ddl)
