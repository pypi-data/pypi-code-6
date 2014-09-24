# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ReportQuery'
        db.create_table('report_builder_reportquery', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('report', self.gf('django.db.models.fields.related.ForeignKey')(related_name='queries', to=orm['report_builder.Report'])),
            ('query_id', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('report_builder', ['ReportQuery'])

        # Adding model 'Template'
        db.create_table('report_builder_template', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('document_type', self.gf('django.db.models.fields.IntegerField')(default=-1)),
            ('json_sections', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('report_builder', ['Template'])

        # Adding model 'Report'
        db.create_table('report_builder_report', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('report_key', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('report_builder', ['Report'])


    def backwards(self, orm):
        
        # Deleting model 'ReportQuery'
        db.delete_table('report_builder_reportquery')

        # Deleting model 'Template'
        db.delete_table('report_builder_template')

        # Deleting model 'Report'
        db.delete_table('report_builder_report')


    models = {
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
        'report_builder.template': {
            'Meta': {'object_name': 'Template'},
            'document_type': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'file_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'json_sections': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['report_builder']
