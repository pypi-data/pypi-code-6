# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Version'
        db.delete_table('repository_version')

        # Deleting model 'Archive'
        db.delete_table('repository_archive')


        # Renaming column for 'Element.archive' to match new field type.
        db.rename_column('repository_element', 'archive_id', 'archive')
        # Changing field 'Element.archive'
        db.alter_column('repository_element', 'archive', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Renaming column for 'Element.version' to match new field type.
        db.rename_column('repository_element', 'version_id', 'version')
        # Changing field 'Element.version'
        db.alter_column('repository_element', 'version', self.gf('django.db.models.fields.CharField')(max_length=255))

    def backwards(self, orm):
        # Adding model 'Version'
        db.create_table('repository_version', (
            ('creation', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('official_link', self.gf('django.db.models.fields.URLField')(blank=True, max_length=255)),
            ('full_name', self.gf('django.db.models.fields.CharField')(db_index=True, blank=True, max_length=255)),
            ('full_name_normalized', self.gf('django.db.models.fields.CharField')(db_index=True, blank=True, max_length=255)),
            ('archive', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.Archive'])),
            ('short_description', self.gf('django.db.models.fields.CharField')(blank=True, max_length=500)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(null=True, blank=True, to=orm['auth.User'])),
            ('modification', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, db_index=True, blank=True)),
            ('long_description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100)),
            ('name', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=100)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('repository', ['Version'])

        # Adding model 'Archive'
        db.create_table('repository_archive', (
            ('creation', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('modification', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, db_index=True, blank=True)),
            ('long_description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100)),
            ('name', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=100)),
            ('short_description', self.gf('django.db.models.fields.CharField')(blank=True, max_length=500)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('official_link', self.gf('django.db.models.fields.URLField')(blank=True, max_length=255)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(null=True, blank=True, to=orm['auth.User'])),
        ))
        db.send_create_signal('repository', ['Archive'])


        # Renaming column for 'Element.archive' to match new field type.
        db.rename_column('repository_element', 'archive', 'archive_id')
        # Changing field 'Element.archive'
        db.alter_column('repository_element', 'archive_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.Archive']))

        # Renaming column for 'Element.version' to match new field type.
        db.rename_column('repository_element', 'version', 'version_id')
        # Changing field 'Element.version'
        db.alter_column('repository_element', 'version_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.Version']))

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False'})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'blank': 'True', 'to': "orm['auth.Group']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'object_name': 'ContentType', 'db_table': "'django_content_type'", 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'repository.archivestate': {
            'Meta': {'object_name': 'ArchiveState'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['auth.User']", 'blank': 'True'}),
            'creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modification': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100'}),
            'repository': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.Repository']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'})
        },
        'repository.element': {
            'Meta': {'object_name': 'Element'},
            'archive': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'default': "''", 'max_length': '255'}),
            'archive_file': ('django.db.models.fields.files.FileField', [], {'null': 'True', 'blank': 'True', 'default': "''", 'max_length': '100'}),
            'archive_key': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'default': "''", 'max_length': '255'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['auth.User']", 'blank': 'True'}),
            'creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'extension': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'default': "''", 'max_length': '20'}),
            'extra_data': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': "''"}),
            'filename': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'default': "''", 'max_length': '255'}),
            'filesize': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True', 'default': '0'}),
            'full_name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '255'}),
            'full_name_normalized': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'md5': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'default': "''", 'max_length': '120'}),
            'mimetype': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'default': "''", 'max_length': '40'}),
            'modification': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100'}),
            'official_link': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '255'}),
            'repository': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.Repository']"}),
            'sha1': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'default': "''", 'max_length': '120'}),
            'sha256': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'default': "''", 'max_length': '120'}),
            'short_description': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '500'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'}),
            'states': ('django.db.models.fields.related.ManyToManyField', [], {'db_index': 'True', 'to': "orm['repository.ArchiveState']", 'symmetrical': 'False'}),
            'uncompressed_key': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'default': "''", 'max_length': '255'}),
            'uuid': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '40'}),
            'version': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'default': "''", 'max_length': '255'})
        },
        'repository.repository': {
            'Meta': {'object_name': 'Repository'},
            'admin_group': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'db_index': 'True', 'to': "orm['auth.Group']", 'symmetrical': 'False'}),
            'archive_type': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['auth.User']", 'blank': 'True'}),
            'creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'db_index': 'True', 'default': 'True'}),
            'modification': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['repository']