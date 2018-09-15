# -*- coding: utf-8 -*-

from ink.util.security import secure_hashing
from ink.sys.config import conf
import ink.sys.database


class Users:

    def __init__(self):
        self.dbc = ink.sys.database.connect()
        self.salt = 'hoge' # XXX

    def get_uid(self, username: str) -> int:
        sql_stmt = '''
            select user_id from users where username = '?'
        '''
        user_id = 0
        statement = (sql_stmt, (username))
        row = self.dbc.fetchone(statement)
        if row:
            user_id = int(row[0])
        return user_id

    def get_username(self, user_id: int) -> str:
        sql_stmt = '''
            select username from users where user_id = ?
        '''
        username = ''
        statement = (sql_stmt, (user_id))
        row = self.dbc.fetchone(statement)
        if row:
            username = str(row[0])
        return username

    def add_user(self, username: str, password: str) -> int:
        # XXX
        return self.get_uid(username)

    def delete_user(self, user_id: int) -> bool:
        pass

    def auth_user(self, username: str, password: str) -> bool:
        sql_stmt = '''
            select password from users where username = '?'
        '''
        stored_password = ''
        input_password = secure_hashing(password, self.salt)
        statement = (sql_stmt, (username))
        row = self.dbc.fetchone(statement)
        if row:
            stored_password = str(row[0])
        return stored_password == input_password
