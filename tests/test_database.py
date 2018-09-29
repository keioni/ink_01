# -*- coding: utf-8 -*-

import hashlib
import json

import ink.util


def test_read_sql_file():
    dbm = ink.util.DBMaintainer(False)
    tables1 = dbm.get_defined_tables('tests/test_table_schema1.sql')
    tables2 = dbm.get_defined_tables('tests/test_table_schema2.sql')

    h1 = hashlib.sha256()
    h1.update(str(tables1).encode('utf-8'))
    dig1 = h1.hexdigest()
    h2 = hashlib.sha256()
    h2.update(str(tables2).encode('utf-8'))
    dig2 = h2.hexdigest()
    assert dig1 == dig2
