# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'WebsiteWidget.load_content'
        db.add_column(u'widgets_websitewidget', 'load_content',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'WebsiteWidget.load_content'
        db.delete_column(u'widgets_websitewidget', 'load_content')


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
            'load_content': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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