#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import hashlib

import ink.util
from ink.sys.config import CONF
from ink.sys.database.connector.mysql import MySQLConnector
from ink.sys.database.connector.null import NullConnector


def mp():
    print('>> Pickle Maker starting...')
    ink.util.make_pickle(args.get(0), args.get(1))
    print('>> Pickle Maker finished.')

def dbm():
    if args.get(0, 'dry') == 'run':
        db_connector =  MySQLConnector()
    else:
        db_connector = NullConnector()
    db_connector.connect(CONF.database.connect_config)
    dbm = ink.util.DBMaintainer(db_connector)
    tables = dbm.get_defined_tables()
    cmd = args.get(1, 's')
    if cmd == 's':
        print(json.dumps(tables, indent=4))
    elif cmd == 'c':
        dbm.create_tables()
    elif cmd == 'd':
        dbm.destroy_tables()

def t_dbm():
    if args.get(1, 'dry') == 'run':
        db_connector =  MySQLConnector()
    else:
        db_connector = NullConnector()
    db_connector.connect(CONF.database.connect_config)
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
cmd = sys.argv[0]
args = dict()
for i in range(len(sys.argv)):
    args[i] = sys.argv[i]

if cmd == 'debug':
    cmd = ''
    args = {1: '', 2: '', 3: '', 4: ''}

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
