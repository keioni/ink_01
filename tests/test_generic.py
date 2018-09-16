# -*- coding: utf-8 -*-

import os
import re
import pytest

# os.environ['INK_CONF_FILE'] = './tests/settings_for_unittest.json'
# import ink.sys
from ink.sys.config import CONF

# def test_get_file_name():
#     assert ink.sys.conf_file

# def test_validate_file():
#     assert ink.sys.raw_conf

# def test_load_file():
#     assert ink.sys.raw_conf and ink.sys.raw_conf['version'] == '1.0'

def test_get_conf_value():
    CONF.load('./tests/settings_for_unittest.json')
    assert CONF.debug
