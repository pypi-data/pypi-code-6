# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.management.base import BaseCommand, CommandError

from distributed_task.broker import get_broker
from distributed_task.core.handler import task_handler
from distributed_task.exceptions import BrokerConnectionError


class Command(BaseCommand):

    help = "Foo."
    args = "ip address [ip address] ..."

    def handle(self, *args, **options):

        try:
            broker = get_broker()

            # broker.consume_message(task_handler)
            broker.keep_consuming(task_handler)

        except BrokerConnectionError, e:
            self.stderr.write("Connection to broker failed: %s" % e)
        except KeyboardInterrupt:
            self.stdout.write("Stopped.")