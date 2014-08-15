"""
This file is part of snakewatch.

snakewatch is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

snakewatch is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with snakewatch.  If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import print_function, absolute_import, unicode_literals, division

import importlib
import json
import os
import re
import six

from . import USER_PATH
from .util import AbortError, ConfigError, NotConfirmedError, ui_print, set_config
from .action._ConfirmAction import ConfirmAction


def lower_keys(x):
    """Recursively make all keys lower-case"""
    if isinstance(x, list):
        return [lower_keys(v) for v in x]
    if isinstance(x, dict):
        return dict((k.lower(), lower_keys(v)) for k, v in x.items())
    return x


def find_config(filename):
    if filename.startswith(''.join([os.curdir, os.sep])) or filename.startswith(os.sep):
        return os.path.abspath(filename)
    if filename.startswith('.'):
        return os.path.abspath(os.path.join(USER_PATH, filename[1:]))

    curdircfg = find_config(os.path.join(os.curdir, filename))
    userdircfg = find_config(''.join(['.', filename]))

    if not os.path.exists(curdircfg):
        curdircfg = None
    if not os.path.exists(userdircfg):
        userdircfg = None

    cfg = None
    if curdircfg and userdircfg:
        cfg = ui_print().get_choice(
            'Config filename can refer to multiple locations. Please specify.',
            'Config Location',
            [curdircfg, userdircfg]
        )
    elif curdircfg:
        cfg = curdircfg
    elif userdircfg:
        cfg = userdircfg

    return cfg


class Config(object):
    """An in-memory instance of a user .cfg file"""

    available_actions = {}
    
    def __init__(self, cfg_file, ui_kwargs):
        set_config(self)
        self.actions = []

        if isinstance(cfg_file, six.string_types):
            try:
                fp = open(find_config(cfg_file), 'r')
                self.cfg = json.load(fp)
            except Exception as err:
                ui_print().error('Cannot read config from {}'.format(cfg_file), str(err), sep='\n')
                raise AbortError()

            fp.close()
            self.source = cfg_file
        elif isinstance(cfg_file, list):
            self.cfg = cfg_file
            self.source = 'default'
        self.cfg = lower_keys(self.cfg)
        self.check_actions(ui_kwargs)
        
    def check_actions(self, ui_kwargs):
        """Create an action instance for each entry in the config"""
        ptrn = re.compile('[\W]+')

        for entry in self.cfg:
            name = ptrn.sub('', entry['action']).title()
            entry['action'] = name

            action_object_name = '{}Action'.format(name)

            try:
                action = Config.available_actions[name]
            except KeyError:
                action_module = importlib.import_module('snakewatch.action.{}'.format(name))
                Config.available_actions[name] = action = getattr(action_module, action_object_name)

            kwargs = {
                'cfg': entry,
            }
            if issubclass(action, ConfirmAction):
                kwargs['ui_confirm'] = ui_kwargs['ui_confirm']

            try:
                self.actions.append(action(**kwargs))
            except ConfigError as ce:
                ui_print().error('Config error detected:', str(ce), sep='\n')
                raise AbortError()
            except NotConfirmedError as nce:
                ui_print().error('Config entry not confirmed')
                raise AbortError()
            except:
                ui_print().error('Fatal Error when instantiating {}'.format(action_object_name))
                raise
        
    def match(self, line, output_method, **output_kwargs):
        """Perform the first action where action.matches(line) is True

        If a match is found, return the result of action.run_on(line)
          or '' if the result is None

        If no match is found, return the line unchanged
        """
        matched = False
        for action in self.actions:
            if not action.matches(line):
                continue

            matched = True
            result = action.run_on(line)
            if result is not None:
                output_method(result, **output_kwargs)

            if not action.continue_matching():
                break

        if not matched:
            output_method(line, **output_kwargs)


class DefaultConfig(Config):
    """A default default config.

    This config is only used when <USER_PATH>/default.json does not exist,
    and uses Print for all inputs.
    """
    def __init__(self, ui, ui_kwargs, use_file=True):
        user_default = DefaultConfig.file_for(ui)
        if use_file and os.path.exists(user_default):
            super(DefaultConfig, self).__init__(user_default, ui_kwargs)

        cfg = [
            {
                'regex': '.*',
                'action': 'Print',
            },
        ]
        super(DefaultConfig, self).__init__(cfg, ui_kwargs)

    @classmethod
    def file_for(cls, ui):
        return os.path.join(USER_PATH, 'default-{}.json'.format(ui.__class__.__name__))
