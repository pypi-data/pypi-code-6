# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ChartJSLineWidget'
        db.create_table(u'widgets_chartjslinewidget', (
            (u'widgetbase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['widgets.WidgetBase'], unique=True, primary_key=True)),
            ('javascript', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=48)),
            ('minimum', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('maximum', self.gf('django.db.models.fields.IntegerField')(default=100)),
            ('legend', self.gf('django.db.models.fields.CharField')(max_length=48)),
        ))
        db.send_create_signal(u'widgets', ['ChartJSLineWidget'])


    def backwards(self, orm):
        # Deleting model 'ChartJSLineWidget'
        db.delete_table(u'widgets_chartjslinewidget')


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
            'legend': ('django.db.models.fields.CharField', [], {'max_length': '48'}),
            'maximum': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'minimum': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '48'}),
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