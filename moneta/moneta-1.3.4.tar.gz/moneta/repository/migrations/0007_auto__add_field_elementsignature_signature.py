# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ElementSignature.signature'
        db.add_column('repository_elementsignature', 'signature',
                      self.gf('django.db.models.fields.TextField')(blank=True, default=''),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ElementSignature.signature'
        db.delete_column('repository_elementsignature', 'signature')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Group']", 'related_name': "'user_set'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
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
        'repository.archivestate': {
            'Meta': {'object_name': 'ArchiveState'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['auth.User']", 'null': 'True'}),
            'creation': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True', 'auto_now_add': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modification': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True', 'auto_now': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100'}),
            'repository': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.Repository']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'})
        },
        'repository.element': {
            'Meta': {'object_name': 'Element'},
            'archive': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '255', 'default': "''"}),
            'archive_file': ('django.db.models.fields.files.FileField', [], {'blank': 'True', 'max_length': '100', 'null': 'True', 'default': "''"}),
            'archive_key': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '255', 'default': "''"}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['auth.User']", 'null': 'True'}),
            'creation': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True', 'auto_now_add': 'True'}),
            'extension': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '20', 'default': "''"}),
            'extra_data': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': "''"}),
            'filename': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '255', 'default': "''"}),
            'filesize': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True', 'default': '0'}),
            'full_name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '255'}),
            'full_name_normalized': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'md5': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '120', 'default': "''"}),
            'mimetype': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '40', 'default': "''"}),
            'modification': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True', 'auto_now': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100'}),
            'official_link': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '255'}),
            'repository': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.Repository']"}),
            'sha1': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '120', 'default': "''"}),
            'sha256': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '120', 'default': "''"}),
            'short_description': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '500'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'}),
            'states': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['repository.ArchiveState']", 'db_index': 'True', 'symmetrical': 'False'}),
            'uncompressed_key': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '255', 'default': "''"}),
            'uuid': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '40'}),
            'version': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '255', 'default': "''"})
        },
        'repository.elementsignature': {
            'Meta': {'object_name': 'ElementSignature'},
            'creation': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True', 'auto_now_add': 'True'}),
            'element': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.Element']", 'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '10'}),
            'signature': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': "''"})
        },
        'repository.repository': {
            'Meta': {'object_name': 'Repository'},
            'admin_group': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'db_index': 'True', 'to': "orm['auth.Group']", 'related_name': "'repository_admin'", 'blank': 'True'}),
            'archive_type': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['auth.User']", 'null': 'True'}),
            'creation': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True', 'auto_now_add': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_private': ('django.db.models.fields.BooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'db_index': 'True', 'default': 'True'}),
            'modification': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True', 'auto_now': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100'}),
            'on_index': ('django.db.models.fields.BooleanField', [], {'db_index': 'True', 'default': 'True'}),
            'reader_group': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'db_index': 'True', 'to': "orm['auth.Group']", 'related_name': "'repository_reader'", 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['repository']