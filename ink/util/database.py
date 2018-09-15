# -*- coding: utf-8 -*-

import mysql.connector

from ink.sys.config import conf
import ink.sys.database


class Maintainer:
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
        self.dbc = ink.sys.database.connect()

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
