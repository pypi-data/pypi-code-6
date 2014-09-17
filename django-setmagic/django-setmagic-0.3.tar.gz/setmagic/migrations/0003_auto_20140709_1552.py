# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setmagic', '0002_setting_current_value'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='setting',
            name='group',
        ),
        migrations.DeleteModel(
            name='Group',
        ),
    ]
