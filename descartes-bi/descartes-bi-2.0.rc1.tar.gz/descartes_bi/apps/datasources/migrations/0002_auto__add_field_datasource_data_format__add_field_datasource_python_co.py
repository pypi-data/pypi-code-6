# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Datasource.data_format'
        db.add_column(u'datasources_datasource', 'data_format',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=1),
                      keep_default=False)

        # Adding field 'Datasource.python_code'
        db.add_column(u'datasources_datasource', 'python_code',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'Datasource.python_enabled'
        db.add_column(u'datasources_datasource', 'python_enabled',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Datasource.data_format'
        db.delete_column(u'datasources_datasource', 'data_format')

        # Deleting field 'Datasource.python_code'
        db.delete_column(u'datasources_datasource', 'python_code')

        # Deleting field 'Datasource.python_enabled'
        db.delete_column(u'datasources_datasource', 'python_enabled')


    models = {
        u'datasources.datasource': {
            'Meta': {'object_name': 'Datasource'},
            'data_format': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'host': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datasources.Host']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '96'}),
            'path': ('django.db.models.fields.TextField', [], {}),
            'python_code': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'python_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'datasources.host': {
            'Meta': {'object_name': 'Host'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'netloc': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['datasources']