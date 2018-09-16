# -*- coding: utf-8 -*-

import os
import re
import pytest

from ink.sys.config import CONF, Configure

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
