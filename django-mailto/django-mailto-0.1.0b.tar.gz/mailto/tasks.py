# -*- coding: utf-8 -*-
from __future__ import absolute_import

from mailto.models import mailto


try:
    from celery import shared_task

    @shared_task
    def task_mailto(args, kwargs):
        mailto(*args, **kwargs)

except ImportError:
    pass