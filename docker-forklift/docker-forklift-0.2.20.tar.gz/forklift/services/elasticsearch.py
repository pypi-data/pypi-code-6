#
# Copyright 2014  Infoxchange Australia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Elasticsearch service.
"""

import json
import urllib.request
from os.path import join

from .base import ensure_container, Service, pipe_split, register


@register('elasticsearch')
class Elasticsearch(Service):
    """
    Elasticsearch service for the application.
    """

    allow_override = ('index_name', 'host')
    allow_override_list = ('urls',)

    def __init__(self, index_name, urls):
        self.index_name = index_name
        self._url_array = []
        self.urls = urls

    def environment(self):
        """
        The environment to access Elasticsearch.
        """

        return {
            'ELASTICSEARCH_INDEX_NAME': self.index_name,
            'ELASTICSEARCH_URLS': self.url_string(),
        }

    def url_string(self):
        """
        All URLs joined as a string.
        """
        return '|'.join(url.geturl() for url in self.urls)

    @property
    def urls(self):
        """
        The (pipe separated) URLs to access Elasticsearch at.
        """

        return self._url_array

    @urls.setter
    def urls(self, urls):
        """
        Set the URLs to access Elasticsearch at.
        """

        self._url_array = [
            urllib.parse.urlparse(url) if isinstance(url, str) else url
            for url in pipe_split(urls)
        ]

    @property
    def host(self):
        """
        The (pipe separated) hosts for the Elasticsearch service.
        """

        return '|'.join(url.hostname for url in self._url_array)

    @host.setter
    def host(self, host):
        """
        Set the host to access Elasticsearch at.
        """

        self.urls = [
            # pylint:disable=protected-access
            url._replace(
                netloc='{host}:{port}'.format(host=host, port=url.port))
            for url in self.urls
        ]

    def available(self):
        """
        Check whether Elasticsearch is available at a given URL.
        """

        if not self.urls:
            return False

        for url in self.urls:
            try:
                es_response = urllib.request.urlopen(url.geturl())
                es_status = json.loads(es_response.read().decode())
                if es_status['status'] != 200:
                    return False
            except (urllib.request.URLError, ValueError):
                return False

        return True

    @classmethod
    def localhost(cls, application_id):
        """
        The Elasticsearch environment on the local machine.
        """
        return cls(index_name=application_id,
                   urls=('http://localhost:9200',))

    @classmethod
    def container(cls, application_id):
        """
        Elasticsearch provided by a container.
        """

        container = ensure_container(
            image='dockerfile/elasticsearch',
            port=9200,
            application_id=application_id,
            data_dir='/data',
        )

        config_path = join(container.data_dir, 'elasticsearch.yml')
        with open(config_path, 'w') as config:
            print(
                """
                path:
                    data: /data/data
                    logs: /data/log
                """,
                file=config,
            )

        return cls(
            index_name=application_id,
            urls=('http://localhost:{0}'.format(container.port),),
        )

    providers = ('localhost', 'container')
