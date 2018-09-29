#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import ink.util

if __name__ == '__main__':
    args = dict()
    for i in range(len(sys.argv)):
        args[i] = sys.argv[i]

    if args[1] == 'mp':
        print('>> Pickle Maker starting...')
        ink.util.make_pickle(args.get(2), args.get(3))
        print('>> Pickle Maker finished.')
