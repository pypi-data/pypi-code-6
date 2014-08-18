# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'WidgetBase'
        db.create_table(u'widgets_widgetbase', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('datasource', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['datasources.Datasource'], unique=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'widgets', ['WidgetBase'])

        # Adding model 'WebsiteWidget'
        db.create_table(u'widgets_websitewidget', (
            (u'widgetbase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['widgets.WidgetBase'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'widgets', ['WebsiteWidget'])

        # Adding model 'MessageWidget'
        db.create_table(u'widgets_messagewidget', (
            (u'widgetbase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['widgets.WidgetBase'], unique=True, primary_key=True)),
            ('message', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'widgets', ['MessageWidget'])


    def backwards(self, orm):
        # Deleting model 'WidgetBase'
        db.delete_table(u'widgets_widgetbase')

        # Deleting model 'WebsiteWidget'
        db.delete_table(u'widgets_websitewidget')

        # Deleting model 'MessageWidget'
        db.delete_table(u'widgets_messagewidget')


    models = {
        u'datasources.datasource': {
            'Meta': {'object_name': 'Datasource'},
            'host': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datasources.Host']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '96'}),
            'path': ('django.db.models.fields.TextField', [], {})
        },
        u'datasources.host': {
            'Meta': {'object_name': 'Host'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'netloc': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'widgets.messagewidget': {
            'Meta': {'ordering': "(u'label',)", 'object_name': 'MessageWidget', '_ormbases': [u'widgets.WidgetBase']},
            'message': ('django.db.models.fields.TextField', [], {}),
            u'widgetbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['widgets.WidgetBase']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'widgets.websitewidget': {
            'Meta': {'ordering': "(u'label',)", 'object_name': 'WebsiteWidget', '_ormbases': [u'widgets.WidgetBase']},
            u'widgetbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['widgets.WidgetBase']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'widgets.widgetbase': {
            'Meta': {'ordering': "(u'label',)", 'object_name': 'WidgetBase'},
            'datasource': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['datasources.Datasource']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['widgets']