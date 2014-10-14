# Copyright 2013-2014 Flavio Garcia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import httplib
import os
from urlparse import urlparse
import urllib2


def exists(url):
    """ Checks if an url exists.
    """
    host = urlparse(url).netloc
    conn = httplib.HTTPConnection(host)
    conn.request('HEAD', url)
    response = conn.getresponse()
    conn.close()
    return response.status == 200


def download_to_path(url, path_to):
    """ Downloads a given url to the a path.
    """
    parsed_url = urlparse(url)
    url_path = parsed_url.path
    file_name = url_path.split('/')[-1]
    
    download_file = os.path.join(path_to, file_name)

    response = urllib2.urlopen(url)

    # Open the file for wirting and reading it from request 
    # while writing it to the file
    with open(download_file, 'w') as f: f.write(response.read())
