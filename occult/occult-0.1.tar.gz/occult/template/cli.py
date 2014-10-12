# -*- coding: utf-8 -*-

import os
import argparse

from clint.textui import prompt, puts, colored, indent

from occult._generator.configreader import ConfigReader
from occult._generator.taskmanager import TaskManager


DEFAULT_CONFIGURATION_FILE = 'package.json'
TEMPLATES_FILE = 'templates.json'
TEMPLATES_CONFIGURATION_FILE = 'configuration.json'

configuration = ConfigReader(os.path.join(os.getcwd(), DEFAULT_CONFIGURATION_FILE))

def subparser_init(args):
    global  configuration

    if is_not_empty_package():
        return

    select_template()

def select_template():
    global configuration

    list = get_templates()
    puts(colored.green('Please Select The Template:'))
    for index, value in enumerate(list):
        with indent(2):
            puts('%d) %s' % (index+1, value.get('title')))

    old = configuration.get('template', 1)
    new = raw_input('[%s] Template: (%s) ' % (colored.green('?'), str(old)))
    new_value = old if not new else int(new)

    if new_value > len(list):
        puts(colored.yellow('Warning!') + ' %s is ' % new + colored.yellow('INVALID'))
        select_template()
    else:
        configuration.put('template', new_value)

    templates = get_templates()
    configuration_path = None;

    for index, value in enumerate(templates):
        if index+1 == configuration.get('template'):
            path = value.get('directory', None)
            configuration_path = os.path.join(os.path.dirname(__file__), path, TEMPLATES_CONFIGURATION_FILE)
            break

    if not configuration_path or not os.path.exists(configuration_path):
        puts(colored.yellow('Warning!') + ' %s is ' % new + colored.yellow('INVALID'))
        select_template()
    else:
        configuration.put('template_path', get_template_path())
        make_and_run_taskmanager(configuration_path)

def get_templates():
    raw = ConfigReader(os.path.join(os.path.dirname(__file__), TEMPLATES_FILE))
    return raw.data.get('templates', [])

def get_template_path():
    global configuration

    templates = get_templates()
    path = None;

    for index, value in enumerate(templates):
        if index+1 == configuration.get('template'):
            path = value.get('directory', None)
            break

    if path is not None:
        path = os.path.abspath(os.path.join(os.path.dirname(__file__),path))

    return path

def make_and_run_taskmanager(path):
    global configuration
    taskmanager = TaskManager(path, extra= {'configuration':configuration})
    taskmanager.run_all()

def is_not_empty_package():
    if os.path.exists(os.path.join(os.getcwd(), DEFAULT_CONFIGURATION_FILE)):
        return not prompt.yn(colored.red('Attention!') + ' The configuration file is exist, this will override it. Are you sure?')
    else:
        return False

def execute():
    parser = argparse.ArgumentParser(description = 'Generator')
    subparsers = parser.add_subparsers()

    init_parser = subparsers.add_parser('init')
    init_parser.set_defaults(func = subparser_init)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    execute()

