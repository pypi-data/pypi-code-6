# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MpesaTransaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ipn_id', models.CharField(unique=True, max_length=256, verbose_name='The IPN id.')),
                ('origin', models.CharField(max_length=128, verbose_name='This is the source of the notification.')),
                ('destination', phonenumber_field.modelfields.PhoneNumberField(max_length=128, verbose_name='This is your business terminal msidn(phone number)')),
                ('recieved_at', models.DateTimeField(verbose_name='The date and time at which the IPN was received')),
                ('message', models.TextField(verbose_name='The text message received from MPESA')),
                ('transaction_code', models.CharField(unique=True, max_length=16)),
                ('account', models.CharField(max_length=128, null=True, verbose_name='The account entered by the subscriber on their paybill transaction', blank=True)),
                ('subscriber_phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, verbose_name='The phone number from which this payment was made.')),
                ('subscriber_name', models.CharField(max_length=128, verbose_name="The sender's name")),
                ('transaction_datetime', models.DateTimeField(blank=True)),
                ('amount', models.DecimalField(max_digits=12, decimal_places=2)),
                ('paybill_number', models.IntegerField(verbose_name='The paybill number used for this transaction')),
                ('customer_id', models.CharField(max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
