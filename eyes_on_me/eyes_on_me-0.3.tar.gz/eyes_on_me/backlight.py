import subprocess
import string


def set_backlight(level):
    subprocess.check_call("xbacklight -set %(level)s" % locals(), shell=True)


def get_backlight():
    return float(string.strip(subprocess.check_output("xbacklight", shell=True)))
