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

import six

from abc import ABCMeta, abstractmethod

from ._Action import Action
from ..util import NotConfirmedError


@six.add_metaclass(ABCMeta)
class ConfirmAction(Action):
    """An abstract Action that requests user confirmation

    If any confirm_config request fails, snakewatch will not run.
    """
    def __init__(self, cfg, ui_confirm, required_attributes=list()):
        super(ConfirmAction, self).__init__(cfg, required_attributes)

        if not ui_confirm(self.confirm_message()):
            raise NotConfirmedError()

    @abstractmethod
    def confirm_message(self):
        pass

    def release_resources(self):
        pass

    def run_on(self, line):
        pass

