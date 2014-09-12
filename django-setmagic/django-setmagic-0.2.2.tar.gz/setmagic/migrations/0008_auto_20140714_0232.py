# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setmagic', '0007_auto_20140713_0121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setting',
            name='current_value',
            field=models.TextField(null=True, blank=True),
        ),
    ]
