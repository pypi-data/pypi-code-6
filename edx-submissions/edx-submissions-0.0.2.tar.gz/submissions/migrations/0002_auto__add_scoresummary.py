# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ScoreSummary'
        db.create_table('submissions_scoresummary', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('student_item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['submissions.StudentItem'], unique=True)),
            ('highest', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['submissions.Score'])),
            ('latest', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['submissions.Score'])),
        ))
        db.send_create_signal('submissions', ['ScoreSummary'])


    def backwards(self, orm):
        # Deleting model 'ScoreSummary'
        db.delete_table('submissions_scoresummary')


    models = {
        'submissions.score': {
            'Meta': {'object_name': 'Score'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'points_earned': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'points_possible': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'student_item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['submissions.StudentItem']"}),
            'submission': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['submissions.Submission']", 'null': 'True'})
        },
        'submissions.scoresummary': {
            'Meta': {'object_name': 'ScoreSummary'},
            'highest': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['submissions.Score']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latest': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['submissions.Score']"}),
            'student_item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['submissions.StudentItem']", 'unique': 'True'})
        },
        'submissions.studentitem': {
            'Meta': {'unique_together': "(('course_id', 'student_id', 'item_id'),)", 'object_name': 'StudentItem'},
            'course_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'item_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'student_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        'submissions.submission': {
            'Meta': {'ordering': "['-submitted_at', '-id']", 'object_name': 'Submission'},
            'answer': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'attempt_number': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'student_item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['submissions.StudentItem']"}),
            'submitted_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'db_index': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '36', 'blank': 'True'})
        }
    }

    complete_apps = ['submissions']