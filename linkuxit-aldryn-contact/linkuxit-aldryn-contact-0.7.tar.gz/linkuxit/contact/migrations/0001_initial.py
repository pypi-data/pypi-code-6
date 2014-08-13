# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ContactPlugin'
        db.create_table(u'cmsplugin_contactplugin', (
            (u'cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('site_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('email_label', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('subject_label', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('content_label', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('thanks', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('submit', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
        ))
        db.send_create_signal(u'contact', ['ContactPlugin'])

        # Adding model 'Message'
        db.create_table(u'contact_message', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'contact', ['Message'])


    def backwards(self, orm):
        # Deleting model 'ContactPlugin'
        db.delete_table(u'cmsplugin_contactplugin')

        # Deleting model 'Message'
        db.delete_table(u'contact_message')


    models = {
        'cms.cmsplugin': {
            'Meta': {'object_name': 'CMSPlugin'},
            'changed_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.CMSPlugin']", 'null': 'True', 'blank': 'True'}),
            'placeholder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            'plugin_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'cms.placeholder': {
            'Meta': {'object_name': 'Placeholder'},
            'default_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        },
        u'contact.contactplugin': {
            'Meta': {'object_name': 'ContactPlugin', 'db_table': "u'cmsplugin_contactplugin'", '_ormbases': ['cms.CMSPlugin']},
            u'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'content_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'email_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'site_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'subject_label': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'submit': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'thanks': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'contact.message': {
            'Meta': {'object_name': 'Message'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['contact']