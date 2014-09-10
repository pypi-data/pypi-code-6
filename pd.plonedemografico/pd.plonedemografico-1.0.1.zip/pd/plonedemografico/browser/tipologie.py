# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from json import dumps
from plone import api


class View(BrowserView):
    ''' Return tipologies jsonified
    '''

    def __call__(self):
        '''
        '''
        prenotazioni = api.content.get_view('prenotazioni_context_state',
                                            self.context,
                                            self.request)
        tipologies = prenotazioni.tipology_durations
        self.request.response.setHeader('Content-Type', 'application/json')
        return dumps(tipologies)
