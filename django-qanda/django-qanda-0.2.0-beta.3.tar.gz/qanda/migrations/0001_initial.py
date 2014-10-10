# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, verbose_name='created', blank=True)),
                ('modified', models.DateTimeField(null=True, verbose_name='modified', blank=True)),
                ('text', models.TextField(verbose_name='question')),
                ('slug', models.SlugField(unique=True, max_length=100, verbose_name='slug')),
                ('answer', models.TextField(verbose_name='answer', blank=True)),
                ('is_published', models.BooleanField(default=False, verbose_name='is published?')),
                ('access', models.PositiveSmallIntegerField(default=0, verbose_name='access', choices=[(0, 'Public'), (1, 'Members'), (2, 'Staff')])),
                ('order', models.IntegerField(default=0, verbose_name='sort order')),
            ],
            options={
                'ordering': ['order', 'created'],
                'verbose_name': 'question',
                'verbose_name_plural': 'questions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=150, verbose_name='title')),
                ('slug', models.SlugField(unique=True, max_length=150, verbose_name='slug')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('order', models.IntegerField(default=0, verbose_name='sort order')),
            ],
            options={
                'ordering': ['order', 'title'],
                'verbose_name': 'topic',
                'verbose_name_plural': 'topics',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='question',
            name='topic',
            field=models.ForeignKey(related_name=b'questions', verbose_name='topic', to='qanda.Topic'),
            preserve_default=True,
        ),
    ]
