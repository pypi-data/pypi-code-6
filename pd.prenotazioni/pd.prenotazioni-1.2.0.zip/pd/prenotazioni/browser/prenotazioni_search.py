# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from rg.prenotazioni.browser.prenotazioni_search import SearchForm as BaseSearchForm  # noqa


class SearchForm(BaseSearchForm):
    """ Customize the rg.prenotazioni search form
    """
    template = ViewPageTemplateFile('prenotazioni_search.pt')

    review_state_map = {
        'pending': 'In attesa',
        'private': 'Private',
        'published': 'Confermato',
        'refused': 'Rifiutato',
    }

    def get_review_state_hr(self, item):
        rs = item.review_state
        return self.review_state_map.get(rs, rs)
