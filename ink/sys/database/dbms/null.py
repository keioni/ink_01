# -*- coding: utf-8 -*-

from ink.sys.database.connector import Connector


class NullConnector(Connector):

    def connect(self, connect_config: dict):
        self.conn = None
        print('== NullConnector ==')

    def execute(self, statements: list):
        for stmt in statements:
            print('execute> ' + stmt )
