#
# Copyright (c) 2011, 2012, 2013, 2014
#   Adam Tauno Williams <awilliam@whitemice.org>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE
#
from coils.core import \
    Team, OGO_ROLE_SYSTEM_ADMIN, AccessForbiddenException, CoilsException
from coils.core.logic import CreateCommand
from keymap import COILS_TEAM_KEYMAP
from command import TeamCommand


class CreateTeam(CreateCommand, TeamCommand):
    __domain__ = "team"
    __operation__ = "new"

    def prepare(self, ctx, **params):
        self.keymap = COILS_TEAM_KEYMAP
        self.entity = Team
        CreateCommand.prepare(self, ctx, **params)

    def check_run_permissions(self):
        if self._ctx.has_role(OGO_ROLE_SYSTEM_ADMIN):
            return
        raise AccessForbiddenException(
            'Context lacks role; cannot create teams.'
        )

    def parse_parameters(self, **params):
        CreateCommand.parse_parameters(self, **params)

    def fill_missing_values(self):
        self.obj._is_team = 1
        if not self.obj.number:
            self.obj.number = 'OGo{0}'.format(self.obj.object_id, )
        if not self.obj.login:
            self.obj.login = self.obj.number

    def sanitize_values(self):

        '''
        Make sure Team.is_locality is something valid - 0 or 1
        '''
        if self.obj.is_locality is None:
            self.obj.is_locality = 0
        if not isinstance(self.obj.is_locality, int):
            try:
                self.obj.is_locality = int(self.obj.is_locality)
            except:
                self.obj.is_locality = 0
        if self.obj.is_locality not in (0, 1, ):
            self.obj.is_locality = 0

    def run(self):
        # TODO: Grant this right to members of the 'team creators' team.
        if self._ctx.is_admin:
            CreateCommand.run(self)
            self.fill_missing_values()
            self.sanitize_values()
            self.set_membership()
            self.save()
        else:
            raise CoilsException(
                'Update of a team entity requires administrative privileges'
            )
