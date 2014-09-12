# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setmagic', '0005_auto_20140711_0818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setting',
            name='current_value',
            field=models.CharField(null=True, max_length=100),
        ),
    ]
