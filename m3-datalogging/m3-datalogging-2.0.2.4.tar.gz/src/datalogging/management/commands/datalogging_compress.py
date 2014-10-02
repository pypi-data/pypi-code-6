#coding: utf-8
"""
File: datalogging_compress.py
Author: Rinat F Sabitov
"""
import os
import sys
import datetime
import tempfile
from zipfile import ZipFile
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from django.conf import settings
from django.core import management



class Command(BaseCommand):
    help = 'Archieve datalogging data'

    option_list = BaseCommand.option_list + (
        make_option('--destination',
            dest='destination',
            default=getattr(settings,'DATALOGGER_COMPRESS_DESTINATION', ''),
            help='Archieving destination folder'),
        make_option('--reset',
            action='store_true',
            dest='reset',
            default=False,
            help='Delete all data after compress'),
        )

    def handle(self, *args, **options):

        default_filename_template = 'datalogging-dump-%d-%m-%Y-%H-%M'
        filename_template = getattr(settings, 'DATALOGGER_COMPRESS_FILENAME_TEMPLATE',
                default_filename_template)

        with tempfile.NamedTemporaryFile() as tf:
            #так как dumpdata сливает все в stdout, нам не остается ничего
            #другого как подменить сам stdout
            sysout = sys.stdout
            try:
                sys.stdout = tf
                management.call_command('dumpdata', 'datalogging')
            finally:
                sys.stdout = sysout

            filename = datetime.datetime.now().strftime(filename_template)
            with ZipFile(os.path.join(options['destination'], '%s.zip' % filename), 'w') as myzip:
                myzip.write(tf.name, filename+'.json')

        if options['reset']:
            management.call_command('reset', 'datalogging')
