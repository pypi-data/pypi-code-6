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

import unittest
from qualitylib import metric, domain
from qualitylib.report import Section


class FakeSonar(object):
    ''' Provide for a fake Sonar object so that the unit test don't need 
        access to an actual Sonar instance. '''
    # pylint: disable=unused-argument
            
    @staticmethod
    def dashboard_url(*args):  
        ''' Return a fake dashboard url. '''
        return 'http://sonar'
          
    @staticmethod
    def package_cycles(*args):
        ''' Return the number of package cycles. '''
        return 1
    
        
class FakeSubject(object):
    ''' Provide for a fake subject. '''
    
    @staticmethod
    def short_name():
        ''' Return the short name of the subject. '''
        return 'FS'
    
    @staticmethod
    def sonar_id():
        ''' Return the Sonar id of the subject. '''
        return ''
           
    @staticmethod  # pylint: disable=unused-argument
    def dependencies(**kwargs):
        ''' Return the dependencies of the subject. '''
        return [('product_name', 'product_version')]

    
class FakeReport(object):
    ''' Fake a quality report. '''
    @staticmethod
    def get_product_section(product_name, product_version):
        # pylint: disable=unused-argument
        ''' Return the section for the product/version. '''
        return Section('', [])

    @staticmethod
    def products():
        ''' Return the products of the project. '''
        return [FakeSubject(), FakeSubject()]
    
    @staticmethod
    def get_product(product, version):  # pylint: disable=unused-argument
        ''' Return the specified product. '''
        return FakeSubject()


class DependencyQualityTest(unittest.TestCase):
    # pylint: disable=too-many-public-methods
    ''' Unit tests for the dependency quality metric. '''
    def setUp(self):  # pylint: disable=invalid-name
        self.__subject = FakeSubject()
        project = domain.Project()
        self.__metric = metric.DependencyQuality(subject=self.__subject, 
                                                 report=FakeReport(),
                                                 project=project)

    def test_value(self):
        ''' Test that the value of the metric equals the percentage of 
            dependencies without red metrics. '''
        self.assertEqual(0, self.__metric.value())
        
    def test_report(self):
        ''' Test that the report is correct. '''
        self.assertEqual('0% van de afhankelijkheden (0 van de 2) is naar ' \
                         'componenten die "rode" metrieken hebben.', 
                         self.__metric.report())

    def test_url(self):
        ''' Test that the url contains the "red" products. '''
        self.assertEqual({'product_name:product_version':
                          'index.html#section_FS'}, self.__metric.url())
        
    def test_url_label(self):
        ''' Test that the url label is correct. '''
        self.assertEqual('Componenten die "rode" metrieken hebben',
                         self.__metric.url_label())


class CyclicDependenciesTest(unittest.TestCase):
    # pylint: disable=too-many-public-methods
    ''' Unit tests for the cyclic dependencies metric. '''

    def setUp(self):  # pylint: disable=invalid-name
        self.__subject = FakeSubject()
        project = domain.Project(sonar=FakeSonar())
        self._metric = metric.CyclicDependencies(subject=self.__subject,
                                                 project=project)

    def test_value(self):
        ''' Test that the value of the metric equals the number of cyclic 
            dependencies between packages. '''
        self.assertEqual(FakeSonar().package_cycles(), self._metric.value())

    def test_url(self):
        ''' Test that the url is correct. '''
        self.assertEqual(dict(Sonar=FakeSonar().dashboard_url()), 
                         self._metric.url())
