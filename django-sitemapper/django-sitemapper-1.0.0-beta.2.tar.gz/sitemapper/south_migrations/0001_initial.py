# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SitemapEntry'
        db.create_table(u'sitemapper_sitemapentry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('changefreq', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('priority', self.gf('django.db.models.fields.DecimalField')(max_digits=2, decimal_places=1)),
        ))
        db.send_create_signal(u'sitemapper', ['SitemapEntry'])

        # Adding unique constraint on 'SitemapEntry', fields ['content_type', 'object_id']
        db.create_unique(u'sitemapper_sitemapentry', ['content_type_id', 'object_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'SitemapEntry', fields ['content_type', 'object_id']
        db.delete_unique(u'sitemapper_sitemapentry', ['content_type_id', 'object_id'])

        # Deleting model 'SitemapEntry'
        db.delete_table(u'sitemapper_sitemapentry')


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
            'changefreq': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'priority': ('django.db.models.fields.DecimalField', [], {'max_digits': '2', 'decimal_places': '1'})
        }
    }

    complete_apps = ['sitemapper']