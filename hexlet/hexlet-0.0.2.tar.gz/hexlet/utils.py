import yaml
import os
import pip
import time
import sys
import os
import click
from hexlet import exceptions

if sys.version_info > (3,0):
    from xmlrpc import client as xmlrpclib
else:
    import xmlrpclib

app_path = click.get_app_dir('Hexlet', force_posix=True)
config_path = os.path.join(app_path, "credentials")


def value_for(key):
    try:
        with open(config_path, 'r') as stream:
            return yaml.load(stream)[key]
    except IOError:
        raise exceptions.ConfigError()


def write_config(data):
    if not os.path.isdir(app_path):
        os.mkdir(app_path)
    with open(config_path, 'w+') as outfile:
        outfile.write(yaml.dump(data, default_flow_style=False))


def look_for_new_version(project_name):
    try:
        pypi = xmlrpclib.ServerProxy("https://pypi.python.org/pypi")

        dist = next(dist for dist in pip.get_installed_distributions() if dist.project_name == project_name)

        available = pypi.package_releases(project_name)
        if not available:
            available = pypi.package_releases(project_name.capitalize())
    except StopIteration:
        raise exceptions.VersionUpdateError("Package %s is not installed" % project_name)
    except Exception as ex:
        raise exceptions.VersionUpdateError("Version update exception: %s" % str(ex))

    if not available:
        # FIXME replace with exception 'Not available on pipy.python.org'
        return (False, dist.version, "")
    elif available[0] != dist.version:
        return (True, dist.version, available[0])
    else:
        return (False, dist.version, available[0])


class UpdateBeforeCall(object):
    def __init__(self, project_name):
        self.project_name = project_name

    def __call__(self, original_func):
        decorator_self = self
        def wrapper(*args, **kwargs):
            project_info = look_for_new_version(decorator_self.project_name)
            if project_info[0]:
                print("New version available (%s), please update (your version installed - %s)" % \
                    (project_info[2], project_info[1]))
            else:
                return original_func(*args,**kwargs)
        return wrapper


def benchmark(func):
    def wrapper(*args, **kwargs):
        t = time.clock()
        res = func(*args, **kwargs)
        print("Time - ", time.clock() - t)
        return res
    return wrapper


def build_key_value(params):
    def iter(params, path, base):
        if isinstance(params, dict):
            for k, v in params.items():
                path_copy = list(path)
                path_copy.append("[%s]" % k)
                if isinstance(v, dict) or isinstance(v, list):
                    iter(v, path_copy, base)
                else:
                    base["".join(path_copy)] = v
        elif isinstance(params, list):
            for idx, v in enumerate(params):
                path_copy = list(path)
                path_copy.append("[%s]" % idx)
                if isinstance(v, dict) or isinstance(v, list):
                    iter(v, path_copy, base)
                else:
                    base["".join(path_copy)] = v

    base = {}
    for k, v in params.items():
        path = []
        path.append(k)
        iter(v, path, base)

    return base
