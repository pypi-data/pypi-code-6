# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'ChartJSLineWidget.title'
        db.delete_column(u'widgets_chartjslinewidget', 'title')

        # Deleting field 'ChartJSLineWidget.minimum'
        db.delete_column(u'widgets_chartjslinewidget', 'minimum')

        # Deleting field 'ChartJSLineWidget.maximum'
        db.delete_column(u'widgets_chartjslinewidget', 'maximum')

        # Deleting field 'ChartJSLineWidget.legend'
        db.delete_column(u'widgets_chartjslinewidget', 'legend')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'ChartJSLineWidget.title'
        raise RuntimeError("Cannot reverse this migration. 'ChartJSLineWidget.title' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'ChartJSLineWidget.title'
        db.add_column(u'widgets_chartjslinewidget', 'title',
                      self.gf('django.db.models.fields.CharField')(max_length=48),
                      keep_default=False)

        # Adding field 'ChartJSLineWidget.minimum'
        db.add_column(u'widgets_chartjslinewidget', 'minimum',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'ChartJSLineWidget.maximum'
        db.add_column(u'widgets_chartjslinewidget', 'maximum',
                      self.gf('django.db.models.fields.IntegerField')(default=100),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'ChartJSLineWidget.legend'
        raise RuntimeError("Cannot reverse this migration. 'ChartJSLineWidget.legend' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'ChartJSLineWidget.legend'
        db.add_column(u'widgets_chartjslinewidget', 'legend',
                      self.gf('django.db.models.fields.CharField')(max_length=48),
                      keep_default=False)


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
        u'widgets.chartjslinewidget': {
            'Meta': {'object_name': 'ChartJSLineWidget'},
            'javascript': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'widgetbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['widgets.WidgetBase']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'widgets.justgagewidget': {
            'Meta': {'object_name': 'JustgageWidget'},
            'javascript': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'legend': ('django.db.models.fields.CharField', [], {'max_length': '48'}),
            'maximum': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'minimum': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '48'}),
            u'widgetbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['widgets.WidgetBase']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'widgets.messagewidget': {
            'Meta': {'ordering': "(u'label',)", 'object_name': 'MessageWidget', '_ormbases': [u'widgets.WidgetBase']},
            'message': ('django.db.models.fields.TextField', [], {}),
            u'widgetbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['widgets.WidgetBase']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'widgets.novuslinechartwidget': {
            'Meta': {'object_name': 'NovusLineChartWidget'},
            'javascript': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'widgetbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['widgets.WidgetBase']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'widgets.websitewidget': {
            'Meta': {'ordering': "(u'label',)", 'object_name': 'WebsiteWidget', '_ormbases': [u'widgets.WidgetBase']},
            'load_content': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'widgetbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['widgets.WidgetBase']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'widgets.widgetbase': {
            'Meta': {'ordering': "(u'label',)", 'object_name': 'WidgetBase'},
            'datasource': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datasources.Datasource']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['widgets']