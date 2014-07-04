# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'EmailLog.raw_email'
        db.add_column(u'email_filter_emaillog', 'raw_email', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True), keep_default=False)

        # Adding field 'EmailLog.message_id'
        db.add_column(u'email_filter_emaillog', 'message_id', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True), keep_default=False)

        # Adding field 'EmailLog.in_reply_to'
        db.add_column(u'email_filter_emaillog', 'in_reply_to', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True), keep_default=False)

        # Adding unique constraint on 'EmailRedirect', fields ['email_in', 'email_redirect']
        db.create_unique(u'email_filter_emailredirect', ['email_in', 'email_redirect'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'EmailRedirect', fields ['email_in', 'email_redirect']
        db.delete_unique(u'email_filter_emailredirect', ['email_in', 'email_redirect'])

        # Deleting field 'EmailLog.raw_email'
        db.delete_column(u'email_filter_emaillog', 'raw_email')

        # Deleting field 'EmailLog.message_id'
        db.delete_column(u'email_filter_emaillog', 'message_id')

        # Deleting field 'EmailLog.in_reply_to'
        db.delete_column(u'email_filter_emaillog', 'in_reply_to')


    models = {
        u'email_filter.emaillog': {
            'Meta': {'object_name': 'EmailLog'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_reply_to': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'message_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'raw_body': ('django.db.models.fields.TextField', [], {}),
            'raw_email': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}),
            'recipient': ('django.db.models.fields.CharField', [], {'max_length': '750'}),
            'sender': ('django.db.models.fields.EmailField', [], {'max_length': '250'}),
            'sent': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'email_filter.emailredirect': {
            'Meta': {'unique_together': "(('email_in', 'email_redirect'),)", 'object_name': 'EmailRedirect'},
            'email_in': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '250'}),
            'email_redirect': ('django.db.models.fields.EmailField', [], {'max_length': '250'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['email_filter']
