# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Query'
        db.create_table('query_builder_query', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('json_query', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('query_builder', ['Query'])


    def backwards(self, orm):
        
        # Deleting model 'Query'
        db.delete_table('query_builder_query')


    models = {
        'query_builder.query': {
            'Meta': {'object_name': 'Query'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'json_query': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        }
    }

    complete_apps = ['query_builder']
