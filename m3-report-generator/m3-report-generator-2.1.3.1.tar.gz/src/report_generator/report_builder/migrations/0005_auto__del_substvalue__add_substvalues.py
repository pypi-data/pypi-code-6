# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'SubstValue'
        db.delete_table('report_builder_substvalue')

        # Adding model 'SubstValues'
        db.create_table('report_builder_substvalues', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('report', self.gf('django.db.models.fields.related.OneToOneField')(related_name='subst_values', unique=True, to=orm['report_builder.Report'])),
            ('json_subst_values', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('report_builder', ['SubstValues'])


    def backwards(self, orm):
        
        # Adding model 'SubstValue'
        db.create_table('report_builder_substvalue', (
            ('report', self.gf('django.db.models.fields.related.ForeignKey')(related_name='subst_values', to=orm['report_builder.Report'])),
            ('json_subst_values', self.gf('django.db.models.fields.TextField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('report_builder', ['SubstValue'])

        # Deleting model 'SubstValues'
        db.delete_table('report_builder_substvalues')


    models = {
        'report_builder.formfield': {
            'Meta': {'object_name': 'FormField'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'json_fields': ('django.db.models.fields.TextField', [], {}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'form_fields'", 'to': "orm['report_builder.Report']"})
        },
        'report_builder.report': {
            'Meta': {'object_name': 'Report'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'report_key': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'report_builder.reportquery': {
            'Meta': {'object_name': 'ReportQuery'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'query_id': ('django.db.models.fields.IntegerField', [], {}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'queries'", 'to': "orm['report_builder.Report']"})
        },
        'report_builder.substvalues': {
            'Meta': {'object_name': 'SubstValues'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'json_subst_values': ('django.db.models.fields.TextField', [], {}),
            'report': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'subst_values'", 'unique': 'True', 'to': "orm['report_builder.Report']"})
        },
        'report_builder.template': {
            'Meta': {'object_name': 'Template'},
            'document_type': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'file_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'json_sections': ('django.db.models.fields.TextField', [], {}),
            'report': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'template'", 'unique': 'True', 'to': "orm['report_builder.Report']"})
        }
    }

    complete_apps = ['report_builder']
