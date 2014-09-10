# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from pd.prenotazioni.browser.prenotazione_add import (AddForm as BaseForm,
                                                      check_mobile_number)
from rg.prenotazioni.browser.prenotazione_add import IAddForm as IBaseForm
from plone.app.form.validators import null_validator
from plone.memoize.view import memoize
from rg.prenotazioni import prenotazioniMessageFactory as _
from rg.prenotazioni.utilities.urls import urlify
from zope.formlib.form import action, setUpWidgets, FormFields
from zope.interface import implements
from zope.schema import TextLine


class IAddForm(IBaseForm):
    ''' Customize fields for this add form
    '''
    add_view = TextLine(default=u'prenotazioni_add_ro')
    backurl = TextLine(default=u'http://example.com')


class AddForm(BaseForm):
    """ Customize pd.prenotazioni add form to redirect to another page
    """
    implements(IAddForm)
    template = ViewPageTemplateFile('prenotazione_add_ro.pt')

    banned_redirect_keys = (
        '_authenticator',
        'ajax_include_head',
        'ajax_load',
        'form..hashkey',
        'form.actions.book',
        'form.add_view',
        'form.backurl',
        'form.captcha',
        'form.tipology-empty-marker',
    )

    @property
    @memoize
    def label(self):
        ''' Override parents label
        '''
        return u''

    @property
    @memoize
    def form_fields(self):
        '''
        The fields for this form
        '''
        ff = FormFields(IAddForm)
        ff = ff.omit('captcha')
        ff['email'].field.required = False
        ff['mobile'].field.constraint = check_mobile_number
        return ff

    def setUpWidgets(self, ignore_request=False):
        '''
        From zope.formlib.form.Formbase.
        '''
        self.adapters = {}
        fieldnames = [x.__name__ for x in self.form_fields]
        data = {}
        for key in fieldnames:
            value = self.request.form.get(key)
            if value is not None and not value == u'':
                data[key] = value
                self.request[key] = value

        self.widgets = setUpWidgets(
            self.form_fields, self.prefix, self.context, self.request,
            form=self, adapters=self.adapters, ignore_request=ignore_request,
            data=data)

    @property
    @memoize
    def backurl(self):
        ''' We need an URL to redirect to

        This URL is passed as form.backurl
        if no form.backurl is given use http://example.com
        '''
        form = {}
        for key in self.request.form.copy():
            if not key in self.banned_redirect_keys:
                value = self.request.form[key]
                if isinstance(value, unicode):
                    value = value.encode('utf8')
                form[key] = value
        backurl = self.request.form.get('form.backurl', 'http://example.com/')
        return urlify(backurl, params=form)

    @action(_('action_book', u'Book'), name=u'book')
    def action_book(self, action, data):
        '''
        Book this resource
        '''
        obj = self.do_book(data)
        self.request.form['form.gate'] = obj.getGate()
        return self.request.response.redirect(self.backurl)

    @action(_(u"action_cancel", default=u"Cancel"), validator=null_validator, name=u'cancel')  # noqa
    def action_cancel(self, action, data):
        '''
        Cancel
        '''
        target = self.back_to_booking_url
        return self.request.response.redirect(target)
