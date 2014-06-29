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
from coils.core import Command, BLOBManager
from command import ContactCommand


def get_default_contact_thumbnail(context):

    project = context.run_command(
        'project::get', id=7000, access_check=False,
    )
    if not project:
        return None

    document = context.run_command(
        'project::get-path',
        path='/Thumbnails/text-vcard.png',
        project=project,
        access_check=False,
    )
    if document:
        handle = context.run_command(
            'document::get-handle', document=document,
        )
        return handle, 'image/png', 'text-vcard.png'
    return None, None, None


class GetPhotoHandle(Command, ContactCommand):

    """
    Retrieve the image related to a contact.

    The image is assumed to be either a gravatar, photo, or the
    default thumbnail.

    Return value is a tuple of HANDLE, MIMETYPE, ETAG.  This tuple may
    be (None, None, None, ) if the contact's image is not available and no
    default thumbnail for text/vcard type has been configured.
    """

    __domain__ = "contact"
    __operation__ = "get-photo-handle"
    mode = None

    def __init__(self):
        Command.__init__(self)

    def parse_parameters(self, **params):
        """
        Parse parameters.

        Only one command specific parameter - "contact" - which is mandatory
        """
        Command.parse_parameters(self, **params)
        self.obj = params.get('contact', None)

    def run(self):
        """Resolve the contact image."""

        rights = self._ctx.access_manager.access_rights(self.obj, )

        if 'r' in rights:
            rfile = BLOBManager.Open(
                'documents/{0}.picture.jpg'.format(self.obj.object_id, ),
                mode='rb',
                encoding='binary',
            )
            if rfile:
                self.set_return_value(
                    (rfile,
                     'image/jpeg',
                     '{0}:contact-image'.format(self.obj.object_id, ),
                     )
                )
                return
        self.set_return_value(get_default_contact_thumbnail(self._ctx))
