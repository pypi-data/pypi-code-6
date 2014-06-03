# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'UserTag', fields ['tag', 'idUser', 'idResource']
        db.delete_unique(u'catalogue_usertag', ['tag_id', 'idUser_id', 'idResource_id'])

        # Removing unique constraint on 'UserVote', fields ['idUser', 'idResource']
        db.delete_unique(u'catalogue_uservote', ['idUser_id', 'idResource_id'])

        # Deleting model 'Tag'
        db.delete_table(u'catalogue_tag')

        # Deleting model 'UserVote'
        db.delete_table(u'catalogue_uservote')

        # Deleting model 'Category'
        db.delete_table(u'catalogue_category')

        # Removing M2M table for field organizations on 'Category'
        db.delete_table(db.shorten_name(u'catalogue_category_organizations'))

        # Removing M2M table for field tags on 'Category'
        db.delete_table(db.shorten_name(u'catalogue_category_tags'))

        # Deleting model 'UserTag'
        db.delete_table(u'catalogue_usertag')


    def backwards(self, orm):
        # Adding model 'Tag'
        db.create_table(u'catalogue_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20, unique=True)),
        ))
        db.send_create_signal(u'catalogue', ['Tag'])

        # Adding model 'UserVote'
        db.create_table(u'catalogue_uservote', (
            ('idUser', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('vote', self.gf('django.db.models.fields.SmallIntegerField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('idResource', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.CatalogueResource'])),
        ))
        db.send_create_signal(u'catalogue', ['UserVote'])

        # Adding unique constraint on 'UserVote', fields ['idUser', 'idResource']
        db.create_unique(u'catalogue_uservote', ['idUser_id', 'idResource_id'])

        # Adding model 'Category'
        db.create_table(u'catalogue_category', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, unique=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.Category'], null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'catalogue', ['Category'])

        # Adding M2M table for field organizations on 'Category'
        m2m_table_name = db.shorten_name(u'catalogue_category_organizations')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('category', models.ForeignKey(orm[u'catalogue.category'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['category_id', 'group_id'])

        # Adding M2M table for field tags on 'Category'
        m2m_table_name = db.shorten_name(u'catalogue_category_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('category', models.ForeignKey(orm[u'catalogue.category'], null=False)),
            ('tag', models.ForeignKey(orm[u'catalogue.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['category_id', 'tag_id'])

        # Adding model 'UserTag'
        db.create_table(u'catalogue_usertag', (
            ('idResource', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.CatalogueResource'])),
            ('weight', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('criteria', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('idUser', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.Tag'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
        ))
        db.send_create_signal(u'catalogue', ['UserTag'])

        # Adding unique constraint on 'UserTag', fields ['tag', 'idUser', 'idResource']
        db.create_unique(u'catalogue_usertag', ['tag_id', 'idUser_id', 'idResource_id'])


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'catalogue.catalogueresource': {
            'Meta': {'unique_together': "((u'short_name', u'vendor', u'version'),)", 'object_name': 'CatalogueResource'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'uploaded_resources'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'fromWGT': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'local_resources'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_uri': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'iphone_image_uri': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'json_description': ('django.db.models.fields.TextField', [], {}),
            'license': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'mail': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'popularity': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '2', 'decimal_places': '1'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'template_uri': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'type': ('django.db.models.fields.SmallIntegerField', [], {}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'local_resources'", 'blank': 'True', 'to': u"orm['auth.User']"}),
            'vendor': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'wiki_page_uri': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'catalogue.widgetwiring': {
            'Meta': {'object_name': 'WidgetWiring'},
            'friendcode': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idResource': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalogue.CatalogueResource']"}),
            'wiring': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['catalogue']