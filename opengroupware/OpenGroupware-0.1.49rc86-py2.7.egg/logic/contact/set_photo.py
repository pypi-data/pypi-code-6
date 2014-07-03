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
# THE SOFTWARE
#
import shutil
from coils.core import \
    Command, \
    NotSupportedException, \
    BLOBManager, \
    Contact, \
    AccessForbiddenException
from command import ContactCommand

LEGAL_PHOTO_MIMETYPES = ('image/jpeg', 'image/jpg', 'image/x-jpeg', )


class SetPhoto(Command, ContactCommand):
    __domain__ = "contact"
    __operation__ = "set-photo"
    mode = None

    def __init__(self):
        Command.__init__(self)

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        self.obj = params.get('contact', None)
        self._mimetype = params.get('mimetype', 'application/octet-stream')
        self._handle = params.get('handle', None)
        # TODO: raise error if there is no handle or no contact

    def check_run_permissions(self):
        rights = self._ctx.access_manager.access_rights(self.obj, )
        if not set('w').intersection(rights):
            raise AccessForbiddenException(
                'Insufficient access to {0}'.format(self.obj, )
            )

    def run(self):

        if not isinstance(self.obj, Contact):
            raise NotSupportedException(
                'Object provided to contact::set-photo not a Contact'
            )

        if self._mimetype not in LEGAL_PHOTO_MIMETYPES:
            raise NotSupportedException(
                'Contact photos must be of type "image/jpeg", content '
                'of type "{0}" was provided by the application'.format(
                    self._mimetype,
                )
            )

        # TODO: Check size is under max
        # TODO: Verify image format for reals

        wfile = BLOBManager.Open(
            'documents/{0}.picture.jpg'.format(self.obj.object_id, ),
            mode='wb',
            encoding='binary',
            create=True,
        )
        shutil.copyfileobj(self._handle, wfile)
        wfile.flush()
        wfile.close()
