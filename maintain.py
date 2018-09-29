#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

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
    elif cmd == 'cc':
        print(CONF)
        print(CONF.database)
        print(CONF.database.host)
    else:
        print('Bad command: {}'.format(cmd))
