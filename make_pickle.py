#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pickle
import json
import sys


def get_filenames() -> tuple:
    conf_file = ''
    pickle_file = ''
    if len(sys.argv) > 1:
        conf_file = sys.argv[1]
        if len(sys.argv) > 2:
            pickle_file = sys.argv[2]
    else:
        if 'INK_CONF_FILE' in os.environ:
            conf_file = os.environ.get('INK_CONF_FILE')
        else:
            conf_dir = os.path.dirname(__file__)
            conf_file = os.path.abspath(conf_dir + '/var/settings.json')

    if not pickle_file:
        pickle_file = conf_file.replace('.json', '.pickle')
    return (conf_file, pickle_file)

if __name__ == '__main__':
    print('== Pickle Maker ==')
    conf_file, pickle_file = get_filenames()
    with open(conf_file, 'rb') as fpr:
        conf = json.load(fpr)
    print('Conf file: {}'.format(conf_file))
    with open(pickle_file, 'wb') as fpw:
        pickle.dump(conf, fpw)
    print('Pickle file: {}'.format(pickle_file))
