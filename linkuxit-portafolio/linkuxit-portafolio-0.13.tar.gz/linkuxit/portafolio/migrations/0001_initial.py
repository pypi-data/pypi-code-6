# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TeamMember'
        db.create_table(u'portafolio_teammember', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('photo', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['filer.Image'], null=True, blank=True)),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('position', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('position_es', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('position_en', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('strong_skills', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('strong_skills_es', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('strong_skills_en', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('summary', self.gf('djangocms_text_ckeditor.fields.HTMLField')()),
            ('summary_es', self.gf('djangocms_text_ckeditor.fields.HTMLField')(null=True, blank=True)),
            ('summary_en', self.gf('djangocms_text_ckeditor.fields.HTMLField')(null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'portafolio', ['TeamMember'])

        # Adding model 'SocialLink'
        db.create_table(u'portafolio_sociallink', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(related_name='social_links', to=orm['portafolio.TeamMember'])),
            ('website', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal(u'portafolio', ['SocialLink'])

        # Adding model 'Service'
        db.create_table(u'portafolio_service', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('title_es', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('title_en', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('html_class', self.gf('django.db.models.fields.CharField')(default='', max_length=30, blank=True)),
            ('description', self.gf('djangocms_text_ckeditor.fields.HTMLField')()),
            ('description_es', self.gf('djangocms_text_ckeditor.fields.HTMLField')(null=True, blank=True)),
            ('description_en', self.gf('djangocms_text_ckeditor.fields.HTMLField')(null=True, blank=True)),
            ('is_featured', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'portafolio', ['Service'])

        # Adding model 'Client'
        db.create_table(u'portafolio_client', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('description', self.gf('djangocms_text_ckeditor.fields.HTMLField')()),
            ('description_es', self.gf('djangocms_text_ckeditor.fields.HTMLField')(null=True, blank=True)),
            ('description_en', self.gf('djangocms_text_ckeditor.fields.HTMLField')(null=True, blank=True)),
            ('is_featured', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'portafolio', ['Client'])

        # Adding model 'Country'
        db.create_table(u'portafolio_country', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('name_es', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'portafolio', ['Country'])

        # Adding model 'Project'
        db.create_table(u'portafolio_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(related_name='projects', to=orm['portafolio.Country'])),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(related_name='projects', to=orm['portafolio.Client'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('description', self.gf('djangocms_text_ckeditor.fields.HTMLField')()),
            ('description_es', self.gf('djangocms_text_ckeditor.fields.HTMLField')(null=True, blank=True)),
            ('description_en', self.gf('djangocms_text_ckeditor.fields.HTMLField')(null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('is_featured', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('main_photo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['filer.Image'])),
        ))
        db.send_create_signal(u'portafolio', ['Project'])

        # Adding M2M table for field services on 'Project'
        m2m_table_name = db.shorten_name(u'portafolio_project_services')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm[u'portafolio.project'], null=False)),
            ('service', models.ForeignKey(orm[u'portafolio.service'], null=False))
        ))
        db.create_unique(m2m_table_name, ['project_id', 'service_id'])

        # Adding M2M table for field developers on 'Project'
        m2m_table_name = db.shorten_name(u'portafolio_project_developers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm[u'portafolio.project'], null=False)),
            ('teammember', models.ForeignKey(orm[u'portafolio.teammember'], null=False))
        ))
        db.create_unique(m2m_table_name, ['project_id', 'teammember_id'])

        # Adding model 'Image'
        db.create_table(u'portafolio_image', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['filer.Image'], null=True, blank=True)),
            ('description', self.gf('djangocms_text_ckeditor.fields.HTMLField')()),
            ('description_es', self.gf('djangocms_text_ckeditor.fields.HTMLField')(null=True, blank=True)),
            ('description_en', self.gf('djangocms_text_ckeditor.fields.HTMLField')(null=True, blank=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='images', to=orm['portafolio.Project'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'portafolio', ['Image'])

        # Adding model 'Team'
        db.create_table(u'portafolio_team', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('name_es', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(default='', max_length=50)),
            ('description', self.gf('djangocms_text_ckeditor.fields.HTMLField')(default='')),
            ('description_es', self.gf('djangocms_text_ckeditor.fields.HTMLField')(default='', null=True, blank=True)),
            ('description_en', self.gf('djangocms_text_ckeditor.fields.HTMLField')(default='', null=True, blank=True)),
        ))
        db.send_create_signal(u'portafolio', ['Team'])

        # Adding M2M table for field members on 'Team'
        m2m_table_name = db.shorten_name(u'portafolio_team_members')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('team', models.ForeignKey(orm[u'portafolio.team'], null=False)),
            ('teammember', models.ForeignKey(orm[u'portafolio.teammember'], null=False))
        ))
        db.create_unique(m2m_table_name, ['team_id', 'teammember_id'])

        # Adding model 'TeamPlugin'
        db.create_table(u'cmsplugin_teamplugin', (
            (u'cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='plugins', to=orm['portafolio.Team'])),
        ))
        db.send_create_signal(u'portafolio', ['TeamPlugin'])

        # Adding model 'PortfolioPlugin'
        db.create_table(u'cmsplugin_portfolioplugin', (
            (u'cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'portafolio', ['PortfolioPlugin'])


    def backwards(self, orm):
        # Deleting model 'TeamMember'
        db.delete_table(u'portafolio_teammember')

        # Deleting model 'SocialLink'
        db.delete_table(u'portafolio_sociallink')

        # Deleting model 'Service'
        db.delete_table(u'portafolio_service')

        # Deleting model 'Client'
        db.delete_table(u'portafolio_client')

        # Deleting model 'Country'
        db.delete_table(u'portafolio_country')

        # Deleting model 'Project'
        db.delete_table(u'portafolio_project')

        # Removing M2M table for field services on 'Project'
        db.delete_table(db.shorten_name(u'portafolio_project_services'))

        # Removing M2M table for field developers on 'Project'
        db.delete_table(db.shorten_name(u'portafolio_project_developers'))

        # Deleting model 'Image'
        db.delete_table(u'portafolio_image')

        # Deleting model 'Team'
        db.delete_table(u'portafolio_team')

        # Removing M2M table for field members on 'Team'
        db.delete_table(db.shorten_name(u'portafolio_team_members'))

        # Deleting model 'TeamPlugin'
        db.delete_table(u'cmsplugin_teamplugin')

        # Deleting model 'PortfolioPlugin'
        db.delete_table(u'cmsplugin_portfolioplugin')


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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'filer.file': {
            'Meta': {'object_name': 'File'},
            '_file_size': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'folder': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'all_files'", 'null': 'True', 'to': "orm['filer.Folder']"}),
            'has_all_mandatory_data': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'original_filename': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'owned_files'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'polymorphic_filer.file_set'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'sha1': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40', 'blank': 'True'}),
            'uploaded_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'filer.folder': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('parent', 'name'),)", 'object_name': 'Folder'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'filer_owned_folders'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['filer.Folder']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'uploaded_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'filer.image': {
            'Meta': {'object_name': 'Image', '_ormbases': ['filer.File']},
            '_height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            '_width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'date_taken': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'default_alt_text': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'default_caption': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'file_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['filer.File']", 'unique': 'True', 'primary_key': 'True'}),
            'must_always_publish_author_credit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'must_always_publish_copyright': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subject_location': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        u'portafolio.client': {
            'Meta': {'object_name': 'Client'},
            'description': ('djangocms_text_ckeditor.fields.HTMLField', [], {}),
            'description_en': ('djangocms_text_ckeditor.fields.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'description_es': ('djangocms_text_ckeditor.fields.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'portafolio.country': {
            'Meta': {'object_name': 'Country'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'portafolio.image': {
            'Meta': {'ordering': "('created_at',)", 'object_name': 'Image'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('djangocms_text_ckeditor.fields.HTMLField', [], {}),
            'description_en': ('djangocms_text_ckeditor.fields.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'description_es': ('djangocms_text_ckeditor.fields.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['filer.Image']", 'null': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': u"orm['portafolio.Project']"})
        },
        u'portafolio.portfolioplugin': {
            'Meta': {'object_name': 'PortfolioPlugin', 'db_table': "u'cmsplugin_portfolioplugin'", '_ormbases': ['cms.CMSPlugin']},
            u'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'portafolio.project': {
            'Meta': {'ordering': "('created_at',)", 'object_name': 'Project'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'projects'", 'to': u"orm['portafolio.Client']"}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'projects'", 'to': u"orm['portafolio.Country']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('djangocms_text_ckeditor.fields.HTMLField', [], {}),
            'description_en': ('djangocms_text_ckeditor.fields.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'description_es': ('djangocms_text_ckeditor.fields.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'developers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'projects'", 'symmetrical': 'False', 'to': u"orm['portafolio.TeamMember']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'main_photo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['filer.Image']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'services': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'projects'", 'symmetrical': 'False', 'to': u"orm['portafolio.Service']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'portafolio.service': {
            'Meta': {'ordering': "('order', 'created_at')", 'object_name': 'Service'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('djangocms_text_ckeditor.fields.HTMLField', [], {}),
            'description_en': ('djangocms_text_ckeditor.fields.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'description_es': ('djangocms_text_ckeditor.fields.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'html_class': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'portafolio.sociallink': {
            'Meta': {'object_name': 'SocialLink'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'social_links'", 'to': u"orm['portafolio.TeamMember']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'portafolio.team': {
            'Meta': {'object_name': 'Team'},
            'description': ('djangocms_text_ckeditor.fields.HTMLField', [], {'default': "''"}),
            'description_en': ('djangocms_text_ckeditor.fields.HTMLField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'description_es': ('djangocms_text_ckeditor.fields.HTMLField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'teams'", 'symmetrical': 'False', 'to': u"orm['portafolio.TeamMember']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'name_es': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '50'})
        },
        u'portafolio.teammember': {
            'Meta': {'ordering': "('created_at',)", 'object_name': 'TeamMember'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['filer.Image']", 'null': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'position_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'position_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'strong_skills': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'strong_skills_en': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'strong_skills_es': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'summary': ('djangocms_text_ckeditor.fields.HTMLField', [], {}),
            'summary_en': ('djangocms_text_ckeditor.fields.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'summary_es': ('djangocms_text_ckeditor.fields.HTMLField', [], {'null': 'True', 'blank': 'True'})
        },
        u'portafolio.teamplugin': {
            'Meta': {'object_name': 'TeamPlugin', 'db_table': "u'cmsplugin_teamplugin'", '_ormbases': ['cms.CMSPlugin']},
            u'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'plugins'", 'to': u"orm['portafolio.Team']"})
        }
    }

    complete_apps = ['portafolio']