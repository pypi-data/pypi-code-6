# -*- coding: utf-8 -*-

from interlegis.portalmodelo.policy.testing import FUNCTIONAL_TESTING
from plone.testing.z2 import Browser

import unittest


class FrontPageTestCase(unittest.TestCase):
    """Ensure site front page has all expected elements."""

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_main_navigation(self):
        browser = Browser(self.layer['app'])
        portal_url = self.portal.absolute_url()

        browser.open(portal_url)
        self.assertIn('Página Inicial', browser.contents)
        self.assertIn('Ouvidoria', browser.contents)
        self.assertIn('Transparência', browser.contents)
        self.assertIn('Perguntas frequentes', browser.contents)

    def test_navigation_portlets(self):
        browser = Browser(self.layer['app'])
        portal_url = self.portal.absolute_url()

        browser.open(portal_url)
        # Sobre a Câmara
        self.assertIn('navTreeItem visualNoMarker navTreeFolderish section-acesso', browser.contents)
        self.assertIn('navTreeItem visualNoMarker navTreeFolderish section-historia', browser.contents)
        self.assertIn('navTreeItem visualNoMarker navTreeFolderish section-funcao-e-definicao', browser.contents)
        self.assertIn('navTreeItem visualNoMarker navTreeFolderish section-estrutura', browser.contents)
        self.assertIn('navTreeItem visualNoMarker navTreeFolderish section-noticias', browser.contents)
        self.assertIn('navTreeItem visualNoMarker navTreeFolderish section-eventos', browser.contents)
        self.assertIn('navTreeItem visualNoMarker navTreeFolderish section-fotos', browser.contents)

        # Processo legislativo
        self.assertIn('navTreeItem visualNoMarker navTreeFolderish section-parlamentares', browser.contents)
        self.assertIn('navTreeItem visualNoMarker navTreeFolderish section-legislaturas', browser.contents)
        self.assertIn('navTreeItem visualNoMarker section-mesa-diretora', browser.contents)

        # Leis
        self.assertIn('navTreeItem visualNoMarker navTreeFolderish section-legislacao-municipal', browser.contents)
        self.assertIn('navTreeItem visualNoMarker navTreeFolderish section-lei-organica-municipal', browser.contents)
        self.assertIn('navTreeItem visualNoMarker navTreeFolderish section-lexml', browser.contents)

        # Transparência
        self.assertIn('navTreeItem visualNoMarker navTreeFolderish section-despesas', browser.contents)
        self.assertIn('navTreeItem visualNoMarker navTreeFolderish section-transferencias', browser.contents)
        self.assertIn('navTreeItem visualNoMarker navTreeFolderish section-receitas', browser.contents)
        self.assertIn('navTreeItem visualNoMarker navTreeFolderish section-acompanhamento', browser.contents)
        self.assertIn('navTreeItem visualNoMarker navTreeFolderish section-licitacoes', browser.contents)
        self.assertIn('navTreeItem visualNoMarker section-faq', browser.contents)

        # Links úteis
        self.assertIn('navTreeItem visualNoMarker section-prefeitura', browser.contents)
        self.assertIn('navTreeItem visualNoMarker section-diario-oficial', browser.contents)
        self.assertIn('navTreeItem visualNoMarker section-programa-interlegis', browser.contents)
        self.assertIn('navTreeItem visualNoMarker section-assembleia-estadual', browser.contents)
        self.assertIn('navTreeItem visualNoMarker section-camara-dos-deputados', browser.contents)
        self.assertIn('navTreeItem visualNoMarker section-senado-federal', browser.contents)

    def test_poll_portlet(self):
        browser = Browser(self.layer['app'])
        portal_url = self.portal.absolute_url()
        browser.open(portal_url)
        self.assertIn('Gostou do novo portal?', browser.contents)

    def test_social_networks_portlet(self):
        browser = Browser(self.layer['app'])
        portal_url = self.portal.absolute_url()
        browser.open(portal_url)
        self.assertIn('Redes sociais', browser.contents)

    def test_video_portlet(self):
        browser = Browser(self.layer['app'])
        portal_url = self.portal.absolute_url()
        browser.open(portal_url)
        # the portlet is there, but hidden
        self.assertNotIn('Sessões on-line', browser.contents)
