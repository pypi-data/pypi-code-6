#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, errno
import re
import sys
import time
import datetime
import gzip
import glob
import json

from datetime import datetime
from pprint import pprint
from optparse import make_option
from os.path import expanduser
from django.core.management.base import BaseCommand, CommandError
from django.template import Context, Template
from django.conf import settings as conf
from django.utils import timezone

import rstamper.models as mymodels


# Class MUST be named 'Command'
class Command(BaseCommand):

    # Displayed from 'manage.py help mycommand'
    help = """
    Tool that tries to import stamps from a .json file:

    ./manage.py import

    """

    option_list = BaseCommand.option_list + (
            make_option('--file',
                dest='file',
                default=expanduser('~/.workstamps.json'),
                help='File to import (~/.workstamps.json by default)'),
            )

    def handle(self, *app_labels, **options):
        """
        The command itself
        """

        with open(options['file'], 'r') as f:
            json_data = json.load(f)

        # Deleting customers and stamps
        mymodels.Customer.objects.all().delete()
        mymodels.Stamp.objects.all().delete()

        # Special customer
        cus = mymodels.Customer(name='None')
        cus.save()

        for stamp in json_data:
            if stamp['customer']:
                try:
                    cus = mymodels.Customer(name=stamp['customer'])
                    cus.save()
                    print "[+] Customer: %s" % stamp['customer']
                except:
                    cus = mymodels.Customer.objects.get(name=stamp['customer'])
            else:
                cus = mymodels.Customer.objects.get(name='None')

            try:
                start = None
                end = None
                if stamp['start'] and stamp['end']:
                    if stamp['start']:
                        start = datetime.strptime(stamp['start'], '%Y-%m-%d %H:%M')
                        start=timezone.make_aware(start, timezone.get_current_timezone())
                    if stamp['end']:
                        end = datetime.strptime(stamp['end'], '%Y-%m-%d %H:%M')
                        end=timezone.make_aware(end, timezone.get_current_timezone())
                    stamp = mymodels.Stamp(
                        action=stamp['action'],
                        customer=cus,
                        start=start,
                        end=end,
                        )
                    stamp.save()
            except Exception as e:
                print "Error: %s" % e
