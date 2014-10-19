from fabric.api import task, env
from fabric_utils.django.server.utils import sudo_command


@task
def createsuperuser(username="admin", email="admin@gmail.com"):
    command = ('python manage.py createsuperuser '
               ' --username=%s '
               ' --email=%s '
               ' --settings="config.settings.%s"')
    command_params = (username, email, env.environment)
    sudo_command(command, command_params)


@task
def loaddata(fixture):
    command = ('./manage.py loaddata %s '
               ' --settings="config.settings.%s" '
               ' --verbosity=3; ')
    command_params = (fixture, env.environment)
    sudo_command(command, command_params)


@task
def rollback(app, migration_id):
    command = ('./manage.py migrate %s %s '
               ' --fake '
               ' --settings="config.settings.%s"; ')
    command_params = (app, migration_id, env.environment)
    sudo_command(command, command_params)


@task
def migrate(app):
    command = ('./manage.py migrate %s '
               ' --settings="config.settings.%s"; ')
    command_params = (app, env.environment)
    sudo_command(command, command_params)
