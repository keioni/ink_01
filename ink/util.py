# -*- coding: utf-8 -*-

import os
import pickle
import json
import sys
from hashlib import blake2b
from base64 import b64encode

import mysql.connector

from ink.sys.config import CONF
import ink.sys.database


def vp(msg: str):
    if CONF.debug.verbose and CONF.debug.verbose_level:
        verbose_level = CONF.debug.verbose_level
    else:
        return

    if verbose_level == 0:
        return
    if verbose_level > 1:
        print('> ' + msg, file=sys.stderr)
    if verbose_level > 2:
        print('>> ' + msg, file=sys.stderr)


class DBMaintainer:
    '''
    INK System Database Maintainer
    '''

    # select * from boxes where user_id=$UID
    # select * from cards where user_id=$UID
    # select * from cards where user_id=$UID and box_id=$BID
    # select record from records where card_id=$CID

    TABLE_DEFS = {
    'tokens': '''
        create table tokens (
            rowid integer auto_increment,
            token bigint,
            user_id integer,
            ctime datetime not null,
            primary key (token),
        )
    ''',
    'users': '''
        create table users (
            rowid integer auto_increment,
            token bigint,
            user_id integer,
            ctime datetime not null,
            primary key (token),
        )
    ''',
    'boxes': '''
        create table boxes (
            box_id integer auto_increment,
            user_id integer,
            box_title varchar(32) not null,
            ctime datetime,
            mtime datetime,
            primary key (box_id),
            index index_user (user_id),
        )
    ''',
    'cards': '''
        create table cards (
            card_id integer auto_increment,
            box_id integer,
            user_id integer,
            card_title varchar(32) not null,
            ctime datetime,
            mtime datetime,
            recent_records char(340),
            primary key (card_id),
            index index_user_box (user_id, box_id),
        )
    ''',
    'records': '''
        create table records (
            rowid integer auto_increment,
            card_id integer,
            record char(16),
            primary key (rowid),
            index index_card (card_id),
        )
    '''
    }

    def __init__(self):
        self.dbc = ink.sys.database.connect(CONF.database)

    def __get_defined_tables(self) -> list:
        tables = list()
        for table_name in self.TABLE_DEFS.keys():
            tables.append(table_name)
        return tables

    def create_tables(self, tables: list=None) -> bool:
        if not tables:
            tables = self.__get_defined_tables()
        statements = list()
        for table in tables:
            statements.append(self.TABLE_DEFS[table])
        return self.dbc.execute(statements)

    def destroy_tables(self, tables: list=None) -> bool:
        if not tables:
            tables = self.__get_defined_tables()
        statements = list()
        for table in tables:
            statements.append('drop table {}'.format(table))
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
