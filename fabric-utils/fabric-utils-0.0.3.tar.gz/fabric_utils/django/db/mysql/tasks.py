from fabric.api import task, env, run, local
from fabric.contrib import django
from fabric.operations import get
from fabric_utils.django.server.utils import sudo_command
import time


@task
def dumpdata():
    command = ('./manage.py dumpdata --indent=2 > /tmp/cirujanos_dump.json')
    command_params = ()
    sudo_command(command, command_params)


@task
def restore_db():
    "Download dump of production DB and loads it in local DB"
    timestamp = time.strftime('%Y%m%d%H%M%S')
    dump_file = "%s_%s.sql" % ('cirujanos_production', timestamp)
    dump_path = "/tmp/%s" % dump_file
    run("mysqldump -u {user} -p{password} {db_name} > {dump_path}"
        .format(db_name='cirujanos_production',
                tbl_name='web_slider',
                user='production',
                password='production',
                dump_path=dump_path)
        )

    # Download
    get(remote_path=dump_path, local_path="data/" + dump_file)
    # Load new dump
    local("mysql -u {user} -p{password} -h {db_host} {db_name} < {dump_path}"
          .format(user='development', password='development',
                  db_host='cirujanostoracicos.local',
                  db_name='cirujanos_development',
                  dump_path='data/' + dump_file))


def mysqldump_backup():
    django.project('config.settings.%s' % env.environment)
    from django.conf import settings
    command = ('./mysqldump -u %s -p=%s %s > /tmp/cirujanos_dump.json')
    command_params = (settings.DATABASE_USER,
                      settings.DATABASE_PASSWORD,
                      settings.DATABASE_NAME)
    sudo_command(command, command_params)
