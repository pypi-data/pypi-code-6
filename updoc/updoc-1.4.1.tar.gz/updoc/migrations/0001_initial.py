# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Keyword'
        db.create_table('updoc_keyword', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
        ))
        db.send_create_signal('updoc', ['Keyword'])

        # Adding model 'UploadDoc'
        db.create_table('updoc_uploaddoc', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uid', self.gf('django.db.models.fields.CharField')(max_length=50, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, default='', db_index=True)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('upload_time', self.gf('django.db.models.fields.DateTimeField')(blank=True, db_index=True, auto_now_add=True)),
        ))
        db.send_create_signal('updoc', ['UploadDoc'])

        # Adding M2M table for field keywords on 'UploadDoc'
        m2m_table_name = db.shorten_name('updoc_uploaddoc_keywords')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('uploaddoc', models.ForeignKey(orm['updoc.uploaddoc'], null=False)),
            ('keyword', models.ForeignKey(orm['updoc.keyword'], null=False))
        ))
        db.create_unique(m2m_table_name, ['uploaddoc_id', 'keyword_id'])

        # Adding model 'LastDocs'
        db.create_table('updoc_lastdocs', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('doc', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['updoc.UploadDoc'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('count', self.gf('django.db.models.fields.IntegerField')(default=1, blank=True, db_index=True)),
            ('last', self.gf('django.db.models.fields.DateTimeField')(blank=True, db_index=True, auto_now=True)),
        ))
        db.send_create_signal('updoc', ['LastDocs'])


    def backwards(self, orm):
        # Deleting model 'Keyword'
        db.delete_table('updoc_keyword')

        # Deleting model 'UploadDoc'
        db.delete_table('updoc_uploaddoc')

        # Removing M2M table for field keywords on 'UploadDoc'
        db.delete_table(db.shorten_name('updoc_uploaddoc_keywords'))

        # Deleting model 'LastDocs'
        db.delete_table('updoc_lastdocs')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Group']", 'blank': 'True', 'related_name': "'user_set'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Permission']", 'blank': 'True', 'related_name': "'user_set'"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)", 'db_table': "'django_content_type'", 'object_name': 'ContentType'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'updoc.keyword': {
            'Meta': {'object_name': 'Keyword'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        'updoc.lastdocs': {
            'Meta': {'object_name': 'LastDocs'},
            'count': ('django.db.models.fields.IntegerField', [], {'default': '1', 'blank': 'True', 'db_index': 'True'}),
            'doc': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['updoc.UploadDoc']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'db_index': 'True', 'auto_now': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'updoc.uploaddoc': {
            'Meta': {'object_name': 'UploadDoc'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['updoc.Keyword']", 'db_index': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "''", 'db_index': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'upload_time': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'db_index': 'True', 'auto_now_add': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['updoc']