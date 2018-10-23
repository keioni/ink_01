#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json

from ink.maintainer import make_pickle, DatabaseMaintainer
from ink.sys.config import CONF
from ink.sys.database.connector.mysql import MySQLConnector
from ink.sys.database.connector.null import NullConnector


def _get_db_connector(dry_run: bool = False):
    if dry_run:
        db_connector = NullConnector()
    else:
        db_connector = MySQLConnector()
    db_connector.connect(CONF.database.connect_config)
    return db_connector

def cmd_mp():
    conf_file = ''
    pickle_file = ''
    if len(args) > 1:
        conf_file = args[1]
    if len(args) > 2:
        pickle_file = args[2]
    print('>> Pickle Maker starting...')
    make_pickle(conf_file, pickle_file)
    print('>> Pickle Maker finished.')

def cmd_dbm():
    db_connector = _get_db_connector(True)
    dbman = DatabaseMaintainer(db_connector)
    if len(args) > 1:
        subcmd = args[1]
        if subcmd == 's':
            tables = dbman.get_defined_tables()
            print(json.dumps(tables, indent=4))
        elif subcmd == 'c':
            dbman.create_tables()
        elif subcmd == 'd':
            dbman.destroy_tables()

def cmd_t_dbm():
    db_connector = _get_db_connector()
    dbman = DatabaseMaintainer(db_connector)
    tables1 = dbman.get_defined_tables('tests/test_table_schema1.sql')
    tables2 = dbman.get_defined_tables('tests/test_table_schema2.sql')
    print(json.dumps(tables1, indent=4))
    print(json.dumps(tables2, indent=4))

def cmd_dbrs():
    name = ''
    arg = ''
    if len(args) > 1:
        name = args[1]
    if len(args) > 2:
        arg = args[2]
    db_connector = _get_db_connector()
    dbman = DatabaseMaintainer(db_connector)
    dbman.get_statement(name, arg)

def cmd_cc():
    print(CONF)
    print(CONF.database)
    print(CONF.database.connect_string.host)


CONF.load()

cmd = sys.argv[1]
args = sys.argv[1:]
if cmd == 'debug':
    cmd = 'dbm'
    args = [cmd, 'c']

if cmd == 'mp':
    cmd_mp()
elif cmd == 'dbm':
    cmd_dbm()
elif cmd == 't_dbm':
    cmd_t_dbm()
elif cmd == 'dbrs':
    cmd_dbrs()
elif cmd == 'cc':
    cmd_cc()
else:
    print('Bad command: {}'.format(cmd))
