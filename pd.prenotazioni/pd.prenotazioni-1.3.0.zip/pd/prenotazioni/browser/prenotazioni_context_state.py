# -*- coding: utf-8 -*-
from plone.memoize.view import memoize
from rg.prenotazioni.browser.prenotazioni_context_state import PrenotazioniContextState  # noqa


class PDPrenotazioniContextState(PrenotazioniContextState):
    ''' Override methods of prenotazioni context state
    '''
    @property
    @memoize
    def add_view(self):
        ''' We want to control the view that allows us to book stuff

        If the parameter form.add_view is not passed we just return
        the parent's one
        '''
        add_view = self.request.form.get('form.add_view', '')
        if isinstance(add_view, (list, tuple)) and len(add_view):
            add_view = add_view[0]
        if not add_view:
            add_view = PrenotazioniContextState.add_view
        return add_view

    @property
    @memoize
    def required_booking_fields(self):
        ''' Required booking field property that proxies the context one
        '''
        field = self.context.getField('required_booking_fields')
        value = field.get(self.context)
        return value

    @property
    @memoize
    def same_day_booking_allowed(self):
        ''' State if the same day booking is allowed
        '''
        field = self.context.getField('same_day_booking_disallowed')
        value = field.get(self.context)
        return value == 'no' or value == self.today.strftime('%Y/%m/%d')

    @property
    @memoize
    def first_bookable_day(self):
        ''' The first day when you can book stuff

        ;return; a datetime.date object
        '''
        if self.same_day_booking_allowed:
            return max(
                self.context.getDaData().asdatetime().date(),
                self.today
            )
        return super(PDPrenotazioniContextState, self).first_bookable_day

    @property
    @memoize
    def user_can_search(self):
        ''' States if the user can see the search button
        '''
        return self.user_can_view
