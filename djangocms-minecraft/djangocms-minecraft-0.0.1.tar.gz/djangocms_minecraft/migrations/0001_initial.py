# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ServerStatus'
        db.create_table(u'djangocms_minecraft_serverstatus', (
            (u'cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('mchost', self.gf('django.db.models.fields.IPAddressField')(default='127.0.0.1', max_length=15)),
            ('mcport', self.gf('django.db.models.fields.PositiveIntegerField')(default=25565)),
        ))
        db.send_create_signal(u'djangocms_minecraft', ['ServerStatus'])

        # Adding model 'ServerQuery'
        db.create_table(u'djangocms_minecraft_serverquery', (
            (u'cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('mchost', self.gf('django.db.models.fields.IPAddressField')(default='127.0.0.1', max_length=15)),
            ('mcport', self.gf('django.db.models.fields.PositiveIntegerField')(default=25565)),
            ('map_url', self.gf('django.db.models.fields.CharField')(default='http://minecraft.ottercloud.net:8123/?mapname=surface&zoom=8', max_length=80)),
        ))
        db.send_create_signal(u'djangocms_minecraft', ['ServerQuery'])

        # Adding model 'PluginsList'
        db.create_table(u'djangocms_minecraft_pluginslist', (
            (u'cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('mchost', self.gf('django.db.models.fields.IPAddressField')(default='127.0.0.1', max_length=15)),
            ('mcport', self.gf('django.db.models.fields.PositiveIntegerField')(default=25565)),
        ))
        db.send_create_signal(u'djangocms_minecraft', ['PluginsList'])


    def backwards(self, orm):
        # Deleting model 'ServerStatus'
        db.delete_table(u'djangocms_minecraft_serverstatus')

        # Deleting model 'ServerQuery'
        db.delete_table(u'djangocms_minecraft_serverquery')

        # Deleting model 'PluginsList'
        db.delete_table(u'djangocms_minecraft_pluginslist')


    models = {
        'cms.cmsplugin': {
            'Meta': {'object_name': 'CMSPlugin'},
            'changed_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.CMSPlugin']", 'null': 'True', 'blank': 'True'}),
            'placeholder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            'plugin_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'cms.placeholder': {
            'Meta': {'object_name': 'Placeholder'},
            'default_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        },
        u'djangocms_minecraft.pluginslist': {
            'Meta': {'object_name': 'PluginsList', '_ormbases': ['cms.CMSPlugin']},
            u'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'mchost': ('django.db.models.fields.IPAddressField', [], {'default': "'127.0.0.1'", 'max_length': '15'}),
            'mcport': ('django.db.models.fields.PositiveIntegerField', [], {'default': '25565'})
        },
        u'djangocms_minecraft.serverquery': {
            'Meta': {'object_name': 'ServerQuery', '_ormbases': ['cms.CMSPlugin']},
            u'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'map_url': ('django.db.models.fields.CharField', [], {'default': "'http://minecraft.ottercloud.net:8123/?mapname=surface&zoom=8'", 'max_length': '80'}),
            'mchost': ('django.db.models.fields.IPAddressField', [], {'default': "'127.0.0.1'", 'max_length': '15'}),
            'mcport': ('django.db.models.fields.PositiveIntegerField', [], {'default': '25565'})
        },
        u'djangocms_minecraft.serverstatus': {
            'Meta': {'object_name': 'ServerStatus', '_ormbases': ['cms.CMSPlugin']},
            u'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'mchost': ('django.db.models.fields.IPAddressField', [], {'default': "'127.0.0.1'", 'max_length': '15'}),
            'mcport': ('django.db.models.fields.PositiveIntegerField', [], {'default': '25565'})
        }
    }

    complete_apps = ['djangocms_minecraft']