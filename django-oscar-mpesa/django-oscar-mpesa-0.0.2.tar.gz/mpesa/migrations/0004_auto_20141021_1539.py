# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mpesa', '0003_auto_20141015_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mpesapayment',
            name='message',
            field=models.TextField(verbose_name='The text message received from M-Pesa'),
        ),
        migrations.AlterField(
            model_name='mpesapayment',
            name='paybill_number',
            field=models.IntegerField(verbose_name='The Paybill number used for this transaction'),
        ),
    ]
