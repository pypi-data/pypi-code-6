# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'TabUi.title_color'
        db.add_column(u'cmsplugin_tab_ui_tabui', 'title_color',
                      self.gf('paintstore.fields.ColorPickerField')(max_length=7, null=True, blank=True),
                      keep_default=False)

        # Adding field 'TabUi.background_color'
        db.add_column(u'cmsplugin_tab_ui_tabui', 'background_color',
                      self.gf('paintstore.fields.ColorPickerField')(max_length=7, null=True, blank=True),
                      keep_default=False)

        # Adding field 'TabUiList.align'
        db.add_column(u'cmsplugin_tab_ui_tabuilist', 'align',
                      self.gf('django.db.models.fields.CharField')(default='h', max_length=1),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'TabUi.title_color'
        db.delete_column(u'cmsplugin_tab_ui_tabui', 'title_color')

        # Deleting field 'TabUi.background_color'
        db.delete_column(u'cmsplugin_tab_ui_tabui', 'background_color')

        # Deleting field 'TabUiList.align'
        db.delete_column(u'cmsplugin_tab_ui_tabuilist', 'align')


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
        u'cmsplugin_tab_ui.tabui': {
            'Meta': {'object_name': 'TabUi', '_ormbases': ['cms.CMSPlugin']},
            'background_color': ('paintstore.fields.ColorPickerField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'}),
            u'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title_color': ('paintstore.fields.ColorPickerField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'})
        },
        u'cmsplugin_tab_ui.tabuilist': {
            'Meta': {'object_name': 'TabUiList', '_ormbases': ['cms.CMSPlugin']},
            'align': ('django.db.models.fields.CharField', [], {'default': "'h'", 'max_length': '1'}),
            u'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'custom_classes': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['cmsplugin_tab_ui']