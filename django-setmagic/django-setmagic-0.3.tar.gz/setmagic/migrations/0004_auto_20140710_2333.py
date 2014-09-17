# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setmagic', '0003_auto_20140709_1552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setting',
            name='current_value',
            field=models.CharField(max_length=100),
        ),
    ]
