# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Host'
        db.create_table(u'datasources_host', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('netloc', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'datasources', ['Host'])

        # Adding model 'Datasource'
        db.create_table(u'datasources_datasource', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('host', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datasources.Host'])),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=96)),
            ('path', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'datasources', ['Datasource'])


    def backwards(self, orm):
        # Deleting model 'Host'
        db.delete_table(u'datasources_host')

        # Deleting model 'Datasource'
        db.delete_table(u'datasources_datasource')


    models = {
        u'datasources.datasource': {
            'Meta': {'object_name': 'Datasource'},
            'host': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datasources.Host']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '96'}),
            'path': ('django.db.models.fields.TextField', [], {})
        },
        u'datasources.host': {
            'Meta': {'object_name': 'Host'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'netloc': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['datasources']