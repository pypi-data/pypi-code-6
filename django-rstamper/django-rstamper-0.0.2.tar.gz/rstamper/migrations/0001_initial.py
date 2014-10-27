# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Customer'
        db.create_table('rstamper_customer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('rstamper', ['Customer'])

        # Adding model 'Stamp'
        db.create_table('rstamper_stamp', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='customer', to=orm['rstamper.Customer'])),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('end', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('rstamper', ['Stamp'])


    def backwards(self, orm):
        # Deleting model 'Customer'
        db.delete_table('rstamper_customer')

        # Deleting model 'Stamp'
        db.delete_table('rstamper_stamp')


    models = {
        'rstamper.customer': {
            'Meta': {'object_name': 'Customer'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'rstamper.stamp': {
            'Meta': {'object_name': 'Stamp'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'customer'", 'to': "orm['rstamper.Customer']"}),
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['rstamper']