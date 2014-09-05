#coding=utf-8
from io import StringIO
from django.conf import settings
from django.core.management import BaseCommand
from django.utils.translation import ugettext as _


__author__ = 'flanker'


class Command(BaseCommand):

    def handle(self, *args, **options):
        conf = settings.CONFIGURATION
        print(_('Read .ini configuration files: '))
        print(', '.join(conf.read_filenames))
        print('')
        print(_('Content of the configuration, including default values:'))
        v = StringIO()
        conf.write(v)
        print(v.getvalue())
        print(_('Available settings in section [updoc]:'))
        print(_('ROOT_PATH: base path for all data'))
        print(_('HOST: your server URL (http://localhost:8000) — no trailing slash!'))
        print(_('DEBUG: debug mode (default : True)'))
        print(_('TIME_ZONE: Europe/Paris'))
        print(_('LANGUAGE_CODE: fr-fr'))
        print(_('USE_XSENDFILE: use it if your can use Apache with mode_xsendfile'))
        print(_('REMOTE_USER_HEADER: HTTP header with remote user'))
        print(_('DATABASE_ENGINE: default: django.db.backends.sqlite3'))
        print(_('DATABASE_NAME'))
        print(_('DATABASE_USER'))
        print(_('DATABASE_PASSWORD'))
        print(_('DATABASE_HOST'))
        print(_('DATABASE_PORT'))
        print(_('PUBLIC_INDEX: show index to anonymous users, default: true'))
        print(_('PUBLIC_DOCS: show docs to anonymous users, default: true'))
        print(_('PUBLIC_BOOKMARKS: show favorites to anonymous users, default: true'))
        print(_('PUBLIC_PROXIES: show proxy.pac to anonymous users, default: true'))
        print(_('ADMIN_EMAIL: default: admin@example.com'))
        print(_('ES_HOSTS: elastic search servers, separated by commas (default: localhost:9200). Empty if no ES'))
        print(_('ES_INDEX: ES index (default: updoc)'))
        print(_('ES_TIKA_EXTENSIONS: ES tika extensions (default: pdf,html,doc,odt,rtf,epub)'))
        print(_('ES_MAX_SIZE: ES max size of indexed documents (default: 30 MB)'))
        print(_('ES_DOC_TYPE: ES document type (default: document)'))
        print(_('ES_PLAIN_EXTENSIONS: ES plain documents (default: txt,csv,md,rst)'))
        print(_('ES_EXCLUDED_DIR: ES excluded directories(default: _sources,_static)'))


if __name__ == '__main__':
    import doctest

    doctest.testmod()