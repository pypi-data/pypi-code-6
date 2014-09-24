# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'MutexModel.status_data'
        db.add_column('m3_mutex', 'status_data', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'MutexModel.status_data'
        db.delete_column('m3_mutex', 'status_data')


    models = {
        'm3_mutex.mutexmodel': {
            'Meta': {'object_name': 'MutexModel', 'db_table': "'m3_mutex'"},
            'auto_release_config': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'auto_release_rule': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'captured_since': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mutex_group': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'mutex_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'mutex_mode': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'owner_host': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'owner_id': ('django.db.models.fields.CharField', [], {'default': "'system'", 'max_length': '40'}),
            'owner_login': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'owner_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'owner_session': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'status_data': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['m3_mutex']
