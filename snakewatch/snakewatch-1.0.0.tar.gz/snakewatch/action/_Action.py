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

import copy
import re
import six

from abc import ABCMeta, abstractmethod

from ..util import ConfigError


@six.add_metaclass(ABCMeta)
class Action(object):
    """Base class for all Actions"""

    def __init__(self, cfg, required_attributes=list()):
        self.raw_cfg = copy.deepcopy(cfg)
        self.cfg = cfg
        try:
            self.pattern = re.compile(self.cfg['regex'])
        except Exception as err:
            self._config_error('Invalid RegEx: {!s}'.format(err))

        self.name = self.__module__.split('.')[-1:][0]
        self.stop_matching = 'continue' not in self.cfg or not self.cfg['continue']

        for attr in required_attributes:
            if attr not in cfg:
                self._config_error('missing required attribute {}'.format(attr))

    def _config_error(self, message):
        raise ConfigError('{}: {}\n{}'.format(
            self.__class__.__name__, message, self.cfg
        ))

    def matches(self, line):
        return self.pattern.match(line) is not None

    def continue_matching(self):
        return not self.stop_matching

    @abstractmethod
    def run_on(self, line):
        pass

    @abstractmethod
    def release_resources(self):
        pass
