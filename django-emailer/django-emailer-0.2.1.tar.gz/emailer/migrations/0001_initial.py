# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConnectionProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('host', models.CharField(max_length=60)),
                ('username', models.CharField(max_length=40, blank=True)),
                ('password', models.CharField(max_length=40, blank=True)),
                ('port', models.PositiveSmallIntegerField()),
                ('use_tls', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('name', models.SlugField(serialize=False, primary_key=True)),
                ('base_template_name', models.CharField(default=b'email/default.html', max_length=70, blank=True)),
                ('subject', models.CharField(max_length=40)),
                ('content', models.TextField()),
                ('connection_profile', models.ForeignKey(to='emailer.ConnectionProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
