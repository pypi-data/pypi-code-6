# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Message'
        db.create_table('sitemessage_message', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['apps.User'], null=True, blank=True)),
            ('cls', self.gf('django.db.models.fields.CharField')(max_length=250, db_index=True)),
            ('context', self.gf('sitemessage.models.ContextField')()),
            ('dispatches_ready', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
        ))
        db.send_create_signal('sitemessage', ['Message'])

        # Adding model 'Dispatch'
        db.create_table('sitemessage_dispatch', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('time_dispatched', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('message', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sitemessage.Message'])),
            ('messenger', self.gf('django.db.models.fields.CharField')(max_length=250, db_index=True)),
            ('recipient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['apps.User'], null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('retry_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('message_cache', self.gf('django.db.models.fields.TextField')(null=True)),
            ('dispatch_status', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('read_status', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
        ))
        db.send_create_signal('sitemessage', ['Dispatch'])


    def backwards(self, orm):
        # Deleting model 'Message'
        db.delete_table('sitemessage_message')

        # Deleting model 'Dispatch'
        db.delete_table('sitemessage_dispatch')


    models = {
        'apps.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'to': "orm['auth.Group']", 'blank': 'True', 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'raters_num': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'rating': ('django.db.models.fields.FloatField', [], {'default': '0', 'db_index': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'to': "orm['auth.Permission']", 'blank': 'True', 'symmetrical': 'False'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
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
            'messenger': ('django.db.models.fields.CharField', [], {'max_length': '250', 'db_index': 'True'}),
            'read_status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['apps.User']", 'null': 'True', 'blank': 'True'}),
            'retry_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'time_dispatched': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'sitemessage.message': {
            'Meta': {'object_name': 'Message'},
            'cls': ('django.db.models.fields.CharField', [], {'max_length': '250', 'db_index': 'True'}),
            'context': ('sitemessage.models.ContextField', [], {}),
            'dispatches_ready': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['apps.User']", 'null': 'True', 'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['sitemessage']