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

"""cubicweb-collaboration specific hooks and operations"""

from cubicweb import Unauthorized
from cubicweb.server.hook import Hook, match_rtype
from cubicweb.predicates import adaptable


class GrantOwnersPermissions(Hook):
    """Grant read/write permissions to the owners of the collaborative
    entity."""
    __regid__ = 'collaboration.set_owners_permissions'
    __select__ = Hook.__select__ &  match_rtype('owned_by')
    events = ('after_add_relation',)

    def __call__(self):
        adapted = self._cw.entity_from_eid(self.eidfrom).cw_adapt_to('ICollaborationSecurity')
        if adapted:
            # Else the collaborative entity does not support security
            # relations.
            adapted.grant_permission(self.eidto, 'write')


class RevokeOwnersPermissions(Hook):
    """Revoke read and write permissions for users who do not own the collaborative
    entity anymore."""
    __regid__ = 'collaboration.revoke_owners_permissions'
    __select__ = Hook.__select__ &  match_rtype('owned_by')
    events = ('after_delete_relation',)

    def __call__(self):
        entity = self._cw.entity_from_eid(self.eidfrom)
        adapted = entity.cw_adapt_to('ICollaborationSecurity')
        if adapted:
            # Else the collaborative entity does not support security
            # relations.
            adapted.revoke_permission(self.eidto, 'write')
            c_adapted = entity.cw_adapt_to('ICollaborative')
            if self.eidto not in (user.eid for user in c_adapted.collaborators):
                adapted.revoke_permission(self.eidto, 'read')


class GrantReadCollaboratorsHook(Hook):
    __regid__ = 'grant-read-collaborators'
    __select__ = Hook.__select__ & match_rtype('collaborates_on')
    events = ('before_add_relation',)

    def __call__(self):
        adapted = self._cw.entity_from_eid(self.eidto).cw_adapt_to('ICollaborationSecurity')
        adapted.grant_permission(self.eidfrom, 'read')


class RevokeReadCollaboratorsHook(Hook):
    __regid__ = 'revoke-read-collaborators'
    __select__ = Hook.__select__ & match_rtype('collaborates_on')
    events = ('after_delete_relation',)

    def __call__(self):
        entity = self._cw.entity_from_eid(self.eidto)
        adapted = entity.cw_adapt_to('ICollaborationSecurity')
        if self.eidfrom not in (u.eid for u in entity.owned_by):
            adapted.revoke_permission(self.eidfrom, 'read')


