#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from ink.sys.config import CONF

def hoge1():
    CONF.load()
    print(CONF)
    print(CONF.database)
    print(CONF.database.host)

hoge1()
