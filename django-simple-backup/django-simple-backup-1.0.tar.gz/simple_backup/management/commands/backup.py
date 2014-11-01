import os
import shutil
import time
import tempfile
from datetime import datetime
from optparse import make_option

from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMessage
from django.conf import settings
from simple_backup.signals import backup_ready

def maybe_print(text, verbosity):
    if verbosity:
        print text

def delete_old_backup_files(directory, days):
    file_names = os.listdir(directory)
    today = datetime.now()
    for name in file_names:
        file_path = os.path.join(directory, name)
        #won't delete a directory or non- .tar.gz files
        if name.endswith('.tar.gz') and os.path.isfile(file_path):
            stat = os.stat(os.path.join(directory, name))
            delta = today - datetime.fromtimestamp(stat.st_ctime)
            if delta.days > days:
                os.remove(file_path)

def get_backup_name():
    if 'sites' in settings.INSTALLED_APPS:
        from django.contrib.sites.models import Site
        site_name = Site.objects.get_current().name
    else:
        site_name = 'django'
    return site_name + '_' + time.strftime('%Y%m%d-%H%M%S')

def get_safe_dirname(sourcedir):
    if not os.path.isabs(sourcedir):
        sourcedir = os.path.abspath(sourcedir)
    drive, dirname = os.path.splitdrive(sourcedir)
    dirname = dirname.replace(os.path.sep, '_')
    if drive:
        dirname = drive.strip(':') + '_' + dirname
    return dirname

def get_database_parameters():
    if hasattr(settings, 'DATABASES'):
        params = list()
        for name in settings.DATABASES.keys():
            params_for_name = {
                'engine': settings.DATABASES[name]['ENGINE'],
                'name': settings.DATABASES[name]['NAME'],
                'user': settings.DATABASES[name]['USER'],
                'password': settings.DATABASES[name]['PASSWORD'],
                'host': settings.DATABASES[name]['HOST'],
                'port': settings.DATABASES[name]['PORT']
            }
            params.append((name, params_for_name))
        return params
    else:
        return ('default', {
            'engine': settings.DATABASE_ENGINE,
            'name': settings.DATABASE_NAME,
            'user': settings.DATABASE_USER,
            'password': settings.DATABASE_PASSWORD,
            'host': settings.DATABASE_HOST,
            'port': settings.DATABASE_PORT
        })

def backup_sqlite(params, outfile):
    os.system('cp %s %s' % (params['name'], outfile))

def backup_mysql(params, outfile):
    args = ''
    user = params['user']
    password = params['password']
    host = params['host']
    port = params['port']
    if user:
        args += "--user=%s " % user
    if password:
        args += "--password=%s " % password
    if host:
        args += "--host=%s " % host
    if port:
        args += "--port=%s " % port
    args += params['name']
    os.system('mysqldump %s > %s' % (args, outfile))

def backup_postgresql(params, outfile):
    args = ''
    user = params['user']
    password = params['password']
    host = params['host']
    port = params['port']
    if user:
        args += "--username=%s " % user
    if host:
        args += "--host=%s " % host
    if port:
        args += "--port=%s " % port
    args += params['name']

    if password:
        command = 'PGPASSWORD=%s pg_dump %s > %s' % (password, args, outfile)
    else:
        command = 'pg_dump %s -w > %s' % (args, outfile)
    os.system(command)

def backup_database(params, outfile, verbosity):
    engine = params['engine']
    name = params['name']
    if 'mysql' in engine:
        maybe_print('Backing up Mysql database %s' % name, verbosity)
        backup_mysql(params, outfile)
    elif engine in ('postgresql_psycopg2', 'postgresql') or 'postgresql' in engine:
        maybe_print('Backing up Postgresql database %s' % name, verbosity)
        backup_postgresql(params, outfile)
    elif 'sqlite3' in engine:
        maybe_print('Backing up Postgresql database %s' % name, verbosity)
        backup_sqlite(params, outfile)
    else:
        raise CommandError('Backup for the database %s engine not implemented' % engine)

# Based on: http://code.google.com/p/django-backup/
# Based on: http://www.djangosnippets.org/snippets/823/
# Based on: http://www.yashh.com/blog/2008/sep/05/django-database-backup-view/
class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--directory', '-d', action='append', default=[], dest='directories',
            help='Extra directories to back up'),
        make_option('--without-media', '-u', action='store_true', default=False,
            dest='without_media', help='Do not backup the media directory'),
        make_option('--without-db', '-b', action='store_true', default=False,
            dest='without_db', help='Do not back up database'),
    )
    help = "Backup database. Mysql, Postgresql and Sqlite engines are supported"

    def handle(self, *args, **options):
        temp_dir = tempfile.mkdtemp()
        backup_name = get_backup_name()
        #collect all files into this directory
        collect_dir = os.path.join(temp_dir, backup_name)
        os.makedirs(collect_dir)

        #Backup documents?
        if not options['without_media']:
            maybe_print("Backing up uploaded files from %s" % settings.MEDIA_ROOT, options['verbosity'])
            #copy the uploaded media to the temp directory
            dest_dir = os.path.join(collect_dir, os.path.basename(settings.MEDIA_ROOT))
            shutil.copytree(settings.MEDIA_ROOT, dest_dir)

        # Doing backup
        if not options['without_db']:
            database_params = get_database_parameters()
            #todo: allow to select databases to back up
            for name, params in database_params:
                outfile = os.path.join(collect_dir, name + '.sql')
                backup_database(params, outfile, options['verbosity'])

        #backing up extra directoris
        comments = list()
        for directory in options['directories']:
            maybe_print("Backing up directory %s" % directory, options['verbosity'])
            destdir = get_safe_dirname(directory)
            shutil.copytree(directory, os.path.join(collect_dir, destdir))
            comments.append('Directory %s copied to %s' % (directory, destdir))

        #write comments if there are any
        if comments:
            readme_file = open(os.path.join(collect_dir, 'README.txt'), 'w')
            readme_file.write('\n'.join(comments))
            readme_file.close()

        #compress backup
        maybe_print('Compressing backup file', options['verbosity'])
        outfile = os.path.join(temp_dir, backup_name + '.tar.gz')
        os.system('cd %s && tar -czf %s %s' % (temp_dir, outfile, backup_name))

        #move file to the final location
        backups_dir = getattr(settings, 'SIMPLE_BACKUP_DIRECTORY', 'backups')
        if not os.path.exists(backups_dir):
            os.makedirs(backups_dir)

        shutil.move(outfile, backups_dir)
        shutil.rmtree(temp_dir)

        days = options.get('days', getattr(settings, 'SIMPLE_BACKUP_DAYS', None))
        if days:
            try:
                days = int(days)
            except ValueError:
                if options['days']:
                    raise CommandError('value of --days must be an integer')
                else:
                    raise ImproperlyConfigured('value of SIMPLE_BACKUP_DAYS must be an Integer')
            else:
                delete_old_backup_files(backups_dir, days)

        backup_file = os.path.join(backups_dir, os.path.basename(outfile))
        backup_ready.send(None, path=backup_file)
