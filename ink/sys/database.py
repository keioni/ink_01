# -*- coding: utf-8 -*-

import mysql.connector


class Connector:

    def __init__(self, db_connect_config: dict):
        self.conn = mysql.connector.connect(**db_connect_config)
        self.conn.autocommit(False)

    def __fetch(self, statement: str, fetch_type: str = 'all') -> tuple:
        result = tuple()
        cursor = self.conn.cursor()
        if cursor:
            cursor.execute(statement)
            if fetch_type == 'all':
                result = tuple(cursor.fetchall())
            elif fetch_type == 'one':
                result = tuple(cursor.fetchone())
            cursor.close()
        return result

    def fetchone(self, statement) -> tuple:
        return self.__fetch(statement, 'one')

    def fetchall(self, statement) -> tuple:
        return self.__fetch(statement, 'all')

    def execute(self, statements: list) -> bool:
        result = False
        cursor = self.conn.cursor()
        if cursor:
            try:
                for statement in statements:
                    cursor.execute(statement)
                self.conn.commit()
                result = True
            except mysql.connector.Error:
                self.conn.rollback()
            finally:
                cursor.close()
        return result


def connect(db_connect_config: dict):
    return Connector(db_connect_config)
