# coding=utf-8

from south.v2 import SchemaMigration


class Migration(SchemaMigration):
    complete_apps = ['email_helper']
    models = {}

    def forwards(self, orm):
        pass

    def backwards(self, orm):
        pass
