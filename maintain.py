#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import hashlib

import ink.util
from ink.sys.config import CONF
from ink.sys.database.dbms.mysql import MySQLConnector
from ink.sys.database.dbms.null import NullConnector


def mp():
    print('>> Pickle Maker starting...')
    ink.util.make_pickle(args.get(0), args.get(1))
    print('>> Pickle Maker finished.')

def dbm():
    if args.get(0, 'dry') == 'run':
        db_connector =  MySQLConnector()
        db_connector.connect(CONF.database.connect_config)
    else:
        db_connector = NullConnector()
    dbm = ink.util.DBMaintainer(db_connector)
    tables = dbm.get_defined_tables()
    print(json.dumps(tables, indent=4))

def t_dbm():
    if args.get(0, 'dry') == 'run':
        db_connector =  MySQLConnector()
        db_connector.connect(CONF.database.connect_config)
    else:
        db_connector = NullConnector()
    dbm = ink.util.DBMaintainer(db_connector)
    tables1 = dbm.get_defined_tables('tests/test_table_schema1.sql')
    tables2 = dbm.get_defined_tables('tests/test_table_schema2.sql')
    print(json.dumps(tables1, indent=4))
    print(json.dumps(tables2, indent=4))

def cc():
    print(CONF)
    print(CONF.database)
    print(CONF.database.connect_string.host)


CONF.load()
progname = sys.argv.pop(0)
cmd = sys.argv.pop(0)
args = dict()
for i in range(len(sys.argv)):
    args[i] = sys.argv[i]

if cmd == 'mp':
    mp()
elif cmd == 'dbm':
    dbm()
elif cmd == 't_dbm':
    t_dbm()
elif cmd == 'cc':
    cc()
else:
    print('Bad command: {}'.format(cmd))
