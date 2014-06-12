'''
Copyright 2012-2014 Ministerie van Sociale Zaken en Werkgelegenheid

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

from qualitylib.domain.measurement.measurable import MeasurableObject


class Document(MeasurableObject):
    ''' Class representing a document. '''

    def __init__(self, name, url=None, **kwargs):
        super(Document, self).__init__(**kwargs)
        self.__name = name
        self.__url = url

    def __str__(self):
        ''' Return the id string of the document. '''
        return self.id_string()

    def name(self):
        ''' Return the name of the document. '''
        return self.__name

    def id_string(self):
        ''' Return an id string for the document. '''
        return self.__name.lower().replace(' ', '_')

    def url(self):
        ''' Return the url of the document. '''
        return self.__url
