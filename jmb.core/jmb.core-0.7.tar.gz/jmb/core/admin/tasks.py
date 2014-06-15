# -*- coding: utf-8 -*-
import time

from celery import Celery

from django.utils.encoding import force_unicode, smart_unicode
from django.utils.html import escape, strip_tags

from jmb.core.utils.functions import render_xls

app = Celery('tasks', broker='amqp://guest@localhost//')

# @app.task
def create_xls(model):
    opts = model._meta
    app_label = opts.app_label
    verbose_name = force_unicode(opts.verbose_name)

    queryset = model.objects.all()
    fields_list = model._meta.get_all_field_names()

    rows = [fields_list]

    list_objects = queryset.values_list(*fields_list)
    for object_values in list_objects:
        row = []
        for value in object_values:
            if value is None:
                value=''
            value = strip_tags(smart_unicode(value))
            row.append(value)
        rows.append(row)

    return render_xls(rows, '%s_%s.xls' % (app_label, verbose_name))
