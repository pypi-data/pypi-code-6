# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from hashlib import md5
from pd.prenotazioni import prenotazioniMessageFactory as _
from plone.app.form.validators import null_validator
from plone.memoize.view import memoize
from rg.prenotazioni import prenotazioniMessageFactory as __
from rg.prenotazioni.browser.prenotazione_add import AddForm as RGAddForm
from rg.prenotazioni.utilities.urls import urlify
from zope.formlib.form import Fields, action
from zope.schema import TextLine, ValidationError
import re

TELEPHONE_PATTERN = re.compile(r'^3([0-9]| )*$')


class InvalidMobile(ValidationError):
    __doc__ = _("invalid_mobile_number", "Mobile phone number not valid")


def check_mobile_number(value):
    '''
    If value exist it should match TELEPHONE_PATTERN
    '''
    if not value:
        return True
    if isinstance(value, basestring):
        value = value.strip()
    if TELEPHONE_PATTERN.match(value) is not None:
        return True
    raise InvalidMobile(value)


class BaseForm(RGAddForm):
    """ Customize the rg.prenotazioni form
    """
    contact_details = ['phone', 'mobile', 'email']

    def get_data_checksum(self, data):
        """ Return a checksum based on the submitted data

        This is useful to get rid of the captcha in the confirm form
        """
        uid = self.context.UID()
        key = uid + data['booking_date'].strftime('%s')
        return md5(key).hexdigest()[:5].upper()

    def is_checksum_valid(self, data):
        """ Check if the data passed have the right checksum
        """
        observed_checksum = data.get('checksum', '')
        expected_checksum = self.get_data_checksum(data)
        return observed_checksum == expected_checksum

    def present_input_value(self, widget):
        """ Given a widget present its input value
        """
        if widget.name == "form.booking_date":
            return self.localized_time(widget.getInputValue(),
                                       long_format=True)
        return widget.getInputValue()

    @property
    @memoize
    def form_fields(self):
        '''
        This method adds mobile number validation to prenotazioni form
        '''
        ff = super(BaseForm, self).form_fields
        ff['email'].field.required = False
        ff['mobile'].field.constraint = check_mobile_number
        return ff

    def validate(self, action, data):
        '''
        Checks if we can book those data
        '''
        errors = super(BaseForm, self).validate(action, data)
        if not any([data.get(key, False) for key in self.contact_details]):
            msg = _('contact_details_error',
                    u'You have to provide at least one of these fields: '
                    u'email, phone, mobile')
            self.set_invariant_error(errors, self.contact_details, msg)
        return errors


class AddForm(BaseForm):
    """ Customized add form

    It submits to a confirm form
    """
    def get_confirm_url(self, data):
        ''' The URL that send to the confirm form
        '''
        request_form = self.request.form
        params = {}
        for key in request_form.keys():
            if (
                key.startswith('form.')
                and (not key.startswith('form.actions.'))
            ):
                value = request_form[key]
                if isinstance(value, unicode):
                    value = value.encode('utf8')
                params[key] = value
        params["form.checksum"] = self.get_data_checksum(data)

        return urlify(
            self.context.absolute_url(),
            '@@prenotazione_confirm',
            params=params
        )

    @action(__('action_book', u'Book'), name=u'book')
    def action_book(self, action, data):
        ''' Book this resource
        '''
        if self.is_anonymous:
            return self.request.response.redirect(self.get_confirm_url(data))
        else:
            return super(AddForm, self).action_book.success_handler(self,
                                                                    action,
                                                                    data)

    @action(_(u"action_cancel", default=u"Annulla"),
            validator=null_validator, name=u'cancel')
    def action_cancel(self, action, data):
        '''
        Cancel
        '''
        target = self.back_to_booking_url
        return self.request.response.redirect(target)


class ConfirmForm(BaseForm):
    """ The confirm form wants a checksum
    """
    template = ViewPageTemplateFile('prenotazione_confirm.pt')
    label = _(
        'booking_to_be_confirmed',
        u"Prenotazione da confermare"
    )
    description = _(
        'booking_confirmation_help',
        u"We assigned you a booking time. "
        u"Please review your data before confirming your booking"
    )

    def validate(self, action, data):
        '''
        Checks if we can book those data
        '''
        errors = super(ConfirmForm, self).validate(action, data)
        if self.is_anonymous:
            if not self.is_checksum_valid(data):
                msg = _('checksum_error', u'Invalid checksum')
                self.set_invariant_error(errors, ['checksum'], msg)
        return errors

    @property
    @memoize
    def form_fields(self):
        '''
        This method adds mobile number validation to prenotazioni form
        '''
        ff = super(ConfirmForm, self).form_fields
        ff = ff.omit('captcha')
        if self.is_anonymous:
            ff = ff + Fields(
                TextLine(
                    __name__='checksum',
                    title=_('verification_code', u"Verification code")
                )
            )
        return ff

    @action(_('action_confirm', u'Conferma'), name=u'book')
    def action_book(self, action, data):
        ''' Book this resource
        '''
        return (
            super(ConfirmForm, self)
            .action_book
            .success_handler(self, action, data)
        )

    @action(_(u"action_cancel", default=u"Annulla"),
            validator=null_validator, name=u'cancel')
    def action_cancel(self, action, data):
        '''
        Cancel
        '''
        target = self.back_to_booking_url
        return self.request.response.redirect(target)
