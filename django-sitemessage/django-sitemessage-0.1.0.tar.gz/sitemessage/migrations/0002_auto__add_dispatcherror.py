# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DispatchError'
        db.create_table('sitemessage_dispatcherror', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('time_created', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
            ('dispatch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sitemessage.Dispatch'])),
            ('error_log', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('sitemessage', ['DispatchError'])


    def backwards(self, orm):
        # Deleting model 'DispatchError'
        db.delete_table('sitemessage_dispatcherror')


    models = {
        'apps.place': {
            'Meta': {'object_name': 'Place'},
            'geo_bounds': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '255'}),
            'geo_pos': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '255'}),
            'geo_title': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'geo_type': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '25', 'null': 'True', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'raters_num': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'rating': ('django.db.models.fields.FloatField', [], {'default': '0', 'db_index': 'True'}),
            'status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True', 'null': 'True'}),
            'time_published': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'user_title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'apps.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Group']", 'blank': 'True', 'related_name': "'user_set'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['apps.Place']", 'blank': 'True', 'null': 'True', 'related_name': "'users'"}),
            'raters_num': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'rating': ('django.db.models.fields.FloatField', [], {'default': '0', 'db_index': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Permission']", 'blank': 'True', 'related_name': "'user_set'"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission', 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'", 'ordering': "('name',)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'sitemessage.dispatch': {
            'Meta': {'object_name': 'Dispatch'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'dispatch_status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sitemessage.Message']"}),
            'message_cache': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'messenger': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '250'}),
            'read_status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['apps.User']", 'blank': 'True', 'null': 'True'}),
            'retry_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'time_dispatched': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'})
        },
        'sitemessage.dispatcherror': {
            'Meta': {'object_name': 'DispatchError'},
            'dispatch': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sitemessage.Dispatch']"}),
            'error_log': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'})
        },
        'sitemessage.message': {
            'Meta': {'object_name': 'Message'},
            'cls': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '250'}),
            'context': ('sitemessage.models.ContextField', [], {}),
            'dispatches_ready': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['apps.User']", 'blank': 'True', 'null': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'})
        }
    }

    complete_apps = ['sitemessage']