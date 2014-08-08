# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PageGuide'
        db.create_table('pageguide_pageguide', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('target_url', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('pageguide', ['PageGuide'])

        # Adding model 'PageGuideStep'
        db.create_table('pageguide_pageguidestep', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pageguide', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pageguide.PageGuide'])),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('css_selector', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('html_content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('pageguide', ['PageGuideStep'])


    def backwards(self, orm):
        # Deleting model 'PageGuide'
        db.delete_table('pageguide_pageguide')

        # Deleting model 'PageGuideStep'
        db.delete_table('pageguide_pageguidestep')

    models = {
        'pageguide.pageguide': {
            'Meta': {'object_name': 'PageGuide'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'target_url': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'pageguide.pageguidestep': {
            'Meta': {'object_name': 'PageGuideStep'},
            'css_selector': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'html_content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pageguide': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pageguide.PageGuide']"})
        }
    }

    complete_apps = ['pageguide']
