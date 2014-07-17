from fabric.api import sudo, env, run
from fabric.colors import green, red, cyan


def pgreen(text):
    print(green(text))


def pred(text):
    print(red(text))


def pcyan(text):
    print(cyan(text))


def remote_shell_vars():
    return {
        "home": run('echo $HOME', shell=True)
    }


def sudo_command(command, command_params):
    config = (
        'cd %s; '
        'source %s/env/bin/activate; '
        'export PYTHONPATH=$PYTHONPATH:%s/apps/cirujanos/releases/current; '
    )
    config_params = (env.release_path, env.www_path, env.shell_vars["home"])
    pgreen(('COMMAND: ' + command) % command_params)
    sudo((config + command) % (config_params + command_params))
