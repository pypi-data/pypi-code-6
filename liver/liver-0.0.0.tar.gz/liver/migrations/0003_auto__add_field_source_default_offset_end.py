# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Source.default_offset_end'
        db.add_column('liver_source', 'default_offset_end',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Source.default_offset_end'
        db.delete_column('liver_source', 'default_offset_end')


    models = {
        'liver.recorder': {
            'Meta': {'object_name': 'Recorder'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '5000'}),
            'token': ('django.db.models.fields.CharField', [], {'default': "'71d7e3d0-e695-11e3-abe0-0025b3ccbf54'", 'max_length': '5000'})
        },
        'liver.recordjob': {
            'Meta': {'object_name': 'RecordJob'},
            'completion_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'execution_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insertion_date': ('django.db.models.fields.DateTimeField', [], {}),
            'modification_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'record_source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['liver.RecordSource']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'recorder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['liver.Recorder']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'result': ('django.db.models.fields.CharField', [], {'max_length': '5000'}),
            'scheduled_duration': ('django.db.models.fields.IntegerField', [], {}),
            'scheduled_start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['liver.Source']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '5000'})
        },
        'liver.recordjobmetadata': {
            'Meta': {'object_name': 'RecordJobMetadata'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '5000', 'blank': 'True'}),
            'record_job': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['liver.RecordJob']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '5000', 'blank': 'True'})
        },
        'liver.recordmetadata': {
            'Meta': {'object_name': 'RecordMetadata'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '5000', 'blank': 'True'}),
            'record_source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['liver.RecordSource']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '5000', 'blank': 'True'})
        },
        'liver.recordrule': {
            'Meta': {'object_name': 'RecordRule'},
            'availability_window': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metadata_key_filter': ('django.db.models.fields.CharField', [], {'max_length': '5000', 'blank': 'True'}),
            'metadata_value_filter': ('django.db.models.fields.CharField', [], {'max_length': '5000', 'blank': 'True'}),
            'offset_end': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'offset_start': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'record_source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['liver.RecordSource']"})
        },
        'liver.recordsource': {
            'Meta': {'object_name': 'RecordSource'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'enabled_since': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'enabled_until': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insertion_date': ('django.db.models.fields.DateTimeField', [], {}),
            'modification_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['liver.Source']", 'null': 'True', 'blank': 'True'})
        },
        'liver.source': {
            'Meta': {'object_name': 'Source'},
            'default_availability_window': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'default_offset_end': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'default_offset_start': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'external_id': ('django.db.models.fields.CharField', [], {'max_length': '5000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insertion_date': ('django.db.models.fields.DateTimeField', [], {}),
            'modification_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '5000'}),
            'uri': ('django.db.models.fields.CharField', [], {'max_length': '5000'})
        }
    }

    complete_apps = ['liver']