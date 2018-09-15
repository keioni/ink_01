#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from ink.sys.config import CONF

def hoge1():
    conf_file = os.environ.get('INK_CONF_FILE')
    if not conf_file:
        conf_file = './var/settings.json'
    CONF.load(conf_file, True)
    print(CONF)
    print(CONF.database)
    print(CONF.database.host)

hoge1()
