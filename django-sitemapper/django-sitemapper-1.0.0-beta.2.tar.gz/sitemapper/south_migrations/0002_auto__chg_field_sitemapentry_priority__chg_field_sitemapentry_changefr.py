# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'SitemapEntry.priority'
        db.alter_column(u'sitemapper_sitemapentry', 'priority', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=2, decimal_places=1))

        # Changing field 'SitemapEntry.changefreq'
        db.alter_column(u'sitemapper_sitemapentry', 'changefreq', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True))

    def backwards(self, orm):

        # Changing field 'SitemapEntry.priority'
        db.alter_column(u'sitemapper_sitemapentry', 'priority', self.gf('django.db.models.fields.DecimalField')(default='0.5', max_digits=2, decimal_places=1))

        # Changing field 'SitemapEntry.changefreq'
        db.alter_column(u'sitemapper_sitemapentry', 'changefreq', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=30))

    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'sitemapper.sitemapentry': {
            'Meta': {'unique_together': "(['content_type', 'object_id'],)", 'object_name': 'SitemapEntry'},
            'changefreq': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'priority': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '2', 'decimal_places': '1', 'blank': 'True'})
        }
    }

    complete_apps = ['sitemapper']