# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ChartJSPieWidget'
        db.create_table(u'widgets_chartjspiewidget', (
            (u'widgetbase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['widgets.WidgetBase'], unique=True, primary_key=True)),
            ('labels_element', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('data_element', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
        ))
        db.send_create_signal(u'widgets', ['ChartJSPieWidget'])


    def backwards(self, orm):
        # Deleting model 'ChartJSPieWidget'
        db.delete_table(u'widgets_chartjspiewidget')


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
        u'widgets.chartjspiewidget': {
            'Meta': {'object_name': 'ChartJSPieWidget'},
            'data_element': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'labels_element': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            u'widgetbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['widgets.WidgetBase']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'widgets.chartjsradarwidget': {
            'Meta': {'object_name': 'ChartJSRadarWidget'},
            'data_element': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'labels_element': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            u'widgetbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['widgets.WidgetBase']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'widgets.justgagewidget': {
            'Meta': {'ordering': "(u'label',)", 'object_name': 'JustgageWidget', '_ormbases': [u'widgets.WidgetBase']},
            'legend': ('django.db.models.fields.CharField', [], {'max_length': '48'}),
            'maximum': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'minimum': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '48', 'blank': 'True'}),
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
            'javascript_code': ('django.db.models.fields.TextField', [], {'default': 'u\'\\n        var data = [\\n            {\\n                value: 300,\\n                color:"#F7464A",\\n                highlight: "#FF5A5E",\\n                label: "Red"\\n            },\\n            {\\n                value: 50,\\n                color: "#46BFBD",\\n                highlight: "#5AD3D1",\\n                label: "Green"\\n            },\\n            {\\n                value: 100,\\n                color: "#FDB45C",\\n                highlight: "#FFC870",\\n                label: "Yellow"\\n            }\\n        ]\\n    \'', 'blank': 'True'}),
            'javascript_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'python_code': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'python_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['widgets']