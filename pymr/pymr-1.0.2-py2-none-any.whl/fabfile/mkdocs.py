from fabric.api import local, task


@task
def build():
    """
    create a new build of the docs
    """
    cmd = '. ./.pymr/bin/activate && '
    cmd += 'mkdocs build'
    local(cmd)


@task
def serve():
    """
    start the mkdocs development server
    """
    cmd = '. ./.pymr/bin/activate && '
    cmd += 'mkdocs serve'
    local(cmd)
