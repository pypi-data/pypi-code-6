#
# Copyright (c) 2012, 2014
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
import traceback
from email import Encoders
from email.Utils import formatdate
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.mime.text import MIMEText
from lxml.etree import XSLTParseError
from coils.core import SMTP, CoilsException
from coils.net import DAVFolder
from xsltobject import XSLTObject
from coils.logic.workflow import XSLTDocument


class XSLTFolder(DAVFolder):
    def __init__(self, parent, name, **params):
        DAVFolder.__init__(self, parent, name, **params)

    def supports_PUT(self):
        return True

    def _load_contents(self):
        for name in XSLTDocument.List():
            try:
                xslt = XSLTDocument.Marshall(name)
            except Exception as exc:
                # TODO: Raise an administrative notice. (see Issue#149)
                pass
            else:
                self.insert_child(
                    name,
                    XSLTObject(
                        self,
                        name,
                        entity=xslt,
                        context=self.context,
                        request=self.request,
                    )
                )
        return True

    def do_PUT(self, request_name):
        '''
        Allows tables to be created by dropping XSLT documents
        into /dav/Workflow/XSLT
        '''
        print 'PUT', request_name
        payload = self.request.get_request_payload()
        # TODO: Verify that payload is XSD data
        xsd = XSLTDocument.Marshall(request_name)
        try:
            xsd.fill(data=payload)
        except XSLTParseError as exc:
            if self.context.email:
                '''
                TODO: Take this out of band!  Otherwise a hung SMTP connection
                can tie up an HTTP worker.
                '''
                subject = \
                    'XSLT Parse Error Saving "{0}"'.format(request_name, )
                message = MIMEMultipart()
                message.attach(
                    MIMEText(
                        traceback.format_exc(),
                    )
                )
                attachment = MIMEBase('text', 'plain')
                attachment.set_payload(payload)
                attachment.add_header(
                    'Content-Disposition',
                    'attachment; filename="{0}"'.format(request_name, ),
                )
                Encoders.encode_base64(attachment)
                message.attach(attachment)
                message['Subject'] = subject
                message['From'] = ''
                message['To'] = self.context.email
                message['Date'] = formatdate(localtime=True)
                SMTP.send('', [self.context.email, ], message)
                self.log.info('Message sent to administrator.')
            raise exc
        else:
            xsd.close()
            self.context.commit()
            self.request.simple_response(201)

    def do_DELETE(self, request_name):
        if self.load_contents():
            if self.has_child(request_name):
                xslt = self.get_child(request_name)
                xslt.entity.delete()
                self.request.simple_response(
                    204,
                    data=None,
                    mimetype='application/xml',
                    headers={},
                )
                return
            else:
                self.no_such_path()
        else:
            raise CoilsException('Unable to enumerate collection contents.')
