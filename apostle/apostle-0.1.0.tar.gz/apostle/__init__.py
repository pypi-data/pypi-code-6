# -*- coding: utf-8 -*-

__title__ = 'apostle'
__version__ = '0.1.0'
__build__ = 0x000100
__author__ = 'Mal Curtis'
__license__ = 'MIT'
__copyright__ = 'Copyright 2013 Apostle.io'

import os

domain_key = os.getenv('APOSTLE_DOMAIN_KEY')
delivery_host = os.getenv('APOSTLE_DELIVERY_HOST', 'https://deliver.apostle.io')

from apostle.exceptions import ValidationError
from apostle.mail import Mail
from apostle.queue import Queue

def deliver(template_id, options):
	if not template_id:
		raise exceptions.ValidationError("No template id provided")
	if not options and not "email" in options:
		raise exceptions.ValidationError("No email address provided")

	queue = get_queue()
	queue.add(Mail(template_id, options))
	queue.deliver()


def get_queue():
	return Queue()
