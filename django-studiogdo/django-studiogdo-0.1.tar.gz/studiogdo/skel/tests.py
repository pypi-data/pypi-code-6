# -*- encoding: utf-8 -*-

from django.core.exceptions import SuspiciousOperation
from django.http.response import HttpResponse
from django.test import TestCase
from base64 import encodestring as encode
from mock import patch
from path import compose_path
from renderer import HTMLRenderer


class TestPath(TestCase):

    def test_compose(self):
        path = compose_path('', '')
        self.assertEqual(path, '')
        path = compose_path('a', '')
        self.assertEqual(path, 'a')
        path = compose_path('', 'b')
        self.assertEqual(path, 'b')
        path = compose_path('a', 'b')
        self.assertEqual(path, 'a/b')
        path = compose_path('a/b', 'c')
        self.assertEqual(path, 'a/b/c')
        path = compose_path('a', 'b/c')
        self.assertEqual(path, 'a/b/c')
        path = compose_path('a/b', 'c/d')
        self.assertEqual(path, 'a/b/c/d')
        path = compose_path('/', '/', '/')
        self.assertEqual(path, '/')
        path = compose_path('/a', '/b')
        self.assertEqual(path, '/b')
        path = compose_path('/', 'a')
        self.assertEqual(path, '/a')

    def test_compose_with_dot(self):
        path = compose_path('a', '.')
        self.assertEqual(path, 'a')
        path = compose_path('.', 'b')
        self.assertEqual(path, 'b')
        path = compose_path('a/./b', 'c/./d')
        self.assertEqual(path, 'a/b/c/d')
        path = compose_path('/', '.')
        self.assertEqual(path, '/')

    def test_compose_with_parent(self):
        path = compose_path('a/..', 'd/..')
        self.assertEqual(path, '')
        path = compose_path('a/b/..', 'c/d/..')
        self.assertEqual(path, 'a/c')
        path = compose_path('a/b/..', 'd/..')
        self.assertEqual(path, 'a')
        path = compose_path('a/..', 'd')
        self.assertEqual(path, 'd')
        with self.assertRaises(SuspiciousOperation):
            path = compose_path('../a')
        with self.assertRaises(SuspiciousOperation):
            path = compose_path('a', '../..')
        path = compose_path('a/b/c', '../..')
        self.assertEqual(path, 'a')


class TestRenderer(TestCase):

    @patch('studiogdo.api.StudiogdoApi')
    def test_renderer_text(self, mock_studiogdo):
        renderer = HTMLRenderer(mock_studiogdo, True)

        skel = '<div debug="/">test</div>'
        res = renderer.render('/', skel)

        self.assertEqual(res, skel)
        self.assertFalse(mock_studiogdo.called)

        mock_studiogdo.post_facet.return_value = HttpResponse("empty")
        skel = '<div data-cond="condition">test</div>'
        res = renderer.render('/', skel)

        self.assertEqual(res.strip(), "")
        self.assertFalse(mock_studiogdo.called)

    @patch('studiogdo.api.StudiogdoApi')
    def test_renderer_container(self, mock_studiogdo):
        renderer = HTMLRenderer(mock_studiogdo)

        mock_studiogdo.get_prop.return_value.content = "test"
        skel = "<span data-value='prop'></span>"
        res = renderer.render('/', skel)

        mock_studiogdo.get_prop.assert_called_once(encode("/prop"))
        self.assertRegexpMatches(res, 'test')

    @patch('studiogdo.api.StudiogdoApi')
    def test_renderer_container_and_child(self, mock_studiogdo):
        renderer = HTMLRenderer(mock_studiogdo)

        mock_studiogdo.get_prop.return_value.content = "test"
        mock_studiogdo.post_facet.return_value = HttpResponse("")
        skel = """<div data-path='path' data-value='prop'>
            <span data-value='prop'></span>
        </div>"""
        res = renderer.render('/', skel)

        mock_studiogdo.get_prop.assert_any_call(encode("/prop"))
        mock_studiogdo.get_prop.assert_any_call(encode("/path/prop"))
        self.assertRegexpMatches(res, 'test')
        self.assertRegexpMatches(res, 'span')

        mock_studiogdo.post_facet.return_value.content = "empty"
        skel = """<div data-path='path' data-value='prop'>
            <span data-value='prop'></span>
        </div>"""
        res = renderer.render('/', skel)

        self.assertTrue(mock_studiogdo.post_facet.called)
        mock_studiogdo.get_prop.assert_any_call(encode("/path/prop"))
        self.assertEqual(res, '')

    @patch('studiogdo.api.StudiogdoApi')
    def test_renderer_container_not(self, mock_studiogdo):
        renderer = HTMLRenderer(mock_studiogdo)

        mock_studiogdo.post_facet.return_value.content = "empty"
        skel = """<div data-path='!path'>
            test
        </div>"""
        res = renderer.render('/', skel)

        self.assertTrue(mock_studiogdo.post_facet.called)
        self.assertRegexpMatches(res, 'test')

        mock_studiogdo.post_facet.return_value.content = ""
        skel = """<div data-path='!path'>
            test
        </div>"""
        res = renderer.render('/', skel)

        self.assertTrue(mock_studiogdo.post_facet.called)
        self.assertRegexpMatches(res.strip(), '')

    @patch('studiogdo.api.StudiogdoApi')
    def test_renderer_final(self, mock_studiogdo):
        mock_studiogdo.get_prop.return_value.content = "test"

        renderer = HTMLRenderer(mock_studiogdo)
        skel = "<progress data-value='prop'></progress>"
        res = renderer.render('/', skel)

        mock_studiogdo.get_prop.assert_called_once(encode("/prop"))
        self.assertRegexpMatches(res, 'test')

    @patch('studiogdo.api.StudiogdoApi')
    def test_renderer_post(self, mock_studiogdo):
        mock_studiogdo.get_prop.return_value.content = "test"

        renderer = HTMLRenderer(mock_studiogdo)
        skel = """<input data-value='prop'/>
            <input data-value='prop%s' name="s_"/>
            <input data-value='prop%i'/>
        """
        res = renderer.render('/', skel)

        self.assertTrue(mock_studiogdo.get_prop.called)
        self.assertRegexpMatches(res, '_L3Byb3A=\n')

    @patch('studiogdo.api.StudiogdoApi')
    def test_renderer_select(self, mock_studiogdo):
        """
        http://localhost:8080/morassuti/html/facet.gdo?p=/Services(baches)&f=json&m={%22fixation%22%20:%20[{%22data-path%22:%20%22Fixation%22,%20%22data-value%22:%20{%22data-value%22:%20%22Nom%22}}]}
        """
        """
        {"fixation":["Sans","Colson/serflex blanc longueur 20cm","Colson/serflex noir longueur 20cm","Sandow/tendeur 1 crochets métal 20 cm","Sandow/tendeur 1 crochets métal 40 cm","Sandow/tendeur 2 crochets métal 20 cm","Sandow/tendeur 2 crochets métal 40 cm","Drisse polypro diam. 4 mm","Drisse élastique diam. 8 mm"]}
        """
        mock_studiogdo.get_prop.return_value.content = "Sans"
        mock_studiogdo.get_stencils.return_value.content = [{"Nom": "Sans", "Id": 0}, {"Nom": "Colson/serflex blanc longueur 20cm", "Id": 1}, {"Nom": "Colson/serflex noir longueur 20cm", "Id": 2}]
        renderer = HTMLRenderer(mock_studiogdo)
        skel = """<select data-value='Nom'>
            <option data-path='Fixation' data-value='Nom' />
            </select>
        """
        res = renderer.render('/', skel)

        self.assertRegexpMatches(res, 'Colson/serflex blanc')
        self.assertRegexpMatches(res, 'Colson/serflex noir')
        self.assertRegexpMatches(res, 's_L05vbQ==')
        self.assertRegexpMatches(res, 'option selected="selected" value="Sans"')

        skel = """<select data-label='Nom'>
            <option data-path='Fixation' data-value='Id' data-label='Nom' />
            </select>
        """
        res = renderer.render('/', skel)
        self.assertRegexpMatches(res, 'option selected="selected" value="0"')

        mock_studiogdo.get_prop.return_value.content = ""
        renderer = HTMLRenderer(mock_studiogdo)
        skel = """<select data-value='Nom'>
            <option value=''></option>
            <option value='1'></option>
            </select>
        """

        res = renderer.render('/', skel)
        self.assertRegexpMatches(res, 'option value=""')

    @patch('studiogdo.api.StudiogdoApi')
    def test_renderer_not_table(self, mock_studiogdo):
        renderer = HTMLRenderer(mock_studiogdo)

        mock_studiogdo.post_facet.return_value = HttpResponse("empty")
        mock_studiogdo.get_stencils.return_value.content = {"data-value": [{"Nom": "Sans", "Id": 0, "path": "Fixation(1)"}, {"Nom": "Colson/serflex blanc longueur 20cm", "Id": 1, "path": "Fixation(2)"}, {"Nom": "Colson/serflex noir longueur 20cm", "Id": 2, "path": "Fixation(3)"}]}
        skel = """<table data-path='!'>
            <thead><tr data-path='Fixation'>
                <th data-value='Id' />
                <th data-value='Nom' />
            </tr></thead>
            </table>
        """

        res = renderer.render('/', skel)
        self.assertRegexpMatches(res, '<tbody>')
        self.assertRegexpMatches(res, '<td>0</td><td>Sans</td>')

        mock_studiogdo.post_facet.return_value = HttpResponse("")
        skel = """<table data-path='!'>
            <thead><tr data-path='Fixation'>
                <th data-value='Id' />
                <th data-value='Nom' />
            </tr></thead>
            </table>
        """
        res = renderer.render('/', skel)
        self.assertRegexpMatches(res.strip(), '')

    @patch('studiogdo.api.StudiogdoApi')
    def test_renderer_table(self, mock_studiogdo):
        """
        http://localhost:8080/morassuti/html/facet.gdo?p=/Services(baches)&f=json&m={'fixation':[{%22data-path%22:%20%22Fixation%22,%20%22data-value%22:%20{%22data-value%22:%20%22Nom%22}}]}
                                                                                    {'DateLivraison':[{'data-path':'.', 'data-value':{'data-value':'DateLivraison'}}], 'SocieteFact':[{'data-path':'.', 'data-value':{'data-value':'SocieteFact'}}], 'PrixFactHT':[{'data-path':'.', 'data-value':{'data-value':'PrixFactHT'}}], 'prixFactTotalHT':[{'data-path':'.', 'data-value':{'data-value':'prixFactTotalHT'}}], 'ModePaiement':[{'data-path':'.', 'data-value':{'data-value':'ModePaiement'}}] }
        """
        """
        {"fixation":["Sans","Colson/serflex blanc longueur 20cm","Colson/serflex noir longueur 20cm","Sandow/tendeur 1 crochets métal 20 cm","Sandow/tendeur 1 crochets métal 40 cm","Sandow/tendeur 2 crochets métal 20 cm","Sandow/tendeur 2 crochets métal 40 cm","Drisse polypro diam. 4 mm","Drisse élastique diam. 8 mm"]}
        """
        renderer = HTMLRenderer(mock_studiogdo)

        mock_studiogdo.get_prop.return_value.content = "Sans"
        mock_studiogdo.get_stencils.return_value.content = []
        skel = """<table>
            <thead><tr data-path='Fixation'>
                <th data-value='Id' />
                <th data-value='Nom' />
            </tr></thead>
            </table>
        """
        res = renderer.render('/', skel)
        self.assertNotRegexpMatches(res, '<tbody>')

        mock_studiogdo.post_facet.return_value = HttpResponse("empty")
        skel = """<table data-path='.'>
            <thead><tr data-path='Fixation'>
                <th data-value='Id' />
                <th data-value='Nom' />
            </tr></thead>
            </table>
        """
        res = renderer.render('/', skel)
        self.assertEqual(res.strip(), '')

