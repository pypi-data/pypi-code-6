# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mpesa', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MpesaTransaction',
            new_name='MpesaPayment',
        ),
    ]
