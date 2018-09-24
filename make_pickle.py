#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Pickle Maker

Convert raw, readable, and formatted config file (json) to
Python independed 'pickle' file.
'''


import os
import pickle
import json
import sys


def pickle_maker():
    '''pickle_maker body
    '''

    conf_file = ''
    pickle_file = ''

    # get source file name (.json)
    if len(sys.argv) > 1:
        conf_file = sys.argv[1]
    else:
        if 'INK_CONF_FILE' in os.environ:
            conf_file = os.environ.get('INK_CONF_FILE')
        else:
            d = os.path.dirname(__file__)
            conf_file = os.path.abspath(d + '/var/settings.json')

    # get destination file name (.pickle)
    if len(sys.argv) > 2:
        pickle_file = sys.argv[2]
    else:
        pickle_file = conf_file.replace('.json', '.pickle')

    # read and write
    with open(conf_file, 'rb') as fpr:
        conf = json.load(fpr)
    print('Conf file: {}'.format(conf_file))
    with open(pickle_file, 'wb') as fpw:
        pickle.dump(conf, fpw)
    print('Pickle file: {}'.format(pickle_file))

if __name__ == '__main__':
    print('== Pickle Maker ==')
    pickle_maker()
