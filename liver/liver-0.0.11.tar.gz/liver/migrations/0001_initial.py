# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
import uuid

class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Source'
        db.create_table('liver_source', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=5000)),
            ('external_id', self.gf('django.db.models.fields.CharField')(max_length=5000)),
            ('uri', self.gf('django.db.models.fields.CharField')(max_length=5000)),
            ('insertion_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('modification_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, null=True, db_index=True, blank=True)),
            ('default_offset_start', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('default_availability_window', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('liver', ['Source'])

        # Adding model 'Recorder'
        db.create_table('liver_recorder', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=5000)),
            ('token', self.gf('django.db.models.fields.CharField')(default=str(uuid.uuid1()), max_length=5000)),
        ))
        db.send_create_signal('liver', ['Recorder'])

        # Adding model 'RecordSource'
        db.create_table('liver_recordsource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['liver.Source'], null=True, blank=True)),
            ('insertion_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('modification_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, null=True, db_index=True, blank=True)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('enabled_since', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
            ('enabled_until', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, db_index=True, blank=True)),
        ))
        db.send_create_signal('liver', ['RecordSource'])

        # Adding model 'RecordMetadata'
        db.create_table('liver_recordmetadata', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('record_source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['liver.RecordSource'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=5000, blank=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=5000, blank=True)),
        ))
        db.send_create_signal('liver', ['RecordMetadata'])

        # Adding model 'RecordRule'
        db.create_table('liver_recordrule', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('record_source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['liver.RecordSource'])),
            ('metadata_key_filter', self.gf('django.db.models.fields.CharField')(max_length=5000, blank=True)),
            ('metadata_value_filter', self.gf('django.db.models.fields.CharField')(max_length=5000, blank=True)),
            ('offset_start', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('availability_window', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('liver', ['RecordRule'])

        # Adding model 'RecordJob'
        db.create_table('liver_recordjob', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('record_source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['liver.RecordSource'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['liver.Source'])),
            ('insertion_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('modification_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, null=True, db_index=True, blank=True)),
            ('execution_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('completion_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('scheduled_start_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('scheduled_duration', self.gf('django.db.models.fields.IntegerField')()),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('recorder', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['liver.Recorder'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('result', self.gf('django.db.models.fields.CharField')(max_length=5000)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=5000)),
        ))
        db.send_create_signal('liver', ['RecordJob'])

        # Adding model 'RecordJobMetadata'
        db.create_table('liver_recordjobmetadata', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('record_job', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['liver.RecordJob'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=5000, blank=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=5000, blank=True)),
        ))
        db.send_create_signal('liver', ['RecordJobMetadata'])


    def backwards(self, orm):
        # Deleting model 'Source'
        db.delete_table('liver_source')

        # Deleting model 'Recorder'
        db.delete_table('liver_recorder')

        # Deleting model 'RecordSource'
        db.delete_table('liver_recordsource')

        # Deleting model 'RecordMetadata'
        db.delete_table('liver_recordmetadata')

        # Deleting model 'RecordRule'
        db.delete_table('liver_recordrule')

        # Deleting model 'RecordJob'
        db.delete_table('liver_recordjob')

        # Deleting model 'RecordJobMetadata'
        db.delete_table('liver_recordjobmetadata')


    models = {
        'liver.recorder': {
            'Meta': {'object_name': 'Recorder'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '5000'}),
            'token': ('django.db.models.fields.CharField', [], {'default': "'640e5b00-e68e-11e3-b443-0025b3ccbf54'", 'max_length': '5000'})
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
            'offset_start': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'record_source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['liver.RecordSource']"})
        },
        'liver.recordsource': {
            'Meta': {'object_name': 'RecordSource'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
