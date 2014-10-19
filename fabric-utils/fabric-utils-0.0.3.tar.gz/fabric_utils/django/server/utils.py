from fabric.api import sudo, env


def sudo_command(command, command_params):
    config = (
        'cd %s; '
        'source %s/env/bin/activate; '
        'export PYTHONPATH=$PYTHONPATH:%s/apps/cirujanos/releases/current; '
    )
    config_params = (env.release_path, env.www_path, env.shell_vars["home"])
    pgreen(('COMMAND: ' + command) % command_params)
    sudo((config + command) % (config_params + command_params))
