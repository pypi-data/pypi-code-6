# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import DataMigration
from django.db import connection


class Migration(DataMigration):

    old_table = 'cmsplugin_subscriptionplugin'
    new_table = 'aldryn_mailchimp_subscriptionplugin'

    def forwards(self, orm):
        table_names = connection.introspection.table_names()

        if self.old_table in table_names:
            if not self.new_table in table_names:
                db.rename_table(self.old_table, self.new_table)
            else:
                db.drop_table(self.old_table)
                # Adding field 'SubscriptionPlugin.assign_language'
                db.add_column(u'aldryn_mailchimp_subscriptionplugin', 'assign_language',
                              self.gf('django.db.models.fields.BooleanField')(default=True),
                              keep_default=False)

    def backwards(self, orm):
        # Deleting field 'SubscriptionPlugin.assign_language'
        db.delete_column(u'aldryn_mailchimp_subscriptionplugin', 'assign_language')

    models = {
        u'aldryn_mailchimp.subscriptionplugin': {
            'Meta': {'object_name': 'SubscriptionPlugin', '_ormbases': ['cms.CMSPlugin']},
            'assign_language': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'list_id': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
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
        }
    }

    complete_apps = ['aldryn_mailchimp']
    symmetrical = True
