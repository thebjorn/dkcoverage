# -*- coding: utf-8 -*-

import os
import sqlite3 as sqlite
from .. import dkenv


DBLOCATION = os.path.join(dkenv.DKROOT, '_coverage', '_covroot', 'dkcoverage.db')


def connect():
    return sqlite.Connection(DBLOCATION)


def create_table(name, ddl):
    try:
        connect().execute("select 1 from " + name)
    except sqlite.OperationalError:
        connect().execute(ddl)
