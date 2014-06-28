#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import platform

if platform.system() == 'Linux':
    path = os.getcwd() + '/'

elif platform.system() == 'Windows':
    path = os.getcwd() + '\/'


def open_file_for_read(file):
    '''Open files for read only'''

    file = open(path + file, 'r')
    read = file.read()
    file.close()

    return read


def open_file_for_read_and_write(file):
    '''Open files for read and write'''

    return open(path + file, 'r+')


def write_to_file(file, result):
    '''Write results to a file'''

    file.seek(0)
    file.truncate()
    file.write(result)
    file.close()
