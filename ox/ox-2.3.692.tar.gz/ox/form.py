# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# GPL 2014
from __future__ import with_statement, print_function

import itertools
import mimetypes
import random
import sys

from six import PY2


__all__ = ['MultiPartForm']

# from /usr/lib/python3.4/email/generator.py
# Helper used by Generator._make_boundary
_width = len(repr(sys.maxsize-1))
_fmt = '%%0%dd' % _width

def _make_boundary():
    # Craft a random boundary.
    token = random.randrange(sys.maxsize)
    boundary = ('=' * 15) + (_fmt % token) + '=='
    return boundary

class MultiPartForm(object):
    """Accumulate the data to be used when posting a form."""

    def __init__(self):
        self.form_fields = []
        self.files = []
        self.boundary = _make_boundary()
        return
    
    def get_content_type(self):
        return 'multipart/form-data; boundary=%s' % self.boundary

    def add_field(self, name, value):
        """Add a simple field to the form data."""
        if isinstance(name, bytes):
            name = name.decode('utf-8')
        if isinstance(value, bytes):
            value = value.decode('utf-8')
        self.form_fields.append((name, value))
        return

    def add_file(self, fieldname, filename, fileHandle, mimetype=None):
        """Add a file to be uploaded."""
        if isinstance(fieldname, bytes):
            fieldname = fieldname.decode('utf-8')
        if isinstance(filename, bytes):
            filename = filename.decode('utf-8')

        if hasattr(fileHandle, 'read'):
            body = fileHandle.read()
        else:
            body = fileHandle
        if mimetype is None:
            mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        self.files.append((fieldname, filename, mimetype, body))
        return

    def __str__(self):
        body = self.body()
        if not PY2:
            body = body.decode('utf-8')
        return body

    def body(self):
        """Return a byte string representing the form data, including attached files."""
        # Build a list of lists, each containing "lines" of the
        # request.  Each part is separated by a boundary string.
        # Once the list is built, return a string where each
        # line is separated by '\r\n'.  
        parts = []
        part_boundary = '--' + self.boundary
        
        # Add the form fields
        parts.extend(
            [ part_boundary,
              'Content-Disposition: form-data; name="%s"' % name,
              '',
              value,
            ]
            for name, value in self.form_fields
            )
        
        # Add the files to upload
        parts.extend(
            [ part_boundary,
              'Content-Disposition: file; name="%s"; filename="%s"' % \
                 (field_name, filename),
              'Content-Type: %s' % content_type,
              '',
              body,
            ]
            for field_name, filename, content_type, body in self.files
            )
        
        # Flatten the list and add closing boundary marker,
        # then return CR+LF separated data
        flattened = list(itertools.chain(*parts))
        flattened.append('--' + self.boundary + '--')
        flattened.append('')
        flattened = [part if isinstance(part, bytes) else part.encode('utf-8') for part in flattened]
        return b'\r\n'.join(flattened)

