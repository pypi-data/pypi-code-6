# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mpesa', '0002_auto_20141013_1222'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mpesapayment',
            old_name='transaction_code',
            new_name='reference_number',
        ),
    ]
