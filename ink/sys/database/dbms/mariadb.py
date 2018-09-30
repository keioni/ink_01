# -*- coding: utf-8 -*-

import mysql.connector

from ink.sys.database.connector import Connector


class MySQLConnector(Connector):

    def connect(self, connect_config: dict):
        self.conn = mysql.connector.connect(**connect_config)
        self.conn.autocommit(False)
        super().connect(connect_config)
