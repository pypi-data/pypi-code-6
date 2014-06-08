#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random


def hash_password(password, maxtime=0.5, length=64):
    import scrypt
    rand_str = ''.join(chr(random.randint(0, 255)) for i in range(length))
    return scrypt.encrypt(rand_str, password, maxtime=maxtime)


def verify_password(hashed_password, guessed_password, maxtime=0.5):
    try:
        import scrypt
        scrypt.decrypt(hashed_password, guessed_password, maxtime)
        return True
    except scrypt.error:
        return False

# vim: filetype=python
