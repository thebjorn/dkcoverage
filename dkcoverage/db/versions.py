# -*- coding: utf-8 -*-
from .covdb import connect, create_table


def version_0():
    create_table("dbversion", """
        create table dbversion  (
          version int primary key
        )
    """)

    cn = connect()
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
