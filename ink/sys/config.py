# -*- coding: utf-8 -*-
"""INK system configuration module.

This module is used to customizing INK system settings.
When you want to access any settings, you must use
the instance -- already created when imported timing --
of this class 'CONF' on this module.

For example:
    from ink.sys.config import CONF

    CONF.load(path_to_setting_file)
    some_instance.do_something(CONF.toplevel.secondlevel)
"""


import os
import json
import pickle
import logging

from attrdict import AttrDict


logger = logging.getLogger(__name__)


class Configure:
    """INK system configuration manager.

    How to use this class, see module docstring.
    """
    CONF_TREE_TOP_NAME = 'configurations'

    # def __init__(self, conf_dict: dict = None):
    #     self.__conf = dict()
    #     self.__conf_parts = dict()
    #     self.__conf_file = ''
    #     if conf_dict:
    #         self.__conf = conf_dict

    # def __repr__(self):
    #     return '{}({})'.format(self.__class__.__name__, self.__conf)

    # def __str__(self):
    #     return json.dumps(self.__conf, indent=4)

    def __init__(self):
        self.__conf = dict()
        self.__conf_parts = dict()

    def __getattr__(self, name):
        if not self.__conf:
            msg = 'Setting file does not loaded.'
            raise AttributeError(msg)
        if name not in self.__conf_parts:
            part = self.__conf[self.CONF_TREE_TOP_NAME].get(name)
            if part:
                self.__conf_parts[name] = AttrDict(part)
            else:
                msg = 'No configuration part: {}'.format(name)
                raise AttributeError(msg)
        return self.__conf_parts[name]

    def _validate_conf_dict(self, conf: dict) -> bool:
        if conf.get('version') != '1.0':
            return False
        if self.CONF_TREE_TOP_NAME not in conf:
            return False
        return True

    def _get_conf_filename(self) -> str:
        if 'INK_CONF_FILE' in os.environ:
            conf_file = os.environ.get('INK_CONF_FILE')
        else:
            conf_dir = os.path.dirname(__file__) + '/../..'
            conf_file = os.path.abspath(conf_dir + '/var/settings.json')
        return conf_file

    # def pickle(self, pickle_file: str):
    #     with open(pickle_file, 'wb') as fpw:
    #         pickle.dump(self.__conf, fpw)

    # def unpickle(self, pickle_file: str):
    #     with open(pickle_file, 'rb') as fpr:
    #         self.__conf = pickle.load(fpr)

    def load(self, conf_file: str = '', use_pickle: bool = True) -> bool:
        """load json format setting file.

        Arguments:
            * conf_file {str} -- file name of the setting file.
            * force_load {bool} -- In default, if setting file was
              already loaded, raise exception. If you need load
              twice or more and override loaded settings, change
              True. (default: {False})

        Return value:
            Return {True} when settings is loaded successfully.
            This method raise ValueError exception instead of
            returning {False}. So use try-except.
        """

        if not conf_file:
            conf_file = self._get_conf_filename()
            if not conf_file:
                msg = 'Cannot load default settings. Retry with filename.'
                raise ValueError(msg)
        conf = dict()
        if use_pickle:
            conf = self.load_conf_cache_pickle(conf_file)
        if not conf:
            with open(conf_file, 'r') as fpr:
                conf = json.load(fpr)
        if not conf:
            msg = 'Cannot load settings from: ' + conf_file
            raise ValueError(msg)
        if not self._validate_conf_dict(conf):
            msg = 'Invalid format file: ' + conf_file
            raise ValueError(msg)
        self.__conf = conf
        self.__conf_parts.clear()
        return True

    @classmethod
    def load_conf_cache_pickle(cls, conf_file: str) -> dict:
        conf = dict()
        pickle_file = conf_file.replace('.json', '.pickle')
        if os.path.exists(pickle_file):
            conf_file_mtime = os.path.getmtime(conf_file)
            pickle_file_mtime = os.path.getmtime(pickle_file)
            if conf_file_mtime <= pickle_file_mtime:
                with open(pickle_file, 'rb') as fpr:
                    conf = pickle.load(fpr)
        return conf


CONF: Configure = Configure()
