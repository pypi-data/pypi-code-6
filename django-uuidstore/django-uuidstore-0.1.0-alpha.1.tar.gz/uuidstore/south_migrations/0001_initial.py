# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ObjectUUID'
        db.create_table(u'uuidstore_objectuuid', (
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'uuidstore', ['ObjectUUID'])

        # Adding unique constraint on 'ObjectUUID', fields ['object_id', 'content_type']
        db.create_unique(u'uuidstore_objectuuid', ['object_id', 'content_type_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'ObjectUUID', fields ['object_id', 'content_type']
        db.delete_unique(u'uuidstore_objectuuid', ['object_id', 'content_type_id'])

        # Deleting model 'ObjectUUID'
        db.delete_table(u'uuidstore_objectuuid')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'uuidstore.objectuuid': {
            'Meta': {'unique_together': "(('object_id', 'content_type'),)", 'object_name': 'ObjectUUID'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        }
    }

    complete_apps = ['uuidstore']