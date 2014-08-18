# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'JustgageWidget.javascript'
        db.delete_column(u'widgets_justgagewidget', 'javascript')

        # Adding field 'WidgetBase.python_code'
        db.add_column(u'widgets_widgetbase', 'python_code',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'WidgetBase.python_enabled'
        db.add_column(u'widgets_widgetbase', 'python_enabled',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'WidgetBase.javascript_code'
        db.add_column(u'widgets_widgetbase', 'javascript_code',
                      self.gf('django.db.models.fields.TextField')(default=u'\n        var data = {\n            labels: ["January", "February", "March", "April", "May", "June", "July"],\n            datasets: [\n                {\n                    label: "My First dataset",\n                    fillColor: "rgba(220,220,220,0.2)",\n                    strokeColor: "rgba(220,220,220,1)",\n                    pointColor: "rgba(220,220,220,1)",\n                    pointStrokeColor: "#fff",\n                    pointHighlightFill: "#fff",\n                    pointHighlightStroke: "rgba(220,220,220,1)",\n                    data: [65, 59, 80, 81, 56, 55, 40]\n                },\n                {\n                    label: "My Second dataset",\n                    fillColor: "rgba(151,187,205,0.2)",\n                    strokeColor: "rgba(151,187,205,1)",\n                    pointColor: "rgba(151,187,205,1)",\n                    pointStrokeColor: "#fff",\n                    pointHighlightFill: "#fff",\n                    pointHighlightStroke: "rgba(151,187,205,1)",\n                    data: [28, 48, 40, 19, 86, 27, 90]\n                }\n            ]\n        };\n    ', blank=True),
                      keep_default=False)

        # Adding field 'WidgetBase.javascript_enabled'
        db.add_column(u'widgets_widgetbase', 'javascript_enabled',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Deleting field 'NovusLineChartWidget.javascript'
        db.delete_column(u'widgets_novuslinechartwidget', 'javascript')

        # Deleting field 'ChartJSLineWidget.javascript'
        db.delete_column(u'widgets_chartjslinewidget', 'javascript')


    def backwards(self, orm):
        # Adding field 'JustgageWidget.javascript'
        db.add_column(u'widgets_justgagewidget', 'javascript',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Deleting field 'WidgetBase.python_code'
        db.delete_column(u'widgets_widgetbase', 'python_code')

        # Deleting field 'WidgetBase.python_enabled'
        db.delete_column(u'widgets_widgetbase', 'python_enabled')

        # Deleting field 'WidgetBase.javascript_code'
        db.delete_column(u'widgets_widgetbase', 'javascript_code')

        # Deleting field 'WidgetBase.javascript_enabled'
        db.delete_column(u'widgets_widgetbase', 'javascript_enabled')

        # Adding field 'NovusLineChartWidget.javascript'
        db.add_column(u'widgets_novuslinechartwidget', 'javascript',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'ChartJSLineWidget.javascript'
        db.add_column(u'widgets_chartjslinewidget', 'javascript',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
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
            'Meta': {'ordering': "(u'label',)", 'object_name': 'ChartJSLineWidget', '_ormbases': [u'widgets.WidgetBase']},
            u'widgetbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['widgets.WidgetBase']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'widgets.justgagewidget': {
            'Meta': {'ordering': "(u'label',)", 'object_name': 'JustgageWidget', '_ormbases': [u'widgets.WidgetBase']},
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
            'javascript_code': ('django.db.models.fields.TextField', [], {'default': 'u\'\\n        var data = {\\n            labels: ["January", "February", "March", "April", "May", "June", "July"],\\n            datasets: [\\n                {\\n                    label: "My First dataset",\\n                    fillColor: "rgba(220,220,220,0.2)",\\n                    strokeColor: "rgba(220,220,220,1)",\\n                    pointColor: "rgba(220,220,220,1)",\\n                    pointStrokeColor: "#fff",\\n                    pointHighlightFill: "#fff",\\n                    pointHighlightStroke: "rgba(220,220,220,1)",\\n                    data: [65, 59, 80, 81, 56, 55, 40]\\n                },\\n                {\\n                    label: "My Second dataset",\\n                    fillColor: "rgba(151,187,205,0.2)",\\n                    strokeColor: "rgba(151,187,205,1)",\\n                    pointColor: "rgba(151,187,205,1)",\\n                    pointStrokeColor: "#fff",\\n                    pointHighlightFill: "#fff",\\n                    pointHighlightStroke: "rgba(151,187,205,1)",\\n                    data: [28, 48, 40, 19, 86, 27, 90]\\n                }\\n            ]\\n        };\\n    \'', 'blank': 'True'}),
            'javascript_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'python_code': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'python_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['widgets']