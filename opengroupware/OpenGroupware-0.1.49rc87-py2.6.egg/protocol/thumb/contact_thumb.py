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
from coils.core import BLOBManager, NoSuchPathException, CoilsException
from coils.net import PathObject
try:
    from PIL import Image
    IMAGE_RESIZE_ENABLED = True
except:
    IMAGE_RESIZE_ENABLED = False


class ContactThumb(PathObject):

    def __init__(self, parent, name, **params):
        self.name = name
        self.entity = None
        self.request = None
        PathObject.__init__(self, parent, **params)

    def _get_thumbnail(self):
        rfile, mimetype, etag = self.context.run_command(
            'contact::get-photo-handle',
            contact=self.entity,
        )
        return rfile, mimetype, etag,

    def do_HEAD(self):
        handle, mimetype, etag, = self._get_thumbnail()
        if not handle:
            raise NoSuchPathException(
                'No thumbnail available for OGo#{0}'.
                format(self.entity.object_id, )
            )
        self.request.simple_response(
            200,
            data=None,
            mimetype=mimetype,
            headers={
                'etag':  etag,
                'Cache-Control': 'max-age=60480',
                'Content-Disposition': 'inline; filename={0}-thumbnail'.format(
                    self.entity.object_id,
                )
            },
        )

    def do_GET(self):
        handle, etag, filename = self._get_thumbnail()
        if not handle:
            raise NoSuchPathException(
                'No thumbnail available for OGo#{0}'.
                format(self.entity.object_id, )
            )

        client_etag = self.request.headers.get('If-None-Match', None)

        if client_etag and client_etag == etag:

            self.request.simple_response(
                304,
                data=None,
                mimetype='image/png',
                headers={
                    'etag':  etag,
                    'Cache-Control': 'max-age=60480',
                    'Content-Disposition': 'inline; filename={0}'.format(
                        filename,
                    ),
                },
            )
            BLOBManager.Close(handle)
            return

        if IMAGE_RESIZE_ENABLED:
            try:
                scratch_file = BLOBManager.ScratchFile()
                image = Image.open(handle)
                image.thumbnail((175, 175, ), Image.ANTIALIAS, )
                image.save(scratch_file, 'png', )
            except:
                # TODO: Log the exception
                # TODO: Cache the contact image thumbnail?  somehow
                raise CoilsException('Exception resizing contact image')
            else:
                BLOBManager.Close(handle)
                handle = scratch_file
                handle.seek(0)

        self.request.stream_response(
            200,
            stream=handle,
            mimetype='image/png',
            headers={
                'Content-Disposition': 'inline; filename={0}'.format(
                    filename,
                ),
                'Cache-Control': 'max-age=60480',
                'etag': etag,
            },
        )

        BLOBManager.Close(handle)
