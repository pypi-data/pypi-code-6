# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'JustgageWidget.title'
        db.delete_column(u'widgets_justgagewidget', 'title')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'JustgageWidget.title'
        raise RuntimeError("Cannot reverse this migration. 'JustgageWidget.title' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'JustgageWidget.title'
        db.add_column(u'widgets_justgagewidget', 'title',
                      self.gf('django.db.models.fields.CharField')(max_length=48),
                      keep_default=False)


    models = {
        u'datasources.datasource': {
            'Meta': {'object_name': 'Datasource'},
            'data_format': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'host': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datasources.Host']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '96'}),
            'path': ('django.db.models.fields.TextField', [], {}),
            'python_code': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'python_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'datasources.host': {
            'Meta': {'object_name': 'Host'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'netloc': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'widgets.chartjsbarwidget': {
            'Meta': {'object_name': 'ChartJSBarWidget'},
            'data_element': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'labels_element': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            u'widgetbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['widgets.WidgetBase']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'widgets.chartjslinewidget': {
            'Meta': {'object_name': 'ChartJSLineWidget'},
            'data_element': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'labels_element': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            u'widgetbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['widgets.WidgetBase']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'widgets.justgagewidget': {
            'Meta': {'ordering': "(u'label',)", 'object_name': 'JustgageWidget', '_ormbases': [u'widgets.WidgetBase']},
            'legend': ('django.db.models.fields.CharField', [], {'max_length': '48'}),
            'maximum': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'minimum': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'widgetbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['widgets.WidgetBase']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'widgets.messagewidget': {
            'Meta': {'ordering': "(u'label',)", 'object_name': 'MessageWidget', '_ormbases': [u'widgets.WidgetBase']},
            'message': ('django.db.models.fields.TextField', [], {}),
            u'widgetbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['widgets.WidgetBase']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'widgets.novuslinechartwidget': {
            'Meta': {'ordering': "(u'label',)", 'object_name': 'NovusLineChartWidget', '_ormbases': [u'widgets.WidgetBase']},
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
            'javascript_code': ('django.db.models.fields.TextField', [], {'default': 'u\'\\n        var data = {\\n            labels: ["January", "February", "March", "April", "May", "June", "July"],\\n            datasets: [\\n                {\\n                    label: "My First dataset",\\n                    fillColor: "rgba(220,220,220,0.5)",\\n                    strokeColor: "rgba(220,220,220,0.8)",\\n                    highlightFill: "rgba(220,220,220,0.75)",\\n                    highlightStroke: "rgba(220,220,220,1)",\\n                    data: [65, 59, 80, 81, 56, 55, 40]\\n                },\\n                {\\n                    label: "My Second dataset",\\n                    fillColor: "rgba(151,187,205,0.5)",\\n                    strokeColor: "rgba(151,187,205,0.8)",\\n                    highlightFill: "rgba(151,187,205,0.75)",\\n                    highlightStroke: "rgba(151,187,205,1)",\\n                    data: [28, 48, 40, 19, 86, 27, 90]\\n                }\\n            ]\\n        };\\n    \'', 'blank': 'True'}),
            'javascript_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'python_code': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'python_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['widgets']