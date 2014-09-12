# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import sitecats.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Title', help_text='Category name.')),
                ('alias', sitecats.models.CharFieldNullable(verbose_name='Alias', unique=True, max_length=80, blank=True, null=True, help_text='Short name to address category from application code.')),
                ('is_locked', models.BooleanField(default=False, verbose_name='Locked', help_text='Categories addressed from application code are locked, their aliases can not be changed. Such categories can be deleted from application code only.')),
                ('note', models.TextField(blank=True, verbose_name='Note')),
                ('status', models.IntegerField(db_index=True, blank=True, verbose_name='Status', null=True)),
                ('slug', sitecats.models.CharFieldNullable(max_length=250, blank=True, verbose_name='Slug', unique=True, null=True)),
                ('time_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('time_modified', models.DateTimeField(auto_now=True, verbose_name='Date modified')),
                ('sort_order', models.PositiveIntegerField(db_index=True, default=0, verbose_name='Sort order', help_text='Item position among other categories under the same parent.')),
                ('creator', models.ForeignKey(related_name='category_creators', verbose_name='Creator', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(verbose_name='Parent', related_name='category_parents', blank=True, null=True, help_text='Parent category.', to='sitecats.Category')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(blank=True, verbose_name='Note')),
                ('status', models.IntegerField(db_index=True, blank=True, verbose_name='Status', null=True)),
                ('time_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('object_id', models.PositiveIntegerField(db_index=True, verbose_name='Object ID')),
                ('category', models.ForeignKey(related_name='tie_categories', verbose_name='Category', to='sitecats.Category')),
                ('content_type', models.ForeignKey(related_name='sitecats_tie_tags', verbose_name='Content type', to='contenttypes.ContentType')),
                ('creator', models.ForeignKey(related_name='tie_creators', verbose_name='Creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Ties',
                'verbose_name': 'Tie',
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together=set([('title', 'parent')]),
        ),
    ]
