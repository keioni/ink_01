#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hashlib import blake2b
from base64 import b64encode


def secure_hashing(value: str, salt: str) -> str:
    '''
    Secure Hash Function

    secure_hashing() is hashing arg[1] string and return hashed string.
    Using hash function is BLAKE2B and digest size is 32.
    '''
    salt = salt.encode('utf-8')
    # https://github.com/PyCQA/pylint/issues/2478
    h = blake2b(key=salt, digest_size=32) # pylint: disable=E1123
    h.update(value.encode('utf-8'))
    return b64encode(h.digest()).decode()
