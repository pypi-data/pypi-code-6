# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pronoun',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=b'30')),
                ('description', models.CharField(max_length=256)),
                ('subject', models.CharField(help_text=b'He, she, it', max_length=b'10')),
                ('object', models.CharField(help_text=b'Her, him, it', max_length=b'10')),
                ('reflexive', models.CharField(help_text=b'Itself, himself, herself', max_length=b'15')),
                ('possessive_pronoun', models.CharField(help_text=b'Hers, his, its', max_length=b'10')),
                ('possessive_determiner', models.CharField(help_text=b'His, her, its', max_length=b'10')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
