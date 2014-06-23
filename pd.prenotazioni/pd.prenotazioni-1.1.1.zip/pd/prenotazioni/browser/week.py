# -*- coding: utf-8 -*-
from plone.memoize.view import memoize
from rg.prenotazioni.browser.week import View as BaseView


class View(BaseView):
    ''' Override rg.prenotazioni default behaviour
    '''
    @property
    @memoize
    def user_can_search(self):
        ''' States if the user can see the search button
        '''
        return self.user_can_view
