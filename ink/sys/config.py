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

from attrdict import AttrDict


class Configure:
    '''INK system configuration manager.

    How to use this class, see module docstring.
    '''


    def __init__(self, conf_dict: dict = None):
        self.__conf = {}
        self.__files = []
        if conf_dict:
            self.__conf = conf_dict
        else:
            conf_dir = __file__ + '../../..'
            conf_file = os.path.abspath(conf_dir + '/var/settings.json')
            if os.path.exists(conf_file):
                with open(conf_file, 'r') as f:
                    self.__conf = json.load(f)
                self.__files.append(conf_file)

    def __getattr__(self, name):
        if not self.__conf:
            msg = 'Setting file does not loaded.'
            raise AttributeError(msg)
        values = self.__conf['configurations'].get(name)
        if values:
            return AttrDict(values)
        msg = 'No configuration values of name: {}'.format(name)
        raise AttributeError(msg)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.__conf)

    # def __str__(self):
    #     return json.dumps(self.__conf, indent=4)

    def load(self, conf_file: str, force_load: bool = False):
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

        if self.__conf:
            if not force_load:
                msg = 'Always loaded.'
                raise ValueError(msg)
        with open(conf_file, 'r') as f:
            self.__conf = json.load(f)
        if not self.__conf:
            msg = 'Cannot load system settings from the file.'
            raise ValueError(msg)
        if self.__conf.get('version') != '1.0':
            msg = 'Version number does not exist or not match this system.'
            raise ValueError(msg)
        if not self.__conf.get('configurations'):
            msg = "Setting file's format is invalid."
            raise ValueError(msg)
        return True

    def is_loaded(self) -> bool:
        return bool(self.__conf)

    def clear(self):
        self.__conf.clear()


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
