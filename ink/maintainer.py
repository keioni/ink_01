# -*- coding: utf-8 -*-
'''INK system maintainer module.

There classes are used from the maintainer program only.
Don't make instance in system's body.
'''

import json
import os
import pickle
import re

from ink.sys.config import CONF


class DBMaintainer:
    '''
    Database Maintainer

    Used only from maintain.py.
    You can create, drop, modify, and other operations through
    this class.
    '''

    def __init__(self, connector=None):
        self.dbc = connector

    def get_defined_tables(self, schema_file: str = '') -> dict:
        tables = dict()
        if not schema_file:
            schema_file = CONF.database.schema_file
        with open(schema_file, 'r') as fpr:

            # read schema file and split to statement blocks
            lines = list()
            for line in fpr:
                comment_start = line.find('--')
                if comment_start >= 0:
                    line = line[:comment_start]
                lines.append(line.strip())
            statements = ''.join(lines).split(';')

            # picking up table schemas
            for statement in statements:
                match = re.search(r'create table (\w+)', statement)
                if match:
                    tables[match.group(1)] = statement

            # table_name = str()
            # lines = list()
            # for line in fpr:
            #     # remove comment
            #     comment_start = line.find('--')
            #     if comment_start >= 0:
            #         line = line[:comment_start].strip()
            #     line = line.strip()

            #     # check blank line or not.
            #     if line == '':
            #         if table_name:
            #             # end of table definition.
            #             tables[table_name] = ''.join(lines)
            #             lines.clear()
            #             table_name = ''
            #         continue
            #     else:
            #         # start of table definition
            #         stmt_begin = re.match(r'create table (\w+)', line)
            #         if stmt_begin:
            #             # if table_name:
            #             #     tables[table_name] = ' '.join(lines)
            #             #     lines.clear()
            #             table_name = stmt_begin.group(1)

            #     if table_name:
            #         lines.append(line)
        return tables

    def get_statement(self, name: str, arg: str = '') -> str:
        print(name + arg)

    def create_tables(self, tables: dict = None) -> bool:
        if not tables:
            tables = self.get_defined_tables()
        statements = list()
        for table_name in tables.keys():
            statements.append(tables[table_name])
        return self.dbc.execute(statements)

    def destroy_tables(self, tables: dict = None) -> bool:
        if not tables:
            tables = self.get_defined_tables()
        statements = list()
        for table_name in tables.keys():
            statements.append('drop table {};'.format(table_name))
        return self.dbc.execute(statements)


def make_pickle(conf_file: str = '', pickle_file: str = ''):
    '''
    Pickle Maker

    Convert raw, readable, and formatted config file (json) to
    Python independed 'pickle' file.
    '''

    # get source file name (.json)
    if not conf_file:
        if 'INK_CONF_FILE' in os.environ:
            conf_file = os.environ.get('INK_CONF_FILE')
        else:
            this_path = os.path.dirname(__file__)
            conf_file = os.path.abspath(this_path + '/../var/settings.json')

    # get destination file name (.pickle)
    if not pickle_file:
        pickle_file = conf_file.replace('.json', '.pickle')

    # read and write
    with open(conf_file, 'rb') as fpr:
        conf = json.load(fpr)
    print('Conf file: {}'.format(conf_file))
    with open(pickle_file, 'wb') as fpw:
        pickle.dump(conf, fpw)
    print('Pickle file: {}'.format(pickle_file))
