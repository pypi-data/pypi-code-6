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

import requests

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
    Tool that tries to export stamps from a .json file:

    ./manage.py export

    """

    option_list = BaseCommand.option_list + (
            make_option(
                '--file',
                dest='file',
                default=expanduser('~/.workstamps.json'),
                help='File to import (~/.workstamps.json by default)'
            ),
            make_option(
                '--remote',
                default='http://oscarmlage.com/stamper/api/',
                dest='remote',
                help='API URL to export data'
            ),
        )

    def handle(self, *app_labels, **options):
        """
        The command itself
        """

        # Customers (bulk delete all the data)
        url = options['remote'] + 'customers/delete'
        res = requests.delete(url)

        # Customers (not bulk)
        url = options['remote'] + 'customers/'
        cus = mymodels.Customer.objects.all()
        data = {}
        remotedata = {}
        for c in cus:
            data = {'name': c.name}
            res = requests.post(url, data=json.dumps(data), headers=headers)
            resdata = json.loads(res.content)
            try:
                remotedata[resdata['id']] = resdata['name']
            except:
                pass
            #print res.status_code
            #print res.content

        # Stamps (bulk action)
        url = options['remote'] + 'stamps/'
        stamps = mymodels.Stamp.objects.all()
        data = []
        for stamp in stamps:
            for k,v in remotedata.items():
                if v == stamp.customer.name:
                    customer = k
            data.append({
                'action': stamp.action,
                'customer': customer,
                'start': stamp.start.strftime("%Y-%m-%d %H:%M"),
                'end': stamp.end.strftime("%Y-%m-%d %H:%M"),
            })
        res = requests.post(url, data=json.dumps(data), headers=headers)
