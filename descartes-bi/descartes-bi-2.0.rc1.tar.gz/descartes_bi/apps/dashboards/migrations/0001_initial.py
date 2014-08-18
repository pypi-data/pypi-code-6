# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Dashboard'
        db.create_table(u'dashboards_dashboard', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=96)),
        ))
        db.send_create_signal(u'dashboards', ['Dashboard'])

        # Adding model 'DashboardElement'
        db.create_table(u'dashboards_dashboardelement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dashboard', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'elements', to=orm['dashboards.Dashboard'])),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('span', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('height', self.gf('django.db.models.fields.PositiveIntegerField')(default=300)),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, null=True, blank=True)),
        ))
        db.send_create_signal(u'dashboards', ['DashboardElement'])


    def backwards(self, orm):
        # Deleting model 'Dashboard'
        db.delete_table(u'dashboards_dashboard')

        # Deleting model 'DashboardElement'
        db.delete_table(u'dashboards_dashboardelement')


    models = {
        u'dashboards.dashboard': {
            'Meta': {'object_name': 'Dashboard'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '96'})
        },
        u'dashboards.dashboardelement': {
            'Meta': {'object_name': 'DashboardElement'},
            'dashboard': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'elements'", 'to': u"orm['dashboards.Dashboard']"}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'height': ('django.db.models.fields.PositiveIntegerField', [], {'default': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'span': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['dashboards']