# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setmagic', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='current_value',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
