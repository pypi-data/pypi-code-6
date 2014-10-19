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
