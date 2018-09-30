#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import hashlib

import ink.util
from ink.sys.config import CONF
from ink.sys.database.connector.mysql import MySQLConnector
from ink.sys.database.connector.null import NullConnector


def _get_db_connector(mode: str = 'dry'):
    if mode == 'dry':
        db_connector = NullConnector()
    else:
        db_connector =  MySQLConnector()
    db_connector.connect(CONF.database.connect_config)
    return db_connector


def mp():
    conf_file = pickle_file = ''
    if len(args) > 1:
        conf_file = args[1]
    if len(args) > 2:
        pickle_file = args[2]
    print('>> Pickle Maker starting...')
    ink.util.make_pickle(conf_file, pickle_file)
    print('>> Pickle Maker finished.')

def dbm():
    db_connector = _get_db_connector()
    dbm = ink.util.DBMaintainer(db_connector)
    if len(args) > 1:
        subcmd = args[1]
        if subcmd == 's':
            tables = dbm.get_defined_tables()
            print(json.dumps(tables, indent=4))
        elif subcmd == 'c':
            dbm.create_tables()
        elif subcmd == 'd':
            dbm.destroy_tables()

def t_dbm():
    db_connector = _get_db_connector()
    dbm = ink.util.DBMaintainer(db_connector)
    tables1 = dbm.get_defined_tables('tests/test_table_schema1.sql')
    tables2 = dbm.get_defined_tables('tests/test_table_schema2.sql')
    print(json.dumps(tables1, indent=4))
    print(json.dumps(tables2, indent=4))

def dbrs():
    name = ''
    arg = ''
    if len(args) > 1:
        name = args[1]
    if len(args) > 2:
        arg = args[2]
    db_connector = _get_db_connector()
    dbm = ink.util.DBMaintainer(db_connector)
    dbm.get_statement(name, arg)

def cc():
    print(CONF)
    print(CONF.database)
    print(CONF.database.connect_string.host)


CONF.load()
progname = sys.argv.pop(0)
cmd = sys.argv[0]
args = sys.argv

if cmd == 'debug':
    cmd = ''
    args = []

if cmd == 'mp':
    mp()
elif cmd == 'dbm':
    dbm()
elif cmd == 't_dbm':
    t_dbm()
elif cmd == 'dbrs':
    dbrs()
elif cmd == 'cc':
    cc()
else:
    print('Bad command: {}'.format(cmd))
