# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ObjectUUID',
            fields=[
                ('uuid', django_extensions.db.fields.UUIDField(primary_key=True, serialize=False, editable=False, blank=True, verbose_name='UUID', name=b'uuid')),
                ('object_id', models.PositiveIntegerField(verbose_name='object id')),
                ('content_type', models.ForeignKey(verbose_name='content type', to='contenttypes.ContentType')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='objectuuid',
            unique_together=set([('object_id', 'content_type')]),
        ),
    ]
