#
# Copyright (c) 2009, 2014
#  Adam Tauno Williams <awilliam@whitemice.org>
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
#
from coils.core import Appointment, CoilsException, AccessForbiddenException
from coils.core.logic import DeleteCommand


class DeleteAppointment(DeleteCommand):
    __domain__ = "appointment"
    __operation__ = "delete"

    def check_run_permissions(self):
        rights = self._ctx.access_manager.access_rights(self.obj)
        if not set('adt').intersection(rights):
            raise AccessForbiddenException(
                'Insufficient access to {0}'.format(self.obj, ))

    def parse_parameters(self, **params):
        DeleteCommand.parse_parameters(self, **params)
        self._cyclic = bool(params.get('all', False))

    def delete_comment(self):
        self._ctx.run_command(
            'appointment::delete-comment', appointment=self.obj,
        )

    def delete_participants(self):
        self._ctx.run_command(
            'appointment::delete-participants', object=self.obj,
        )

    def run(self):
        if (self.obj is None):
            raise CoilsException('No appointment provided for deletion.')
        if self._cyclic and self.obj.parent_id:
            apps = self._ctx.db_session.query(Appointment).\
                filter(Appointment.parent_id == self.obj.parent_id)
            for app in apps:
                if app.object_id != self.obj.object_id:
                    self._ctx.run_command('appointment::delete', object=app, )
        self.delete_participants()
        self.delete_comment()
        DeleteCommand.run(self)
