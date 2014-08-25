import unittest
import quant.soleInstance
from dm.view.testunit import ApiTestCase
from dm.view.testunit import TestCase
from quant.djangoapp.apps.eui.views.testbase import ViewTestCase
from quant.djangoapp.apps.eui.views.api import QuantApiView
from dm.webkit import HttpRequest
from dm.dictionarywords import SYSTEM_VERSION

def suite():
    suites = [
    #    unittest.makeSuite(TestApi),
        unittest.makeSuite(TestExchange),
        unittest.makeSuite(TestSymbol),
        unittest.makeSuite(TestMarket),
        unittest.makeSuite(TestImage),
        unittest.makeSuite(TestBook),
        unittest.makeSuite(TestDsl),
        unittest.makeSuite(TestResult),
    ]
    return unittest.TestSuite(suites)


class QuantApiTestCase(ApiTestCase):

    viewClass = QuantApiView
    apiKeyHeaderName = 'HTTP_X_QUANT_API_KEY'


class TestApi(QuantApiTestCase):

    def test_getResponse(self):
        self.setRequestPath('/')
        self.getResponse()
        self.failUnlessStatusCode(200)
        # Todo: Fix this to have verion and resources.
        #self.failUnlessData({'version': self.dictionary[SYSTEM_VERSION]})


class TestExchange(QuantApiTestCase):

    registerName = 'exchanges'
    newEntity = {'name': 'XXXX'}
    entityKey = 'XXXX'
    notFoundKey = 'ZZZZ'
    changedEntity = {'name': 'XXXXX'}
    updatedEntityKey = 'XXXXX'

    def tearDown(self):
        key = self.newEntity['name']
        if key in self.registry.exchanges:
            del(self.registry.exchanges[key])
        key = self.changedEntity['name']
        if key in self.registry.exchanges:
            del(self.registry.exchanges[key])
        super(TestExchange, self).tearDown()


class TestSymbol(QuantApiTestCase):

    registerName = 'symbols'
    newEntity = {'name': 'XX', 'exchange': 'http://kforge.dev.localhost/api/exchanges/NYMX'}
    entityKey = 'XX'
    notFoundKey = 'ZZ'
    changedEntity = {'name': 'XXX', 'exchange': 'http://kforge.dev.localhost/api/exchanges/NYMX'}
    updatedEntityKey = 'XXX'

    def tearDown(self):
        key = self.newEntity['name']
        if key in self.registry.symbols:
            del(self.registry.symbols[key])
        key = self.changedEntity['name']
        if key in self.registry.symbols:
            del(self.registry.symbols[key])
        super(TestSymbol, self).tearDown()

 
class TestMarket(QuantApiTestCase):

    registerName = 'markets'
    newEntity = {'symbol': 'http://kforge.dev.localhost/api/symbols/CL', 'expiration': '2015-01-01', 
        'firstDeliveryDate': '2015-01-01'}
    entityKey = '1'
    changedEntity = {'symbol': 'http://kforge.dev.localhost/api/symbols/HO', 'expiration': '2016-01-01', 
        'firstDeliveryDate': '2016-01-01'}


class TestImage(QuantApiTestCase):

    registerName = 'images'
    newEntity = {'priceProcess': 'http://kforge.dev.localhost/api/priceProcesses/1', 'observationTime': '2011-01-01 00:00:00'}
    entityKey = '1'
    changedEntity = {'priceProcess': 'http://kforge.dev.localhost/api/priceProcesses/1', 'observationTime': '2011-02-01 00:00:00'}

 
class TestBook(QuantApiTestCase):

    registerName = 'books'
    newEntity = {'title': 'Test'}
    entityKey = '1'
    changedEntity = {'title': 'Test2'}


class TestDsl(QuantApiTestCase):

    registerName = 'dsls'
    newEntity = {'specification':'Max(2, 3)', 'book': 'http://kforge.dev.localhost/api/books/1', 'title': 'Test'}
    entityKey = '1'
    changedEntity = {'specification':'4 * Max(2, 3)', 'book': 'http://kforge.dev.localhost/api/books/1', 'title': 'Test'}
    
    def setUp(self):
        super(TestDsl, self).setUp()
        self.book = self.registry.books.create()
        self.newEntity['book'] = 'http://kforge.dev.localhost/api/books/%s' % self.book.id

    def tearDown(self):
        self.book.delete()
        super(TestDsl, self).tearDown()


class TestResult(QuantApiTestCase):
    registerName = 'results'
    newEntity = {'book': 'http://kforge.dev.localhost/api/books/1', 'image': 'http://kforge.dev.localhost/api/images/1'}
    entityKey = '1'
    changedEntity = {'book': 'http://kforge.dev.localhost/api/books/1', 'image': 'http://kforge.dev.localhost/api/images/1'}
    
