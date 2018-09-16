# -*- coding: utf-8 -*-
'''INK system configuration module.

This module is used to customizing INK system settings.
When you want to access any settings, you must use
the instance -- already created when imported timing --
of this class 'CONF' on this module.

For example:
    from ink.sys.config import CONF

    CONF.load(path_to_setting_file)
    some_instance.do_something(CONF.toplevel.secondlevel)
'''


import os
import json
import pickle

from attrdict import AttrDict


class Configure:
    '''INK system configuration manager.

    How to use this class, see module docstring.
    '''
    CONF_TREE_NAME = 'configurations'

    def __init__(self, conf_dict: dict = None):
        self.__conf = {}
        self.__conf_parts = {}
        if conf_dict:
            self.__conf = conf_dict

    def __getattr__(self, name):
        if not self.__conf:
            msg = 'Setting file does not loaded.'
            raise AttributeError(msg)
        if name not in self.__conf_parts:
            part = self.__conf[self.CONF_TREE_NAME].get(name)
            if part:
                self.__conf_parts[name] = AttrDict(part)
            else:
                msg = 'No configuration part: {}'.format(name)
                raise AttributeError(msg)
        return self.__conf_parts[name]

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.__conf)

    # def __str__(self):
    #     return json.dumps(self.__conf, indent=4)

    def __make_pickle(self, conf_file: str) -> bool:
        pickle_file = conf_file.replace('.json', '.pickle')
        pickle_file_mtime = 0
        conf_file_mtime = os.path.getmtime(conf_file)
        if os.path.exists(pickle_file):
            pickle_file_mtime = os.path.getmtime(pickle_file)
        if conf_file_mtime > pickle_file_mtime:
            with open(pickle_file, 'wb') as fp:
                pickle.dump(self.__conf, fp)
                return True
        return False

    def __validate_conf_dict(self, conf: dict) -> bool:
        if conf.get('version') != '1.0':
            return False
        if self.CONF_TREE_NAME not in conf:
            return False
        return True

    def load(self, conf_file: str = None, read_pickle: bool = True):
        '''load json format setting file.

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
        '''

        if not conf_file:
            conf_file = os.environ.get('INK_CONF_FILE')
            if not conf_file:
                conf_dir = os.path.dirname(__file__) + '/../..'
                conf_file = os.path.abspath(conf_dir + '/var/settings.json')
            if not conf_file:
                msg = 'Cannot load default settings. Retry with filename.'
                raise ValueError(msg)
        if read_pickle:
            pickle_file = conf_file.replace('.json', '.pickle')
            if os.path.exists(pickle_file):
                conf_file_mtime = os.path.getmtime(conf_file)
                pickle_file_mtime = os.path.getmtime(pickle_file)
                if conf_file_mtime <= pickle_file_mtime:
                    with open(pickle_file, 'rb') as fp:
                        self.__conf = pickle.load(fp)
                    self.__conf_parts.clear()
                    return True
        with open(conf_file, 'r') as fp:
            conf = json.load(fp)
        if not conf:
            msg = 'Cannot load settings from: ' + conf_file
            raise ValueError(msg)
        if not self.__validate_conf_dict(conf):
            msg = 'Invalid format file: ' + conf_file
            raise ValueError(msg)
        self.__conf = conf
        self.__conf_parts.clear()
        self.__make_pickle(conf_file)
        return True


CONF = Configure()

# conf = AttrDict()

# conf_file = os.environ.get('INK_CONF_FILE')
# if not conf_file:
#     conf_file = './var/settings.json'

# with open(conf_file, 'r') as f:
#     raw_conf = json.load(f)
# if not raw_conf:
#     msg = 'Cannot load system settings from the file.'
#     raise ValueError(msg)
# if raw_conf.get('version') != '1.0':
#     msg = 'Version number does not exist or not match this system.'
#     raise ValueError(msg)
# conf = AttrDict(raw_conf.get('configurations'))
