# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Dashboard.icon_code'
        db.add_column(u'dashboards_dashboard', 'icon_code',
                      self.gf('django.db.models.fields.TextField')(default=u'<i class="fa fa-tachometer"></i>', blank=True),
                      keep_default=False)

        # Adding field 'Dashboard.description'
        db.add_column(u'dashboards_dashboard', 'description',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Dashboard.icon_code'
        db.delete_column(u'dashboards_dashboard', 'icon_code')

        # Deleting field 'Dashboard.description'
        db.delete_column(u'dashboards_dashboard', 'description')


    models = {
        u'dashboards.dashboard': {
            'Meta': {'object_name': 'Dashboard'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'icon_code': ('django.db.models.fields.TextField', [], {'default': 'u\'<i class="fa fa-tachometer"></i>\'', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '96'})
        },
        u'dashboards.dashboardelement': {
            'Meta': {'ordering': "(u'order',)", 'object_name': 'DashboardElement'},
            'dashboard': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'elements'", 'to': u"orm['dashboards.Dashboard']"}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'height': ('django.db.models.fields.PositiveIntegerField', [], {'default': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'span': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'widget': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['widgets.WidgetBase']"})
        },
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
        u'widgets.widgetbase': {
            'Meta': {'ordering': "(u'label',)", 'object_name': 'WidgetBase'},
            'datasource': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datasources.Datasource']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'javascript_code': ('django.db.models.fields.TextField', [], {'default': 'u\'\\n        var data = {\\n            labels: ["Eating", "Drinking", "Sleeping", "Designing", "Coding", "Cycling", "Running"],\\n            datasets: [\\n                {\\n                    label: "My First dataset",\\n                    fillColor: "rgba(220,220,220,0.2)",\\n                    strokeColor: "rgba(220,220,220,1)",\\n                    pointColor: "rgba(220,220,220,1)",\\n                    pointStrokeColor: "#fff",\\n                    pointHighlightFill: "#fff",\\n                    pointHighlightStroke: "rgba(220,220,220,1)",\\n                    data: [65, 59, 90, 81, 56, 55, 40]\\n                },\\n                {\\n                    label: "My Second dataset",\\n                    fillColor: "rgba(151,187,205,0.2)",\\n                    strokeColor: "rgba(151,187,205,1)",\\n                    pointColor: "rgba(151,187,205,1)",\\n                    pointStrokeColor: "#fff",\\n                    pointHighlightFill: "#fff",\\n                    pointHighlightStroke: "rgba(151,187,205,1)",\\n                    data: [28, 48, 40, 19, 96, 27, 100]\\n                }\\n            ]\\n        };\\n    \'', 'blank': 'True'}),
            'javascript_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'python_code': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'python_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['dashboards']