# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'MutexModel'
        db.create_table('m3_mutex', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mutex_group', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('mutex_mode', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('mutex_id', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('owner_session', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('owner_host', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('owner_id', self.gf('django.db.models.fields.CharField')(default='system', max_length=40)),
            ('owner_login', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('owner_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('auto_release_rule', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('auto_release_config', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('captured_since', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('m3_mutex', ['MutexModel'])


    def backwards(self, orm):
        
        # Deleting model 'MutexModel'
        db.delete_table('m3_mutex')


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
            'owner_session': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['m3_mutex']
