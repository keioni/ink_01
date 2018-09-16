#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pickle
import json
import sys


def make_setting_pickle(json_file: str) -> bool:
    pickle_file = json_file.replace('.json', '.pickle')
    pickle_file_mtime = 0
    json_file_mtime = os.path.getmtime(json_file)
    if os.path.exists(pickle_file):
        pickle_file_mtime = os.path.getmtime(pickle_file)
    if json_file_mtime > pickle_file_mtime:
        with open(json_file, 'rb') as fp:
            conf = json.load(fp)
        with open(pickle_file, 'wb') as fp:
            pickle.dump(conf, fp)
            return True
    return False


if __name__ == '__main__':
    json_file: str = ''
    if sys.argv:
        pass
        # XXX
    else:
        json_file = os.environ.get('INK_json_FILE')
        if not json_file:
            json_dir = os.path.dirname(__file__) + '/../..'
            json_file = os.path.abspath(json_dir + '/var/settings.json')
        if not json_file:
            msg = 'Cannot load default settings. Retry with filename.'
            raise ValueError(msg)

    make_setting_pickle(json_file)
