# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Action'
        db.create_table(u'activity_action', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('actor_content_type', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'actor', null=True, to=orm['contenttypes.ContentType'])),
            ('actor_object_id', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('verb', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('action_content_type', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'action', null=True, to=orm['contenttypes.ContentType'])),
            ('action_object_id', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('target_content_type', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'target', null=True, to=orm['contenttypes.ContentType'])),
            ('target_object_id', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal(u'activity', ['Action'])


    def backwards(self, orm):
        # Deleting model 'Action'
        db.delete_table(u'activity_action')


    models = {
        u'activity.action': {
            'Meta': {'ordering': "(u'-timestamp',)", 'object_name': 'Action'},
            'action_content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'action'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'action_object_id': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'actor_content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'actor'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'actor_object_id': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'target_content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'target'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'target_object_id': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'verb': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['activity']