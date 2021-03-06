# -*- coding: utf-8 -*-

import mysql.connector

from ink.sys.database.connector import BaseConnector


class MySQLConnector(BaseConnector):

    def connect(self, connect_config: dict):
        self.conn = mysql.connector.connect(**connect_config)
        self.conn.autocommit(False)
        super().connect(connect_config)

    def close(self):
        self.conn.close()
        super().close()
