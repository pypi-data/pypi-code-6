# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from datetime import date
from plone.memoize.view import memoize
from pd.prenotazioni import prenotazioniMessageFactory as _
try:
    from collections import OrderedDict
except ImportError:
    from zope.schema.vocabulary import OrderedDict  # <py27


class Widget(BrowserView):
    ''' Widget to display same_day_booking_disallowed
    '''
    @property
    @memoize
    def today(self):
        ''' Return the value used for today date as %Y/%m/%d
        '''
        return date.today().strftime('%Y/%m/%d')

    @memoize
    def get_options(self, field):
        ''' Return the options for this widget
        '''
        options = OrderedDict(
            [
                ('yes', {'label': _('yes', u'Yes')}, ),
                ('no', {'label': _('no', u'No')},),
                (self.today, {'label': _('no_today', u'No, just for today')}),
            ]
        )
        value = field.get(self.context)
        if value in options:
            options[value]['selected'] = 'selected'
        else:
            options['yes']['selected'] = 'selected'
        return options

    @property
    @memoize
    def macros(self):
        """ Return the macros of our template
        """
        return self.index.macros
