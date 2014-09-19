# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Archive.author'
        db.alter_column('repository_archive', 'author_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))

        # Changing field 'Repository.author'
        db.alter_column('repository_repository', 'author_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))

        # Changing field 'Element.author'
        db.alter_column('repository_element', 'author_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))

        # Changing field 'ArchiveState.author'
        db.alter_column('repository_archivestate', 'author_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))

        # Changing field 'Version.author'
        db.alter_column('repository_version', 'author_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))

    def backwards(self, orm):

        # Changing field 'Archive.author'
        db.alter_column('repository_archive', 'author_id', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['auth.User']))

        # Changing field 'Repository.author'
        db.alter_column('repository_repository', 'author_id', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['auth.User']))

        # Changing field 'Element.author'
        db.alter_column('repository_element', 'author_id', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['auth.User']))

        # Changing field 'ArchiveState.author'
        db.alter_column('repository_archivestate', 'author_id', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['auth.User']))

        # Changing field 'Version.author'
        db.alter_column('repository_version', 'author_id', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['auth.User']))

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"})
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Group']", 'related_name': "'user_set'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']", 'related_name': "'user_set'"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)", 'db_table': "'django_content_type'", 'object_name': 'ContentType'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'repository.archive': {
            'Meta': {'object_name': 'Archive'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'creation': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'db_index': 'True', 'auto_now_add': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'modification': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'db_index': 'True', 'auto_now': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'official_link': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'})
        },
        'repository.archivestate': {
            'Meta': {'object_name': 'ArchiveState'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'creation': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'db_index': 'True', 'auto_now_add': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modification': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'db_index': 'True', 'auto_now': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'repository': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.Repository']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'})
        },
        'repository.element': {
            'Meta': {'object_name': 'Element'},
            'archive': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['repository.Archive']"}),
            'archive_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'default': "''", 'blank': 'True', 'null': 'True'}),
            'archive_key': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "''", 'blank': 'True', 'db_index': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'creation': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'db_index': 'True', 'auto_now_add': 'True'}),
            'extension': ('django.db.models.fields.CharField', [], {'max_length': '20', 'default': "''", 'blank': 'True', 'db_index': 'True'}),
            'extra_data': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "''", 'blank': 'True', 'db_index': 'True'}),
            'filesize': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True', 'db_index': 'True'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True', 'db_index': 'True'}),
            'full_name_normalized': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'md5': ('django.db.models.fields.CharField', [], {'max_length': '120', 'default': "''", 'blank': 'True', 'db_index': 'True'}),
            'mimetype': ('django.db.models.fields.CharField', [], {'max_length': '40', 'default': "''", 'blank': 'True', 'db_index': 'True'}),
            'modification': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'db_index': 'True', 'auto_now': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'official_link': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'}),
            'repository': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.Repository']"}),
            'sha1': ('django.db.models.fields.CharField', [], {'max_length': '120', 'default': "''", 'blank': 'True', 'db_index': 'True'}),
            'sha256': ('django.db.models.fields.CharField', [], {'max_length': '120', 'default': "''", 'blank': 'True', 'db_index': 'True'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'}),
            'states': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['repository.ArchiveState']", 'db_index': 'True'}),
            'uncompressed_key': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "''", 'blank': 'True', 'db_index': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True', 'db_index': 'True'}),
            'version': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.Version']"})
        },
        'repository.repository': {
            'Meta': {'object_name': 'Repository'},
            'admin_group': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'db_index': 'True', 'to': "orm['auth.Group']"}),
            'archive_type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'creation': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'db_index': 'True', 'auto_now_add': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'modification': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'db_index': 'True', 'auto_now': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'})
        },
        'repository.version': {
            'Meta': {'ordering': "('full_name',)", 'object_name': 'Version'},
            'archive': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.Archive']"}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'creation': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'db_index': 'True', 'auto_now_add': 'True'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True', 'db_index': 'True'}),
            'full_name_normalized': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'modification': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'db_index': 'True', 'auto_now': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'official_link': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['repository']