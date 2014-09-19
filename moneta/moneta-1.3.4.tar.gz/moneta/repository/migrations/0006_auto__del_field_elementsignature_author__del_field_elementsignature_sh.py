# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'ElementSignature.author'
        db.delete_column('repository_elementsignature', 'author_id')

        # Deleting field 'ElementSignature.sha256'
        db.delete_column('repository_elementsignature', 'sha256')

        # Adding field 'ElementSignature.element'
        db.add_column('repository_elementsignature', 'element',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.Element'], default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'ElementSignature.author'
        db.add_column('repository_elementsignature', 'author',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], blank=True, null=True),
                      keep_default=False)

        # Adding field 'ElementSignature.sha256'
        db.add_column('repository_elementsignature', 'sha256',
                      self.gf('django.db.models.fields.CharField')(max_length=40, db_index=True, default=None),
                      keep_default=False)

        # Deleting field 'ElementSignature.element'
        db.delete_column('repository_elementsignature', 'element_id')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True', 'symmetrical': 'False'})
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
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True', 'related_name': "'user_set'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True', 'related_name': "'user_set'"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)", 'object_name': 'ContentType'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'repository.archivestate': {
            'Meta': {'object_name': 'ArchiveState'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modification': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100'}),
            'repository': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.Repository']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'})
        },
        'repository.element': {
            'Meta': {'object_name': 'Element'},
            'archive': ('django.db.models.fields.CharField', [], {'blank': 'True', 'db_index': 'True', 'max_length': '255', 'default': "''"}),
            'archive_file': ('django.db.models.fields.files.FileField', [], {'null': 'True', 'blank': 'True', 'max_length': '100', 'default': "''"}),
            'archive_key': ('django.db.models.fields.CharField', [], {'blank': 'True', 'db_index': 'True', 'max_length': '255', 'default': "''"}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True', 'db_index': 'True'}),
            'extension': ('django.db.models.fields.CharField', [], {'blank': 'True', 'db_index': 'True', 'max_length': '20', 'default': "''"}),
            'extra_data': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': "''"}),
            'filename': ('django.db.models.fields.CharField', [], {'blank': 'True', 'db_index': 'True', 'max_length': '255', 'default': "''"}),
            'filesize': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'default': '0', 'db_index': 'True'}),
            'full_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'db_index': 'True', 'max_length': '255'}),
            'full_name_normalized': ('django.db.models.fields.CharField', [], {'blank': 'True', 'db_index': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'md5': ('django.db.models.fields.CharField', [], {'blank': 'True', 'db_index': 'True', 'max_length': '120', 'default': "''"}),
            'mimetype': ('django.db.models.fields.CharField', [], {'blank': 'True', 'db_index': 'True', 'max_length': '40', 'default': "''"}),
            'modification': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100'}),
            'official_link': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '255'}),
            'repository': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.Repository']"}),
            'sha1': ('django.db.models.fields.CharField', [], {'blank': 'True', 'db_index': 'True', 'max_length': '120', 'default': "''"}),
            'sha256': ('django.db.models.fields.CharField', [], {'blank': 'True', 'db_index': 'True', 'max_length': '120', 'default': "''"}),
            'short_description': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '500'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'}),
            'states': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['repository.ArchiveState']", 'symmetrical': 'False', 'db_index': 'True'}),
            'uncompressed_key': ('django.db.models.fields.CharField', [], {'blank': 'True', 'db_index': 'True', 'max_length': '255', 'default': "''"}),
            'uuid': ('django.db.models.fields.CharField', [], {'blank': 'True', 'db_index': 'True', 'max_length': '40'}),
            'version': ('django.db.models.fields.CharField', [], {'blank': 'True', 'db_index': 'True', 'max_length': '255', 'default': "''"})
        },
        'repository.elementsignature': {
            'Meta': {'object_name': 'ElementSignature'},
            'creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True', 'db_index': 'True'}),
            'element': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.Element']", 'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '10'})
        },
        'repository.repository': {
            'Meta': {'object_name': 'Repository'},
            'admin_group': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True', 'related_name': "'repository_admin'", 'db_index': 'True'}),
            'archive_type': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_private': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'modification': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100'}),
            'on_index': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'reader_group': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True', 'related_name': "'repository_reader'", 'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['repository']