# -*- coding: utf-8 -*-

from ink.util import DBMaintainer

def test_read_sql_file():
    dbm = DBMaintainer(False)
    tables = dbm.get_defined_tables('tests/test_table_schema.sql')
    assert tables
