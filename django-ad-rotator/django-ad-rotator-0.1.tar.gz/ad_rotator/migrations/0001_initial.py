# flake8: noqa
# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BannerAd'
        db.create_table(u'ad_rotator_bannerad', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('link_url', self.gf('django.db.models.fields.URLField')(max_length=256)),
            ('link_alt_text', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'ad_rotator', ['BannerAd'])


    def backwards(self, orm):
        # Deleting model 'BannerAd'
        db.delete_table(u'ad_rotator_bannerad')


    models = {
        u'ad_rotator.bannerad': {
            'Meta': {'ordering': "('start_date',)", 'object_name': 'BannerAd'},
            'end_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'link_alt_text': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'link_url': ('django.db.models.fields.URLField', [], {'max_length': '256'}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        }
    }

    complete_apps = ['ad_rotator']
