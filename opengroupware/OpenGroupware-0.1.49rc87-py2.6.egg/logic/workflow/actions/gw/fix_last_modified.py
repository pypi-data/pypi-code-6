#
# Copyright (c) 2014
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
# THE SOFTWARE.
#
from lxml import etree
from coils.foundation import UniversalTimeZone
from coils.core import Task, OGO_ROLE_SYSTEM_ADMIN, CoilsException
from coils.core.logic import ActionCommand


class FixTaskLastModified(ActionCommand):
    __domain__ = "action"
    __operation__ = "fix-task-lastmodified"
    __aliases__ = ['fixTaskLastModified', "fixTaskLastModifiedAction", ]

    def __init__(self):
        ActionCommand.__init__(self)

    def parse_action_parameters(self):
        pass

    def check_run_permissions(self):
        if self._ctx.has_role(OGO_ROLE_SYSTEM_ADMIN):
            return
        raise CoilsException(
            'Insufficient privilages to invoke fixTaskLastModifiedAction'
        )

    def do_action(self):
        """
        Perform the action of correct trailing last-modified time stamps.

        TODO: This type of action should be performed in Logic, and then
        wrapped in an Action, not implemented in an Action.
        TODO: This action could store its last run time in a server property
        and floor based on that value;  this would potentially reduce the
        number of tasks that would need to be scanned at each iteration.  Not
        sure if that is worth the trouble.
        """
        db = self._ctx.db_session()
        counter = 0

        query = db.query(Task).filter(
            Task.state.in_(['00_created', '02_rejected', '25_done', ])
        )

        for task in query.all():
            changed = False
            last_modified = task.modified
            for action in task.notes:
                value = action.action_date.replace(tzinfo=UniversalTimeZone())
                if not last_modified or value > last_modified:
                    last_modified = value
            if not last_modified == task.modified:
                task.modified = value
                if task.version:
                    task.version += 1
                else:
                    task.version = 2
                counter += 1

        self.wfile.write(unicode(counter))
