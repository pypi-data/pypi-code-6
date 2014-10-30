import subprocess
import sys


def execute_cmd(cmd):
    output = subprocess.check_output(cmd, shell=True)
    return output[:-1]


def get_input(message):
    if is_screen_available():
        return raw_input(message).strip()
    else:
        return False


def is_screen_available():
    try:
        sys.stdin = open('/dev/tty')
        return True
    except IOError:
        return False
