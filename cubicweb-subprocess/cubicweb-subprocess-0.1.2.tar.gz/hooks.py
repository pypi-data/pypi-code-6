# -*- coding: utf-8 -*-
# copyright 2014 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.

"""cubicweb-subprocess specific hooks and operations"""

from cubicweb.predicates import is_instance, on_fire_transition, score_entity
from cubicweb.server import hook, ON_COMMIT_ADD_RELATIONS


class StartHook(hook.Hook):
    __regid__ = 'subprocess.start'
    __select__ = hook.Hook.__select__ & on_fire_transition('Subprocess', 'start')
    events = ('after_add_entity',)
    category = 'subprocess.workflow'

    def __call__(self):
        StartOp(self._cw, subprocess=self.entity.for_entity)


class StartOp(hook.Operation):
    def postcommit_event(self):
        self.subprocess.start()


class KillHook(hook.Hook):
    __regid__ = 'subprocess.kill'
    __select__ = hook.Hook.__select__ & on_fire_transition('Subprocess', 'kill')
    events = ('after_add_entity',)
    category = 'subprocess.workflow'

    def __call__(self):
        KillOp(self._cw, subprocess=self.entity.for_entity)


class KillOp(hook.Operation):
    def postcommit_event(self):
        self.subprocess.kill()
