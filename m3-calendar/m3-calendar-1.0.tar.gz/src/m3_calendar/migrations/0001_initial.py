# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ExceptedDay'
        db.create_table('m3_calendar_exceptedday', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('day', self.gf('django.db.models.fields.DateField')()),
            ('type', self.gf('django.db.models.fields.SmallIntegerField')()),
        ))
        db.send_create_signal('m3_calendar', ['ExceptedDay'])


    def backwards(self, orm):
        
        # Deleting model 'ExceptedDay'
        db.delete_table('m3_calendar_exceptedday')


    models = {
        'm3_calendar.exceptedday': {
            'Meta': {'object_name': 'ExceptedDay'},
            'day': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'type': ('django.db.models.fields.SmallIntegerField', [], {})
        }
    }

    complete_apps = ['m3_calendar']
