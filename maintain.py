#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import hashlib


import ink.util
from ink.sys.config import CONF

if __name__ == '__main__':
    CONF.load()
    progname = sys.argv.pop(0)
    cmd = sys.argv.pop(0)
    args = dict()
    for i in range(len(sys.argv)):
        args[i] = sys.argv[i]

    if cmd == 'mp':
        print('>> Pickle Maker starting...')
        ink.util.make_pickle(args.get(0), args.get(1))
        print('>> Pickle Maker finished.')
    elif cmd == 'dbm':
        dbm = ink.util.DBMaintainer(False)
        tables = dbm.get_defined_tables()
        print(json.dumps(tables, indent=4))
    elif cmd == 't_dbm':
        dbm = ink.util.DBMaintainer(False)
        tables = dbm.get_defined_tables('tests/test_table_schema.sql')
        cur_digest = ink.util.generate_digest(str(tables))

        json_str = str(json.dumps(tables, indent=4))
        print(json_str)
        print(ink.util.generate_digest(json_str))
    elif cmd == 'cc':
        print(CONF)
        print(CONF.database)
        print(CONF.database.connect_string.host)
    else:
        print('Bad command: {}'.format(cmd))
