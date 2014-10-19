#!/usr/bin/env python
# coding: utf-8

from __future__ import division, print_function, unicode_literals

import sys
from os import environ, getcwd
from os.path import dirname, isdir, join, realpath, basename, exists
from os import makedirs

from clint.arguments import Args
from clint.textui import colored, indent, puts
from jinja2 import Environment, FileSystemLoader, Template


def red(text):
    puts(colored.red(text))


def green(text):
    puts(colored.green(text))


exit = sys.exit
#from future_builtins import *


def get_template_dir(current_dir, user_templates):
    for path in walk_upper(current_dir):
        full_path = join(path, user_templates)
        print(full_path)
        if isdir(full_path):
            return full_path
    print(join(dirname(realpath(__file__)), '.templates'))

dir = join(dirname(realpath(__file__)), '.templates')
dir = dirname(dir)
# print(dir)


def walk_upper(path=__file__):
    #dir = os.path.dirname(os.path.realpath(path))
    dir = realpath(path)
    while dir != '/':
        yield dir
        dir = dirname(dir)
# print(os.path.isdir(dir))


def render(path, kvargs):
    return Template(get_template(path)).render(**kvargs)


# os.makedirs(


def get_template_name():
    if Args().grouped['_'].all:
        return Args().grouped['_'].all[0]
    red('Please set template name.')
    exit(0)


def get_cli_params():
    all_args = Args().grouped
    res = {}
    for item in all_args:
        if item.startswith('-') and (not (item is '_')):
            value = all_args[item].all
            value = value[0] if len(value
                                 ) == 1 else value
            res[item.lstrip('-')] = value
    return res


def read_config(path):
    res = {}
    path = join(path, '_config')
    for line in open(path).read().split('\n'):
        if len(line.split('=')) != 2:
            continue
        key, value = line.split('=')
        res[key.strip()] = value.strip()
    return res.items()


def make_dir(path):
    directory = dirname(path)
    if not exists(directory):
        makedirs(directory)

import codecs

def main():
    template_name = get_template_name()
    params = get_cli_params()
    current_dir = getcwd()
    user_templates = environ.get("TEMPLETOR_DIR", '.templates')
    template_dir = join(
        get_template_dir(current_dir, user_templates), template_name)
    print(template_dir, params)
    template_loader = FileSystemLoader(searchpath=template_dir)

    env = Environment(loader=template_loader)
    for filename, path in read_config(template_dir):
        template_rendered = env.get_template(filename).render(params)
        path = join(current_dir, Template(path).render(params).lstrip('/'))
        make_dir(path)
        with codecs.open(path, "w", "utf-8") as temp:
            temp.write(template_rendered)


if __name__ == "__main__":
    main()
