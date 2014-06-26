# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import datetime
import logging
import textwrap
from optparse import make_option

from django.core.management.base import BaseCommand

from ralph.util import plugin
from ralph_pricing.app import setup_scrooge_logger
from ralph.discovery.models import DiskShare


logger = logging.getLogger(__name__)


class PluginError(Exception):
    pass


class Command(BaseCommand):
    """Retrieve data for pricing for today"""

    help = textwrap.dedent(__doc__).strip()
    requires_model_validation = True
    option_list = BaseCommand.option_list + (
        make_option(
            '--today',
            dest='today',
            default=None,
            help="Save the synchronised results under the specified date.",
        ),
        make_option(
            '--run-only',
            dest='run_only',
            default=None,
            help="Run only the selected plugin, ignore dependencies.",
        ),
    )

    def handle(self, today, run_only, *args, **options):
        template = "{0};{1};{2};{3};{4};{5};{6}"
        results = []
        wwns = {}

        with open('/Users/ext_slawomir.sawicki/share_logs/found.csv') as f:   
            for line in f.readlines():
                line = line.split(';')
                wwns[line[2]] = [line[0], line[1]]
        '''
        with open('/Users/ext_slawomir.sawicki/share_logs/not_found.csv') as f:   
            for line in f.readlines():
                line = line.decode('utf-8', 'ignore').split(';')
                wwns[line[0]] = [line[2], line[3]]
        '''
        for disk_share in DiskShare.objects.filter(device__id__in=[501121L, 300549L, 2109927L, 299819L, 2104217L, 501115L, 300541L]):
            if disk_share.wwn in wwns:
                result = template.format(
                    disk_share.wwn,
                    disk_share.size,
                    disk_share.label,
                    disk_share.device.name,
                    disk_share.device.id,
                    wwns[disk_share.wwn][0],
                    wwns[disk_share.wwn][1],
                )
            else:
                result = template.format(
                    disk_share.wwn,
                    disk_share.size,
                    disk_share.label,
                    disk_share.device.name,
                    disk_share.device.id,
                    None,
                    None,
                )
            results.append(result)

        with open('/Users/ext_slawomir.sawicki/share_logs/disk_share_from_venture.csv', 'a+') as f:
            for result in results:
                f.write(result + '\n')