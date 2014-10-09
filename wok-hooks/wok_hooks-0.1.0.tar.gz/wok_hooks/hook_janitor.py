
import os
import logging


def clean_temp_files(options):
    for root, dirnames, filenames in os.walk('./', topdown=True):
        for filename in filenames:
            if filename[-1] == '~':
                logging.info('remove %s/%s', root, filename)
                os.remove(root + '/' + filename)
