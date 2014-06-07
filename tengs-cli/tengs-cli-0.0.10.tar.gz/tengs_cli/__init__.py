import yaml
from tengs_cli import settings

from clint.textui import colored

def generate_url(url, api_key=None):
    if api_key == None:
        api_key = value_for("api_key")
    url = "{0}/api/{1}?api_key={2}".format(settings.site, url, api_key)
    return url

def value_for(key):
    stream = open(settings.file_path, 'r')
    return yaml.load(stream)[key]

def write_config(data):
    with open(settings.file_path, 'w+') as outfile:
        outfile.write(yaml.dump(data, default_flow_style=False))

def logger(current_level, level, message):
    if current_level == level:
        print("[{0}] {1}".format(colored.yellow(level), message))
