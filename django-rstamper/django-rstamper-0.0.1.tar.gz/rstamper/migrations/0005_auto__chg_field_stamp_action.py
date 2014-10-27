# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Stamp.action'
        db.alter_column('rstamper_stamp', 'action', self.gf('django.db.models.fields.TextField')(max_length=255, null=True))

    def backwards(self, orm):

        # Changing field 'Stamp.action'
        db.alter_column('rstamper_stamp', 'action', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

    models = {
        'rstamper.customer': {
            'Meta': {'object_name': 'Customer'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'rstamper.stamp': {
            'Meta': {'object_name': 'Stamp'},
            'action': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'customer'", 'to': "orm['rstamper.Customer']"}),
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['rstamper']