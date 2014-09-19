# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Repository.on_index'
        db.add_column('repository_repository', 'on_index',
                      self.gf('django.db.models.fields.BooleanField')(db_index=True, default=True),
                      keep_default=False)

        # Adding field 'Repository.is_private'
        db.add_column('repository_repository', 'is_private',
                      self.gf('django.db.models.fields.BooleanField')(db_index=True, default=False),
                      keep_default=False)

        # Adding M2M table for field reader_group on 'Repository'
        m2m_table_name = db.shorten_name('repository_repository_reader_group')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('repository', models.ForeignKey(orm['repository.repository'], null=False)),
            ('group', models.ForeignKey(orm['auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['repository_id', 'group_id'])


    def backwards(self, orm):
        # Deleting field 'Repository.on_index'
        db.delete_column('repository_repository', 'on_index')

        # Deleting field 'Repository.is_private'
        db.delete_column('repository_repository', 'is_private')

        # Removing M2M table for field reader_group on 'Repository'
        db.delete_table(db.shorten_name('repository_repository_reader_group'))


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
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
            'Meta': {'db_table': "'django_content_type'", 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'repository.archivestate': {
            'Meta': {'object_name': 'ArchiveState'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modification': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100'}),
            'repository': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.Repository']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'})
        },
        'repository.element': {
            'Meta': {'object_name': 'Element'},
            'archive': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '255', 'default': "''"}),
            'archive_file': ('django.db.models.fields.files.FileField', [], {'null': 'True', 'blank': 'True', 'max_length': '100', 'default': "''"}),
            'archive_key': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '255', 'default': "''"}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
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
            'modification': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100'}),
            'official_link': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '255'}),
            'repository': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.Repository']"}),
            'sha1': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '120', 'default': "''"}),
            'sha256': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '120', 'default': "''"}),
            'short_description': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '500'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'}),
            'states': ('django.db.models.fields.related.ManyToManyField', [], {'db_index': 'True', 'to': "orm['repository.ArchiveState']", 'symmetrical': 'False'}),
            'uncompressed_key': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '255', 'default': "''"}),
            'uuid': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '40'}),
            'version': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '255', 'default': "''"})
        },
        'repository.repository': {
            'Meta': {'object_name': 'Repository'},
            'admin_group': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'repository_admin'", 'blank': 'True', 'db_index': 'True', 'to': "orm['auth.Group']", 'symmetrical': 'False'}),
            'archive_type': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_private': ('django.db.models.fields.BooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'db_index': 'True', 'default': 'True'}),
            'modification': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100'}),
            'on_index': ('django.db.models.fields.BooleanField', [], {'db_index': 'True', 'default': 'True'}),
            'reader_group': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'repository_reader'", 'blank': 'True', 'db_index': 'True', 'to': "orm['auth.Group']", 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['repository']