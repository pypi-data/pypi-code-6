from fabric.api import local, task, env


@task
def up():
    local(('source /var/www/%s/env/bin/activate; '
           './manage.py runserver 0.0.0.0:8000; ') % env.project_name,
          shell='/bin/bash')
