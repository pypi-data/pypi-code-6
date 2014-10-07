# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('sitemapper', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitemapentry',
            name='changefreq',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Change frequency', choices=[(10, b'always'), (20, b'hourly'), (30, b'daily'), (40, b'weekly'), (50, b'monthly'), (60, b'yearly'), (70, b'never')]),
        ),
        migrations.AlterField(
            model_name='sitemapentry',
            name='priority',
            field=models.DecimalField(decimal_places=1, choices=[(Decimal('0'), b'0.0'), (Decimal('0.1'), b'0.1'), (Decimal('0.2'), b'0.2'), (Decimal('0.3'), b'0.3'), (Decimal('0.4'), b'0.4'), (Decimal('0.5'), b'0.5'), (Decimal('0.6'), b'0.6'), (Decimal('0.7'), b'0.7'), (Decimal('0.8'), b'0.8'), (Decimal('0.9'), b'0.9'), (Decimal('1'), b'1.0')], max_digits=2, blank=True, null=True, verbose_name='priority'),
        ),
    ]
