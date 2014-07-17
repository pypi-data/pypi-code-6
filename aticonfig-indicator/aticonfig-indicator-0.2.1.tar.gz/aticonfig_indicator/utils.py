import subprocess


def parse_aticonfig(s):
    for line in s.split('\n'):
        l = line.strip()
        if l.startswith('Sensor 0: Temperature - '):
            return l.split('Sensor 0: Temperature - ')[1].split()[0]

    return None


def get_aticonfig_output():
    s = subprocess.check_output(["aticonfig", "--adapter=0", "--od-gettemperature"])

    return s


def get_temp():
    aticonfig_output = get_aticonfig_output()


    temp_from_aticonfig = parse_aticonfig(aticonfig_output)
    if temp_from_aticonfig:
        return temp_from_aticonfig.split('.')[0]

    return "N/A"

import os


def image_path(name):
    """Returns path to the image file by its name"""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "img", "%s.svg" % name))
