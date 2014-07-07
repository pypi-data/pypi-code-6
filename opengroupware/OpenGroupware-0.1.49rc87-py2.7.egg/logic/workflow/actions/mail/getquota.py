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
from lxml import etree
from coils.foundation.api import elementflow
import imaplib
import re
from coils.core import \
    CoilsException, \
    get_yaml_struct_from_project7000, \
    ServerDefaultsManager
from coils.core.logic import ActionCommand


RE_QUOTA_PATTERN = re.compile('\d+')


class GetIMAPQuotaAction(ActionCommand):
    __domain__ = "action"
    __operation__ = "get-imap-quota"
    __aliases__ = ['getIMAPQuota', 'getIMAPQuotaAction', ]

    def __init__(self):
        ActionCommand.__init__(self)

    @property
    def result_mimetype(self):
        return 'application/xml'

    def do_action(self):

        folder_list = dict()

        doc = etree.parse(self.rfile)
        nsmap = doc.getroot().nsmap
        if None in nsmap:
            nsmap['default'] = nsmap[None]
            nsmap.pop(None)
        result = doc.xpath(self._xpath, namespaces=nsmap)
        if isinstance(result, list):
            for tmp_value in result:
                if (tmp_value, basestring):
                    box_path = '{0}{1}'.format(
                        self._mailbox_path_prefix, tmp_value,
                    )
                    folder_list[box_path] = (0.0, 0.0, 0.0, )

        server = imaplib.IMAP4(self._hostname)
        server.login(self._username, self._password)
        for box_path in folder_list.keys():
            quota_string = server.getquotaroot(box_path)
            try:
                quota_info = RE_QUOTA_PATTERN.findall(quota_string[1][1][0])
            except TypeError:
                quota_info = set()
            if len(quota_info) == 2:
                consumed = float(quota_info[0]) / 1024.0
                quota_limit = float(quota_info[1]) / 1024.0
                percentage = 0.0
                if quota_limit:
                    percentage = (consumed / quota_limit) * 100.0
                folder_list[box_path] = (consumed, quota_limit, percentage, )
        server.logout()

        with elementflow.xml(self.wfile, u'ResultSet',
                             attrs={
                                 'format': 'imapQuotaReport',
                                 'version': '1.0',
                             },) as xml:
            for key, value, in folder_list.items():
                with xml.container(u'row'):
                    xml.element(
                        'mailboxPath',
                        text=key,
                        attrs={'dataType': 'string', }
                    )
                    xml.element(
                        'kilobytesConsumed',
                        text=unicode(value[0]),
                        attrs={'dataType': 'float', }
                    )
                    xml.element(
                        'kilobytesLimit',
                        text=unicode(value[1]),
                        attrs={'dataType': 'float', }
                    )
                    xml.element(
                        'percentConsumed',
                        text=unicode(value[2]),
                        attrs={'dataType': 'float', },
                    )

    def parse_action_parameters(self):

        credentials = get_yaml_struct_from_project7000(
            self._ctx, '/Credentials.yaml', access_check=True,
        )

        self._hostname = self.process_label_substitutions(
            self.action_parameters.get(
                'imapServer',
                self._ctx.server_defaults_manager.string_for_default(
                    'imap_host', 'localhost',
                )
            )
        )

        self._username = credentials['imap'][self._hostname]['username']
        self._password = credentials['imap'][self._hostname]['password']

        self._xpath = self.process_label_substitutions(
            self.action_parameters.get('xpath', )
        )

        self._mailbox_path_prefix = self.process_label_substitutions(
            self.action_parameters.get(
                'mailboxPathPrefix', '',
            )
        )
