# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Email'
        db.create_table(u'email_helper_email', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('when', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 5, 0, 0))),
            ('whom', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=254)),
        ))
        db.send_create_signal(u'email_helper', ['Email'])


    def backwards(self, orm):
        # Deleting model 'Email'
        db.delete_table(u'email_helper_email')


    models = {
        u'email_helper.email': {
            'Meta': {'object_name': 'Email'},
            'body': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'when': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 5, 0, 0)'}),
            'whom': ('django.db.models.fields.CharField', [], {'max_length': '254'})
        }
    }

    complete_apps = ['email_helper']