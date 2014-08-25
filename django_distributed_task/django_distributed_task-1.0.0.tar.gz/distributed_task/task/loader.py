from django import get_version

from django.utils.module_loading import module_has_submodule
from importlib import import_module

TASKS_MODULE_NAME = 'tasks'


def get_task_paths():
    if get_version() < '1.7':
        return get_installed_apps16()

    return get_installed_apps17()


def get_installed_apps17():
    from django.apps import apps

    for app_config in apps.get_app_configs():
        if module_has_submodule(app_config.module, TASKS_MODULE_NAME):
            yield '%s.%s' % (app_config.name, TASKS_MODULE_NAME)


def get_installed_apps16():
    from django.conf import settings
    INSTALLED_APPS = getattr(settings, 'INSTALLED_APPS', list())

    for app in INSTALLED_APPS:
        module = import_module(app)
        if module_has_submodule(module, TASKS_MODULE_NAME):
            yield '%s.%s' % (app, TASKS_MODULE_NAME)