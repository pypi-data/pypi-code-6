# -*- coding: utf-8 -*-

from interlegis.portalmodelo.buscadores.browser.base import BaseView


class LexMLResults(BaseView):
    """Define the page used to return the results of the external search on
    the LexML Brasil site. The implementation is iframe-based on ``lexml.pt``.
    """
    base_url = 'http://www.lexml.gov.br/busca/search?keyword=%s'
