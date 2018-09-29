# -*- coding: utf-8 -*-

import os
import pickle
import json
import sys
import re
from hashlib import blake2b
from base64 import b64encode

import mysql.connector

from ink.sys.config import CONF
from ink.sys.database import Connector


def vp(msg: str):
    if CONF.debug.verbose and CONF.debug.verbose_level:
        verbose_level = CONF.debug.verbose_level
    else:
        return

    if verbose_level > 1:
        print('> ' + msg, file=sys.stderr)
    if verbose_level > 2:
        print('>> ' + msg, file=sys.stderr)


class DBMaintainer:
    '''
    INK System Database Maintainer
    '''

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        if dry_run:
            self.dbc = Connector(CONF.database.connect_string)

    def get_defined_tables(self, schema_file: str = '') -> dict:
        tables = dict()
        if not schema_file:
            schema_file = CONF.database.schema_file
        with open(schema_file, 'r') as fpr:
            table_name = str()
            lines = list()
            for line in fpr:
                line = line.strip()
                # remove comment
                comment_start = line.find('--')
                if comment_start >= 0:
                    line = line[:comment_start]

                # check blank line or not.
                if line == '':
                    if table_name:
                        # end of table definition.
                        tables[table_name] = ' '.join(lines)
                        lines.clear()
                        table_name = ''
                else:
                    # start of table definition
                    stmt_begin = re.match(r'create table (\w+)', line)
                    if stmt_begin:
                        if table_name:
                            tables[table_name] = ' '.join(lines)
                            lines.clear()
                        table_name = stmt_begin.group(1)

                if table_name:
                    lines.append(line)
        return tables

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
            statements.append('drop table {}'.format(table_name))
        return self.dbc.execute(statements)


def make_pickle(conf_file: str = '', pickle_file: str = ''):
    '''Pickle Maker

    Convert raw, readable, and formatted config file (json) to
    Python independed 'pickle' file.
    '''

    # get source file name (.json)
    if not conf_file:
        if 'INK_CONF_FILE' in os.environ:
            conf_file = os.environ.get('INK_CONF_FILE')
        else:
            d = os.path.dirname(__file__)
            conf_file = os.path.abspath(d + '/../var/settings.json')

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


def secure_hash(value: str, salt: str) -> str:
    '''
    Secure Hash Function

    secure_hashing() is hashing arg[1] string and return hashed string.
    Using hash function is BLAKE2B and digest size is 32.
    '''

    salt = salt.encode('utf-8')
    # https://github.com/PyCQA/pylint/issues/2478
    h = blake2b(key=salt, digest_size=32) # pylint: disable=E1123
    h.update(value.encode('utf-8'))
    return b64encode(h.digest()).decode()
