# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Tasks'
        db.create_table('m3_task_scheduler', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('task_name', self.gf('django.db.models.fields.CharField')(max_length=200, db_index=True)),
            ('proc_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('last_run', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('next_run', self.gf('django.db.models.fields.DateTimeField')()),
            ('period', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('executing', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('status', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('m3_task_scheduler', ['Tasks'])


    def backwards(self, orm):
        
        # Deleting model 'Tasks'
        db.delete_table('m3_task_scheduler')


    models = {
        'm3_task_scheduler.tasks': {
            'Meta': {'object_name': 'Tasks', 'db_table': "'m3_task_scheduler'"},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'executing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_run': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'next_run': ('django.db.models.fields.DateTimeField', [], {}),
            'period': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'proc_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'task_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'})
        }
    }

    complete_apps = ['m3_task_scheduler']
