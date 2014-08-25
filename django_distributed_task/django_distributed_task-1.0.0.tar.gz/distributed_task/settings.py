# from __future__ import unicode_literals

from django.conf import settings


SETTINGS = getattr(settings, 'DISTRIBUTED_TASK_BROKER', {})

BROKER_BACKEND = SETTINGS.get('BACKEND', 'distributed_task.broker.backends.dummy.DummyMessageBroker')
BROKER_OPTIONS = SETTINGS.get('OPTIONS', {})