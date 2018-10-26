# -*- coding: utf-8 -*-

from typing import Union


FETCH_ALL = 0
FETCH_ONE = 1


class BaseConnector:

    def __init__(self):
        self.conn = None

    def connect(self, connect_config: dict):
        pass

    def close(self):
        self.conn = None

    def __fetch(self, statement: str, fetch_type: int = FETCH_ALL) -> tuple:
        result = tuple()
        cursor = self.conn.cursor()
        if cursor:
            cursor.execute(statement)
            if fetch_type == FETCH_ALL:
                result = tuple(cursor.fetchall())
            elif fetch_type == FETCH_ONE:
                result = tuple(cursor.fetchone())
            cursor.close()
        return result

    def fetchone(self, statement) -> tuple:
        return self.__fetch(statement, FETCH_ONE)

    def fetchall(self, statement) -> tuple:
        return self.__fetch(statement, FETCH_ALL)

    def execute(self, statements: Union[str, list] = str) -> bool:
        result = False
        cursor = self.conn.cursor()
        if cursor:
            if isinstance(statements, str):
                statements = [statements]
            try:
                for statement in statements:
                    cursor.execute(statement)
                self.conn.commit()
                result = True
            # except mysql.connector.Error:
            except():
                self.conn.rollback()
            finally:
                cursor.close()
        return result
