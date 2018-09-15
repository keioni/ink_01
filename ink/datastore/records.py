# -*- coding: utf-8 -*-

from ink.sys.config import conf
import ink.sys.database

class Records:

    def __init__(self):
        self.dbc = ink.sys.database.connect()

    def get_boxes(self, user_id: str) -> tuple:
        sql_stmt = '''
            select * from boxes where user_id = '?'
        '''
        statement = (sql_stmt, (user_id))
        return self.dbc.fetchall(statement)

    def get_cards(self, user_id: int, box_id: int) -> tuple:
        sql_stmt = '''
            select * from cards where user_id = ? and box_id = ?
        '''
        statement = (sql_stmt, (user_id, box_id))
        return self.dbc.fetchall(statement)

    def get_records(self, card_id: int) -> tuple:
        sql_stmt = '''
            select record from records where card_id = ?
        '''
        statement = (sql_stmt, (card_id))
        return self.dbc.fetchall(statement)


def get_all():
    pass
