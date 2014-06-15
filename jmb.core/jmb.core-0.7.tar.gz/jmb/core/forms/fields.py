from django.conf import settings
from django import forms
from django.core.validators import validate_email
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _
from django.core.validators import EMPTY_VALUES

from jmb.core.forms.widgets import DateWidget
from jmb.core.forms import DateWidget

class JumboDateField(forms.DateField):
    widget = DateWidget

class ChainedChoiceField(forms.ChoiceField):
    def __init__(self, choices=(), model=None, required=True, widget=None, label=None,
                 initial=None, help_text=None, *args, **kwargs):
        super(ChainedChoiceField, self).__init__(choices=choices, required=required,
                                                widget=widget, label=label,
                                                initial=initial, help_text=help_text,
                                                *args, **kwargs)
        self.model = model

    def to_python(self, value):
        if value in EMPTY_VALUES:
            return None

        if not self.model:
            return value

        try:
            value = self.model.objects.get(**{'pk': value or None})
        except self.model.DoesNotExist:
            raise forms.ValidationError(self.error_messages['invalid_choice'] % {'value': value})
        return value

    def validate(self, value):
        """
        Validates that the input is in self.choices.
        """
        if self.required and not value:
            raise forms.ValidationError(self.error_messages['invalid_choice'] % {'value': value})


class MultiEmailField(forms.Field):
    widget = forms.Textarea

    def to_python(self, value):
        "Normalize data to a list of strings."

        # Return an empty list if no input was given.
        if not value:
            return []

        # Dato che uso una text area le mail possono essere separate
        # da un invio. In caso di invio il value che mi arriva invece di
        # essere una lista di indirizzi mail e' una stringa cosi' composta:
        # [u'mminutoli@thundersystems.it\r\nmminut@thunder.it']
        # In questo modo mi ricostruisco la lista di indirizzi correttamente.
        #
        all_mails = []
        emails = value.split('\r\n')
        for e in emails:
            for email in e.split(','):
                all_mails.append(email.strip())

        return all_mails


    def validate(self, value):
        "Check if value consists only of valid emails."
        # Use the parent's handling of required fields, etc.
        super(MultiEmailField, self).validate(value)

        for email in value:
            validate_email(email)

