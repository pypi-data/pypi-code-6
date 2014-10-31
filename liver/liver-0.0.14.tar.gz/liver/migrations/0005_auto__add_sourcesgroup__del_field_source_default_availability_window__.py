# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SourcesGroup'
        db.create_table(u'liver_sourcesgroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=5000)),
            ('external_id', self.gf('django.db.models.fields.CharField')(max_length=5000)),
            ('insertion_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('modification_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, null=True, blank=True)),
            ('default_offset_start', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('default_offset_end', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('default_availability_window', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'liver', ['SourcesGroup'])

        # Deleting field 'Source.default_availability_window'
        db.delete_column(u'liver_source', 'default_availability_window')

        # Deleting field 'Source.default_offset_start'
        db.delete_column(u'liver_source', 'default_offset_start')

        # Deleting field 'Source.default_offset_end'
        db.delete_column(u'liver_source', 'default_offset_end')

        # Adding field 'Source.source_group'
        db.add_column(u'liver_source', 'source_group',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['liver.SourcesGroup'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'SourcesGroup'
        db.delete_table(u'liver_sourcesgroup')

        # Adding field 'Source.default_availability_window'
        db.add_column(u'liver_source', 'default_availability_window',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Source.default_offset_start'
        db.add_column(u'liver_source', 'default_offset_start',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Source.default_offset_end'
        db.add_column(u'liver_source', 'default_offset_end',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Source.source_group'
        db.delete_column(u'liver_source', 'source_group_id')


    models = {
        u'liver.recorder': {
            'Meta': {'object_name': 'Recorder'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '5000'}),
            'token': ('django.db.models.fields.CharField', [], {'default': "'faeb56e6-3840-11e4-83cd-cf4dea1c091a'", 'max_length': '5000'})
        },
        u'liver.recordjob': {
            'Meta': {'object_name': 'RecordJob'},
            'completion_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'execution_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insertion_date': ('django.db.models.fields.DateTimeField', [], {}),
            'modification_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'record_source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['liver.RecordSource']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'recorder': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['liver.Recorder']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'result': ('django.db.models.fields.CharField', [], {'default': "'None'", 'max_length': '5000', 'null': 'True', 'blank': 'True'}),
            'scheduled_duration': ('django.db.models.fields.IntegerField', [], {}),
            'scheduled_start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['liver.Source']"}),
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
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['liver.Source']", 'null': 'True', 'blank': 'True'})
        },
        u'liver.source': {
            'Meta': {'object_name': 'Source'},
            'external_id': ('django.db.models.fields.CharField', [], {'max_length': '5000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insertion_date': ('django.db.models.fields.DateTimeField', [], {}),
            'modification_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '5000'}),
            'source_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['liver.SourcesGroup']", 'null': 'True', 'blank': 'True'}),
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