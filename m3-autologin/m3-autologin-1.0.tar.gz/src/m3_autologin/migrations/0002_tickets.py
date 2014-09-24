# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'RemoteAuthTicket'
        db.create_table('m3_autologin_tickets', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_login', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('ticket_key', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('ticket_hash', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('m3_autologin', ['RemoteAuthTicket'])


    def backwards(self, orm):
        
        # Deleting model 'RemoteAuthTicket'
        db.delete_table('m3_autologin_tickets')


    models = {
        'm3_autologin.autologinaudit': {
            'Meta': {'object_name': 'AutoLoginAudit', 'db_table': "'m3_autologin_audit'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'remote_address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'type': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'user_fio': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '70', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'user_info': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'userid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'db_index': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '50', 'null': 'True', 'db_index': 'True', 'blank': 'True'})
        },
        'm3_autologin.remoteauthticket': {
            'Meta': {'object_name': 'RemoteAuthTicket', 'db_table': "'m3_autologin_tickets'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ticket_hash': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ticket_key': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'user_login': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['m3_autologin']
