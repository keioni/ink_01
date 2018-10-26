# -*- coding: utf-8 -*-
"""INK system utilities module.
"""

from base64 import b64encode
import hashlib
import sys

from ink.sys.config import CONF


def verbose_print(msg: str):
    """
    Verbose Printer.

    Print called message if verbose mode is on.
    """

    if CONF.debug.verbose and CONF.debug.verbose_level:
        verbose_level = CONF.debug.verbose_level
    else:
        return

    if verbose_level > 1:
        print('> ' + msg, file=sys.stderr)
    if verbose_level > 2:
        print('>> ' + msg, file=sys.stderr)


def secure_hash(value: str, salt: str) -> str:
    """
    Secure Hash Function

    secure_hashing() is hashing arg[1] string and return hashed string.
    Using hash function is BLAKE2B and digest size is 32.
    """

    salt = salt.encode('utf-8')
    # https://github.com/PyCQA/pylint/issues/2478
    # https://github.com/PyCQA/pylint/issues/2551
    hashobj = hashlib.blake2b(key=salt, digest_size=32)  # pylint: disable=E1123
    hashobj.update(value.encode('utf-8'))
    return b64encode(hashobj.digest()).decode()
