# -*- coding: utf-8 -*-

from django.db import models


class Audit(models.Model):
    command_name = models.CharField(max_length=80)
    date_started = models.DateTimeField()
    date_ended = models.DateTimeField()

    class Meta:
        app_label = 'management_audit'
