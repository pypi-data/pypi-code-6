import unittest
import mock
from wireframe2html import *
from xml.dom.minidom import Element
import jinja2

class TestWireframe2html(unittest.TestCase):

    def setUp(self):
        pass

    def test_attribute2param(self):
        element = Element('cbrun')
        element.setAttribute('href','http://site.free.fr')
        element.setAttribute('style','bien')
        self.assertItemsEqual(attribute2param(element),{'href':'http://site.free.fr', 'style':'bien'})

    def test_get_table_header(self):
        data =  "header1,header2,header3\nvalue1,value2,value3\nautrevalue1,autrevalue2,autrevalue3"
        self.assertItemsEqual(get_table_header(data),['header1','header2','header3'])

    def test_get_table_lignes(self):
        data =  "header1,header2,header3\nvalue1,value2,value3\nautrevalue1,autrevalue2,autrevalue3"
        self.assertItemsEqual(get_table_lignes(data),['value1,value2,value3','autrevalue1,autrevalue2,autrevalue3'])

    def test_get_table_ligne_value(self):
        data="value1,value2,value3"
        self.assertItemsEqual(get_table_ligne_value(data),['value1','value2','value3'])

    def test_hasoverride(self):
        domDocument = Element('test')
        child = Element('overrides')
        domDocument.appendChild(child)
        self.assertTrue(hasoverride(domDocument))
        domDocument = Element('autre_test')
        child = Element('autre_child')
        domDocument.appendChild(child)
        self.assertFalse(hasoverride(domDocument))

    def test_mreplace(self):
        string = "Bonjour le #monde, et les @autres &"
        replacement1 = {'&':'',}
        self.assertEquals(mreplace(replacement1,string),"Bonjour le #monde, et les @autres ")
        replacement2 = {'&':'', '#':'-', ' ':'_', '@':'', ',':''}
        self.assertEquals(mreplace(replacement2,string),"Bonjour_le_-monde_et_les_autres_")
        string = "%20avec un autre caractere"

    
    @mock.patch('wireframe2html.handleWidgets')
    def test_handleModelScreen(self, mock_handleWidgets):
        domDocument = Element('root')
        child = Element(u'widgets')
        domDocument.appendChild(child)
        childlist = []
        childlist.append(child)
        handleModelScreen(domDocument, '')
        mock_handleWidgets.assert_has_call([
            mock.call(childlist)
            ])

    @mock.patch('wireframe2html.handleScreen')
    @mock.patch('wireframe2html.handleOverrides')
    @mock.patch('jinja2.Environment.get_template')
    def test_handleWidgets(self, mock_handleScreen, mock_handleOverrides,mock_get_template):
        # Sans overrides
        domDocument = Element(u'widgets')
        domDocument.setAttribute('xsi:type','model:Master')
        child = Element('screen')
        domDocument.appendChild(child)
        handleWidgets(domDocument, jinja2.Environment())
        mock_handleScreen.assert_has_call([
            mock.call([child,])
            ])
        mock_get_template.assert_has_call([
            mock.call()
            ])
        # Avec overrides
        child = Element('overrides')
        domDocument.appendChild(child)
        handleWidgets(domDocument, jinja2.Environment())
        mock_handleOverrides.assert_has_call([
            mock.call([child,])
            ])


    @mock.patch('jinja2.Environment.get_template')
    def test_handleScreen(self, mock_get_template):
        element = Element('screen')
        handleScreen([element,], jinja2.Environment(), None)
        mock_get_template.assert_has_call([
            mock.call()
            ])


    @mock.patch('wireframe2html.handleWidgetOverrides')
    def test_handleOverrides(self, mock_handleWidgetOverrides):
        domDocument = Element('overrides')
        child = Element('widgets')
        domDocument.appendChild(child)
        handleOverrides([domDocument,])
        mock_handleWidgetOverrides.assert_has_call([
            mock.call(child)
            ])

    @mock.patch('wireframe2html.attribute2param')
    @mock.patch('wireframe2html.handleItems')
    def test_handleWidgetOverrides(self, mock_attribute2param, mock_handleItems):
        element = Element('test')
        handleWidgetOverrides(element)
        mock_attribute2param.assert_has_call([
            mock.call(element)
            ])
        mock_handleItems.assert_has_call([
            mock.call(element)
            ])

    @mock.patch('wireframe2html.attribute2param')
    def test_handleItems(self, mock_attribute2param):
        element = Element('test')
        child = Element('items')
        element.appendChild(child)
        handleItems(element)
        mock_attribute2param.assert_has_call([
            mock.call(element)
            ])




