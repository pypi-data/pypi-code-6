# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setmagic', '0004_auto_20140710_2333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setting',
            name='help_text',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='setting',
            name='label',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='setting',
            name='name',
            field=models.CharField(max_length=40, unique=True),
        ),
    ]
