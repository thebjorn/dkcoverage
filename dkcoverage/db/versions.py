# -*- coding: utf-8 -*-
import sqlite3 as sqlite
from .covdb import connect, create_table


def upversion():
    newver = None
    cn = connect()

    create_table("dbversion", """
        create table dbversion  (
          version int primary key
        )
    """, cn)

    try:
        curver = cn.execute("select max(version) from dbversion").fetchone()[0]
    except sqlite.OperationalError:
        curver = -1

    versions = [version_0, version_1, version_2]

    for version in versions[curver+1:]:
        newver = version(cn)

    return newver


def version_2(cn):
    """Add lintscore column to srcfiles table.
    """
    cn.execute("""
        alter table srcfiles add column lintscore real default 0.0
    """)
    cn.execute("insert into dbversion (version) values (2)")
    cn.commit()
    return 2


def version_1(cn):
    """Add testrun table.
    """
    create_table("testrun", """
        create table testrun (
          relname varchar(150),

          passing int default 0,
          failing int default 0,
          erring int default 0,

          elapsed_secs real,
          pytest_output text null,
          mailbox text null,
          coverage blob null,

          foreign key (relname) references srcfiles(relname) on delete cascade
        )
    """, cn)

    cn.execute("insert into dbversion (version) values (1)")
    cn.commit()
    return 1


def version_0(cn):
    c = cn.cursor()
    c.execute("select count(*) from dbversion where version == 0")
    if c.fetchone()[0] == 1:
        return 0

    create_table("srcfiles", """
        create table srcfiles (
          relname varchar(150) primary key,
          absname varchar(250),
          appname varchar(30) null,

          digest varchar(32) null,
          stat_atime int null,
          stat_created int null,
          stat_mtime int null,
          size int null
        )
    """)

    create_table("dependencies", """
        create table dependencies (
          srcfile varchar(150),
          imports varchar(150),
          foreign key (srcfile) references srcfiles(relname) on delete cascade,
          foreign key (imports) references srcfiles(relname),
          constraint uniquedeps unique (srcfile, imports)
        )
    """)

    c.execute("select count(*) from dbversion")
    if c.fetchone()[0] == 0:
        c.execute("insert into dbversion (version) values (0)")
    cn.commit()
    return 0
