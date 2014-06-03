# -*- coding: utf-8 -*-

# Copyright (c) 2012-2014 CoNWeT Lab., Universidad Politécnica de Madrid

# This file is part of Wirecloud.

# Wirecloud is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Wirecloud is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with Wirecloud.  If not, see <http://www.gnu.org/licenses/>.

import codecs
import platform
import requests
from urlparse import urlparse

import wirecloud.platform


VERSIONS = {
    'wirecloud_version': wirecloud.platform.__version__,
    'system': platform.system(),
    'machine': platform.machine(),
    'requests_version': requests.__version__,
}


def download_local_file(path):

    f = codecs.open(path, 'rb')
    contents = f.read()
    f.close()

    return contents


def download_http_content(url, user=None):

    parsed_url = urlparse(url)
    if parsed_url.scheme not in ('http', 'https'):
        return ''

    headers = {
        'User-Agent': 'Mozilla/5.0 (%(system)s %(machine)s;U) Wirecloud/%(wirecloud_version)s python-requests/%(requests_version)s' % VERSIONS,
        'Accept': '*/*',
        'Accept-Language': 'en-gb,en;q=0.8,*;q=0.7',
        'Accept-Charset': 'utf-8;q=1,*;q=0.2',
    }

    if user and not user.is_anonymous():
        headers.update({
            'Remote-User': user.username,
        })

    return requests.get(url, headers=headers).content
