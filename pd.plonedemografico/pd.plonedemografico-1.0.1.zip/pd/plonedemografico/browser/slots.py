# -*- coding: utf-8 -*-
from DateTime import DateTime
from Products.Five.browser import BrowserView
from json import dumps, JSONEncoder
from plone import api
from plone.memoize.view import memoize
from rg.prenotazioni.adapters.slot import BaseSlot
from rg.prenotazioni.utilities.urls import urlify


class SlotAwareEncoder(JSONEncoder):
    ''' Return an Encoder that knows about slots
    '''
    def default(self, obj):
        if isinstance(obj, BaseSlot):
            return obj.start()
        return super(SlotAwareEncoder, self).default(obj)


class View(BrowserView):
    ''' Return tipologies jsonified
    '''
    @property
    @memoize
    def prenotazioni(self):
        ''' The prenotazioni_context_state view
        '''
        return api.content.get_view('prenotazioni_context_state',
                                    self.context,
                                    self.request)

    @property
    @memoize
    def booking_date(self):
        ''' Compute the booking date as passed in the request
        '''
        booking_date = self.request.form.get('booking_date', DateTime())
        if not booking_date:
            return []
        if isinstance(booking_date, basestring):
            booking_date = DateTime(booking_date)
        return booking_date.asdatetime().date()

    @property
    @memoize
    def additional_parameters(self):
        ''' Get some additional parameteres
        '''
        params = self.request.form.copy()
        params.pop('booking_date', '')
        return urlify(params=params)

    def get_url_lists(self):
        ''' Return the urls for this booking date
        '''
        day = self.booking_date
        tipology = self.request.form.get('form.tipology', '')
        prenotazioni = self.prenotazioni
        duration = prenotazioni.get_tipology_duration(tipology) * 60
        booking_urls = prenotazioni.get_all_booking_urls(day, slot_min_size=duration)  # noqa
        additional_parameters = self.additional_parameters
        return ["%s&%s" % (url['url'], additional_parameters)
                for url in booking_urls]

    def __call__(self):
        '''
        '''
        self.request.response.setHeader('Content-Type', 'application/json')
        url_lists = self.get_url_lists()
        return dumps(url_lists, cls=SlotAwareEncoder)
