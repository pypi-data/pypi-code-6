# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Record'
        db.create_table(u'liver_record', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('record_job', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['liver.RecordJob'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=5000, blank=True)),
            ('insertion_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('modification_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, null=True, blank=True)),
            ('metadata_json', self.gf('django.db.models.fields.TextField')(max_length=5000, blank=True)),
            ('profiles_json', self.gf('django.db.models.fields.TextField')(max_length=5000, blank=True)),
            ('to_delete', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'liver', ['Record'])


    def backwards(self, orm):
        # Deleting model 'Record'
        db.delete_table(u'liver_record')


    models = {
        u'liver.record': {
            'Meta': {'object_name': 'Record'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insertion_date': ('django.db.models.fields.DateTimeField', [], {}),
            'metadata_json': ('django.db.models.fields.TextField', [], {'max_length': '5000', 'blank': 'True'}),
            'modification_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '5000', 'blank': 'True'}),
            'profiles_json': ('django.db.models.fields.TextField', [], {'max_length': '5000', 'blank': 'True'}),
            'record_job': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['liver.RecordJob']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'to_delete': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'liver.recorder': {
            'Meta': {'object_name': 'Recorder'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '5000'}),
            'token': ('django.db.models.fields.CharField', [], {'default': "'4023492e-3997-11e4-83cd-59cb9fdf41f7'", 'max_length': '5000'})
        },
        u'liver.recordjob': {
            'Meta': {'object_name': 'RecordJob'},
            'completion_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'execution_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insertion_date': ('django.db.models.fields.DateTimeField', [], {}),
            'modification_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'record_source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['liver.RecordSource']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'recorder': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['liver.Recorder']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'result': ('django.db.models.fields.CharField', [], {'default': "'None'", 'max_length': '5000', 'null': 'True', 'blank': 'True'}),
            'scheduled_duration': ('django.db.models.fields.IntegerField', [], {}),
            'scheduled_start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'sources_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['liver.SourcesGroup']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '5000'})
        },
        u'liver.recordjobmetadata': {
            'Meta': {'object_name': 'RecordJobMetadata'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '5000', 'blank': 'True'}),
            'record_job': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['liver.RecordJob']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '5000', 'blank': 'True'})
        },
        u'liver.recordmetadata': {
            'Meta': {'object_name': 'RecordMetadata'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '5000', 'blank': 'True'}),
            'record_source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['liver.RecordSource']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '5000', 'blank': 'True'})
        },
        u'liver.recordrule': {
            'Meta': {'object_name': 'RecordRule'},
            'availability_window': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metadata_key_filter': ('django.db.models.fields.CharField', [], {'max_length': '5000', 'blank': 'True'}),
            'metadata_value_filter': ('django.db.models.fields.CharField', [], {'max_length': '5000', 'blank': 'True'}),
            'offset_end': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'offset_start': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'record_source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['liver.RecordSource']"})
        },
        u'liver.recordsource': {
            'Meta': {'object_name': 'RecordSource'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'enabled_since': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'enabled_until': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insertion_date': ('django.db.models.fields.DateTimeField', [], {}),
            'modification_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'sources_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['liver.SourcesGroup']", 'null': 'True', 'blank': 'True'})
        },
        u'liver.source': {
            'Meta': {'object_name': 'Source'},
            'external_id': ('django.db.models.fields.CharField', [], {'max_length': '5000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insertion_date': ('django.db.models.fields.DateTimeField', [], {}),
            'modification_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '5000'}),
            'sources_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['liver.SourcesGroup']", 'null': 'True', 'blank': 'True'}),
            'uri': ('django.db.models.fields.CharField', [], {'max_length': '5000'})
        },
        u'liver.sourcesgroup': {
            'Meta': {'object_name': 'SourcesGroup'},
            'default_availability_window': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'default_offset_end': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'default_offset_start': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'external_id': ('django.db.models.fields.CharField', [], {'max_length': '5000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insertion_date': ('django.db.models.fields.DateTimeField', [], {}),
            'modification_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '5000'})
        }
    }

    complete_apps = ['liver']