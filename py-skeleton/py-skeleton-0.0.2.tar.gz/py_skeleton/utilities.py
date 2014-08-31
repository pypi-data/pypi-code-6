#!/usr/bin/env python
# -*- coding: utf-8 -*-

import fnmatch
import os
from py_utilities.fs.file_utilities import iter_files
from py_utilities.fs.file_utilities import write_file
from py_utilities.fs.fs_utilities import mkdir_p
import re

TEMPLATED_RE = re.compile(r'(\{\{([\w\s\.]+)\}\})')


def render_template_to_target(
        env,
        tmpl_src,
        context_dict,
        tmpl_target,
        tmpl_ext):

    contents = get_template_contents(env, tmpl_src, context_dict)
    mkdir_p(os.path.dirname(tmpl_target))
    write_file(tmpl_target.replace(tmpl_ext, ''), contents)


def get_template_contents(env, tmpl_src, context_dict):
    tmpl = env.get_template(tmpl_src)
    return tmpl.render(context_dict)


def iter_files_filter(dir_path, filter_pattern):
    for file in iter_files(dir_path):
        if fnmatch.fnmatch(os.path.basename(file), filter_pattern):
            yield file


def resolve_templated_file_path(templated_file_path, config):
    match = TEMPLATED_RE.search(templated_file_path)
    if match:
        templated_value = config.get(match.group(2))
        if templated_value:
            return templated_file_path.replace(match.group(1), templated_value)
    return templated_file_path


# vim: filetype=python
