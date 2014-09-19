# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Repository'
        db.create_table('repository_repository', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100)),
            ('creation', self.gf('django.db.models.fields.DateTimeField')(db_index=True, blank=True, auto_now_add=True)),
            ('modification', self.gf('django.db.models.fields.DateTimeField')(db_index=True, auto_now=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('archive_type', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(db_index=True, default=True)),
        ))
        db.send_create_signal('repository', ['Repository'])

        # Adding M2M table for field admin_group on 'Repository'
        m2m_table_name = db.shorten_name('repository_repository_admin_group')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('repository', models.ForeignKey(orm['repository.repository'], null=False)),
            ('group', models.ForeignKey(orm['auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['repository_id', 'group_id'])

        # Adding model 'ArchiveState'
        db.create_table('repository_archivestate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100)),
            ('creation', self.gf('django.db.models.fields.DateTimeField')(db_index=True, blank=True, auto_now_add=True)),
            ('modification', self.gf('django.db.models.fields.DateTimeField')(db_index=True, auto_now=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('repository', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.Repository'])),
        ))
        db.send_create_signal('repository', ['ArchiveState'])

        # Adding model 'Archive'
        db.create_table('repository_archive', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100)),
            ('creation', self.gf('django.db.models.fields.DateTimeField')(db_index=True, blank=True, auto_now_add=True)),
            ('modification', self.gf('django.db.models.fields.DateTimeField')(db_index=True, auto_now=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('official_link', self.gf('django.db.models.fields.URLField')(max_length=255, blank=True)),
            ('short_description', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('long_description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('repository', ['Archive'])

        # Adding model 'Version'
        db.create_table('repository_version', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100)),
            ('creation', self.gf('django.db.models.fields.DateTimeField')(db_index=True, blank=True, auto_now_add=True)),
            ('modification', self.gf('django.db.models.fields.DateTimeField')(db_index=True, auto_now=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('official_link', self.gf('django.db.models.fields.URLField')(max_length=255, blank=True)),
            ('short_description', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('long_description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True, blank=True)),
            ('full_name_normalized', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True, blank=True)),
            ('archive', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.Archive'])),
        ))
        db.send_create_signal('repository', ['Version'])

        # Adding model 'Element'
        db.create_table('repository_element', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100)),
            ('creation', self.gf('django.db.models.fields.DateTimeField')(db_index=True, blank=True, auto_now_add=True)),
            ('modification', self.gf('django.db.models.fields.DateTimeField')(db_index=True, auto_now=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('official_link', self.gf('django.db.models.fields.URLField')(max_length=255, blank=True)),
            ('short_description', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('long_description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('repository', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.Repository'])),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True, blank=True)),
            ('full_name_normalized', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True, blank=True)),
            ('archive', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, to=orm['repository.Archive'])),
            ('version', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.Version'])),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True, default='', blank=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=40, db_index=True, blank=True)),
            ('md5', self.gf('django.db.models.fields.CharField')(max_length=120, db_index=True, default='', blank=True)),
            ('sha1', self.gf('django.db.models.fields.CharField')(max_length=120, db_index=True, default='', blank=True)),
            ('sha256', self.gf('django.db.models.fields.CharField')(max_length=120, db_index=True, default='', blank=True)),
            ('filesize', self.gf('django.db.models.fields.IntegerField')(db_index=True, default=0, blank=True)),
            ('extension', self.gf('django.db.models.fields.CharField')(max_length=20, db_index=True, default='', blank=True)),
            ('mimetype', self.gf('django.db.models.fields.CharField')(max_length=40, db_index=True, default='', blank=True)),
            ('archive_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True, default='', null=True)),
            ('archive_key', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True, default='', blank=True)),
            ('uncompressed_key', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True, default='', blank=True)),
            ('extra_data', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
        ))
        db.send_create_signal('repository', ['Element'])

        # Adding M2M table for field states on 'Element'
        m2m_table_name = db.shorten_name('repository_element_states')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('element', models.ForeignKey(orm['repository.element'], null=False)),
            ('archivestate', models.ForeignKey(orm['repository.archivestate'], null=False))
        ))
        db.create_unique(m2m_table_name, ['element_id', 'archivestate_id'])


    def backwards(self, orm):
        # Deleting model 'Repository'
        db.delete_table('repository_repository')

        # Removing M2M table for field admin_group on 'Repository'
        db.delete_table(db.shorten_name('repository_repository_admin_group'))

        # Deleting model 'ArchiveState'
        db.delete_table('repository_archivestate')

        # Deleting model 'Archive'
        db.delete_table('repository_archive')

        # Deleting model 'Version'
        db.delete_table('repository_version')

        # Deleting model 'Element'
        db.delete_table('repository_element')

        # Removing M2M table for field states on 'Element'
        db.delete_table(db.shorten_name('repository_element_states'))


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'related_name': "'user_set'", 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'related_name': "'user_set'", 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'repository.archive': {
            'Meta': {'object_name': 'Archive'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'creation': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True', 'auto_now_add': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'modification': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'official_link': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'})
        },
        'repository.archivestate': {
            'Meta': {'object_name': 'ArchiveState'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'creation': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True', 'auto_now_add': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modification': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'repository': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.Repository']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'})
        },
        'repository.element': {
            'Meta': {'object_name': 'Element'},
            'archive': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['repository.Archive']"}),
            'archive_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True', 'default': "''", 'null': 'True'}),
            'archive_key': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True', 'default': "''", 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'creation': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True', 'auto_now_add': 'True'}),
            'extension': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True', 'default': "''", 'blank': 'True'}),
            'extra_data': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True', 'default': "''", 'blank': 'True'}),
            'filesize': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'default': '0', 'blank': 'True'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True', 'blank': 'True'}),
            'full_name_normalized': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'md5': ('django.db.models.fields.CharField', [], {'max_length': '120', 'db_index': 'True', 'default': "''", 'blank': 'True'}),
            'mimetype': ('django.db.models.fields.CharField', [], {'max_length': '40', 'db_index': 'True', 'default': "''", 'blank': 'True'}),
            'modification': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'official_link': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'}),
            'repository': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.Repository']"}),
            'sha1': ('django.db.models.fields.CharField', [], {'max_length': '120', 'db_index': 'True', 'default': "''", 'blank': 'True'}),
            'sha256': ('django.db.models.fields.CharField', [], {'max_length': '120', 'db_index': 'True', 'default': "''", 'blank': 'True'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'}),
            'states': ('django.db.models.fields.related.ManyToManyField', [], {'db_index': 'True', 'symmetrical': 'False', 'to': "orm['repository.ArchiveState']"}),
            'uncompressed_key': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True', 'default': "''", 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '40', 'db_index': 'True', 'blank': 'True'}),
            'version': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.Version']"})
        },
        'repository.repository': {
            'Meta': {'object_name': 'Repository'},
            'admin_group': ('django.db.models.fields.related.ManyToManyField', [], {'db_index': 'True', 'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Group']"}),
            'archive_type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'creation': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True', 'auto_now_add': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'db_index': 'True', 'default': 'True'}),
            'modification': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'})
        },
        'repository.version': {
            'Meta': {'object_name': 'Version', 'ordering': "('full_name',)"},
            'archive': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.Archive']"}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'creation': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True', 'auto_now_add': 'True'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True', 'blank': 'True'}),
            'full_name_normalized': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'modification': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'official_link': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['repository']