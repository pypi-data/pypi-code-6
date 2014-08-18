# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Dashboard.icon_code'
        db.delete_column(u'dashboards_dashboard', 'icon_code')


    def backwards(self, orm):
        # Adding field 'Dashboard.icon_code'
        db.add_column(u'dashboards_dashboard', 'icon_code',
                      self.gf('django.db.models.fields.TextField')(default=u'<i class="fa fa-tachometer"></i>', blank=True),
                      keep_default=False)


    models = {
        u'dashboards.dashboard': {
            'Meta': {'ordering': "(u'order',)", 'object_name': 'Dashboard'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'full_screen': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '96'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'})
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
            'Meta': {'ordering': "(u'label',)", 'object_name': 'Datasource'},
            'data_format': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
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
            'javascript_code': ('django.db.models.fields.TextField', [], {'default': 'u\'\\n        var data = [\\n            {\\n                value: 300,\\n                color:"#F7464A",\\n                highlight: "#FF5A5E",\\n                label: "Big"\\n            },\\n            {\\n                value: 50,\\n                color: "#46BFBD",\\n                highlight: "#5AD3D1",\\n                label: "Small"\\n            },\\n            {\\n                value: 100,\\n                color: "#FDB45C",\\n                highlight: "#FFC870",\\n                label: "Medium"\\n            }\\n        ]\\n    \'', 'blank': 'True'}),
            'javascript_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'python_code': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'python_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['dashboards']