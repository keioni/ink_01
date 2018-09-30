# -*- coding: utf-8 -*-

from typing import Union

from ink.sys.database.connector import BaseConnector


class NullConnector(BaseConnector):

    def connect(self, connect_config: dict):
        print('== NullConnector ==')

    def execute(self, statements: Union[str, list] = str):
        if isinstance(statements, str):
            statements = [statements]
        for stmt in statements:
            print('execute> ' + stmt )
