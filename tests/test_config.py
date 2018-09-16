# -*- coding: utf-8 -*-

import os
import re
import pytest

from ink.sys.config import CONF, Configure

# def test_get_file_name():
#     assert ink.sys.conf_file

# def test_validate_file():
#     assert ink.sys.raw_conf

# def test_load_file():
#     assert ink.sys.raw_conf and ink.sys.raw_conf['version'] == '1.0'

TEST_CONF_FILE = './tests/settings_for_unittest.json'

def test_load_env_file():
    os.environ['INK_CONF_FILE'] = TEST_CONF_FILE
    conf = Configure()
    conf.load()
    assert conf.debug

def test_load_hardcoded_file():
    conf = Configure()
    conf.load()
    assert conf.debug

def test_load_specified_file():
    conf = Configure()
    conf.load(TEST_CONF_FILE)
    assert conf.debug

def test_pickling():
    # conf_file = TEST_CONF_FILE.replace('.json', '_pickling_test.json')
    # conf = Configure()
    # conf.load()
    assert True
