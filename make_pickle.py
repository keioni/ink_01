#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pickle
import json
import sys


def make_conf_pickle(conf_file: str) -> bool:
    pickle_file = conf_file.replace('.json', '.pickle')
    with open(conf_file, 'rb') as fpr:
        conf = json.load(fpr)
    if conf:
        with open(pickle_file, 'wb') as fpw:
            pickle.dump(conf, fpw)
            return True
    return False

def get_conf_filename() -> tuple:
    conf_file = ''
    src = ''
    if len(sys.argv) > 1:
        conf_file = sys.argv[1]
        src = 'argument'
    if not conf_file:
        conf_file = os.environ.get('INK_conf_file')
        src = 'OS envvar'
    if not conf_file:
        conf_dir = os.path.dirname(__file__)
        conf_file = os.path.abspath(conf_dir + '/var/settings.json')
        src = 'hardcoded'
    return (conf_file, src)

if __name__ == '__main__':
    print('== Pickle Maker ==')
    exit_code = 1
    conf_file, src = get_conf_filename()
    if not conf_file:
        print('Cannot get conf filename.')
    else:
        print('Conf file by {}: {}'.format(src, conf_file))
        if os.path.exists(conf_file):
            if make_conf_pickle(conf_file):
                print('Succeeded!')
                exit_code = 0
            else:
                print('Failed: making pickle failed.')
        else:
            print('Failed: specified file not found.')
    sys.exit(exit_code)
