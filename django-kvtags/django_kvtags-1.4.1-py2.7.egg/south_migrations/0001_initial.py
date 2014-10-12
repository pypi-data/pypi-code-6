# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tag'
        db.create_table(u'kvtags_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=50, db_index=True)),
        ))
        db.send_create_signal(u'kvtags', ['Tag'])

        # Adding model 'KeyValue'
        db.create_table(u'kvtags_keyvalue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(related_name='kv_pairs', to=orm['kvtags.Tag'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=50, db_index=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'kvtags', ['KeyValue'])

        # Adding unique constraint on 'KeyValue', fields ['tag', 'key']
        db.create_unique(u'kvtags_keyvalue', ['tag_id', 'key'])

        # Adding model 'TaggedItem'
        db.create_table(u'kvtags_taggeditem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(related_name='items', null=True, to=orm['kvtags.Tag'])),
            ('object_id', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
        ))
        db.send_create_signal(u'kvtags', ['TaggedItem'])

        # Adding unique constraint on 'TaggedItem', fields ['tag', 'object_id', 'content_type']
        db.create_unique(u'kvtags_taggeditem', ['tag_id', 'object_id', 'content_type_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'TaggedItem', fields ['tag', 'object_id', 'content_type']
        db.delete_unique(u'kvtags_taggeditem', ['tag_id', 'object_id', 'content_type_id'])

        # Removing unique constraint on 'KeyValue', fields ['tag', 'key']
        db.delete_unique(u'kvtags_keyvalue', ['tag_id', 'key'])

        # Deleting model 'Tag'
        db.delete_table(u'kvtags_tag')

        # Deleting model 'KeyValue'
        db.delete_table(u'kvtags_keyvalue')

        # Deleting model 'TaggedItem'
        db.delete_table(u'kvtags_taggeditem')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'kvtags.keyvalue': {
            'Meta': {'unique_together': "(('tag', 'key'),)", 'object_name': 'KeyValue'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'kv_pairs'", 'to': u"orm['kvtags.Tag']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'kvtags.tag': {
            'Meta': {'object_name': 'Tag'},
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        u'kvtags.taggeditem': {
            'Meta': {'unique_together': "(('tag', 'object_id', 'content_type'),)", 'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'null': 'True', 'to': u"orm['kvtags.Tag']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        }
    }

    complete_apps = ['kvtags']