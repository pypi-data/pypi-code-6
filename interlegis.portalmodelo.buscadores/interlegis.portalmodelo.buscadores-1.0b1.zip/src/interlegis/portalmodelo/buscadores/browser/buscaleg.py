# -*- coding: utf-8 -*-

from interlegis.portalmodelo.buscadores.browser.base import BaseView


class BuscaLegResults(BaseView):
    """Define the page used to return the results of the external search on
    the Buscador Legislativo site. The implementation is iframe-based on
    ``buscaleg.pt``.
    """

    base_url = 'http://busca.interlegis.leg.br/search?keywords=%s'
