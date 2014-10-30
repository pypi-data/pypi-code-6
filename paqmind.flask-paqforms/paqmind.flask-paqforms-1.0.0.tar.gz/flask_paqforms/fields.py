import os.path as op; __dir__ = op.dirname(__file__)
import flask

from flask.ext.babel import get_locale, get_timezone, lazy_gettext as _l
from babel.support import NullTranslations

from paqforms import *
from paqforms.bootstrap import *

from .validators import *


nt = NullTranslations()


class Form(BaseForm):
    def __init__(self,
        model,
        data = {},
        default = lambda: {},
        submit = None,
        locale = None,
        translations = nt,
        meta = {},
        name = None
    ):
        locale = locale or get_locale()
        BaseForm.__init__(self, model, data, default, submit, locale, translations, meta, name)


    def feed(self, model, data={}, submit=None):
        if self.is_multidict(data):
            data = variable_decode(data)
        if submit is None:
            try:
                submit = flask.request.method in {'POST', 'PUT', 'DELETE'}
            except Exception: # TODO think how to deal with working outside of request context (remove FormField shortcuts?)
                submit = False
        return BaseForm.feed(self, model, data, submit)


    def is_multidict(self, data):
        return hasattr(data, 'getlist')


class FilterForm(Form): # with auto-eval of submit for now
    meta = {'name': 'filters'}


class SortForm(BaseForm): # no auto-eval of submit
    meta = {'name': 'sorts'}


class RecaptchaField(Field):
    """
    TODO: works only on top-level-forms for now
    """
    def __init__(self, widget, publickey, privatekey, default=None, required=lambda: True, name=None):
        widget = Widget(
            widget,
            template = 'RecaptchaWidget.html',
            template_dirs = [op.join(__dir__, 'bootstrap/templates')] + SelectWidget.template_dirs
        ) if isinstance(widget, str) else widget
        Field.__init__(self, widget, default, required, validators=[RecaptchaValidator()], name=name)
        self.publickey = publickey
        self.privatekey = privatekey


    # HIGH-LEVEL API
    def feed(self, value=None, data=None, submit=False):
        if submit is True:
            if self.required():
                try:
                    feed_data = self.master().feed_data
                    data = {
                        'challenge': feed_data['recaptcha_challenge_field'],
                        'response': feed_data['recaptcha_response_field'],
                    }
                except Exception:
                    data = None
            else:
                data = None
        return Field.feed(self, value, data, submit)


# SHORTCUTS ====================================================================
def SortField(widget):
    return ChoiceField(
        SelectWidget(widget, options=[''] + list(map(_l, SORT_OPTIONS))), # TODO как запустить lazy_load с подгрузкой переводов ОТСЮДА???
        choices = [None] + SORT_OPTIONS,
    )


def PhoneField(widget='Phone', default=None, required=False, meta={}, name=None):
    return TextField(
        widget = widget,
        default = default,
        required = required,
        converters = [StrConverter(), CutNonNumConverter()],
        validators = LengthValidator(max=18),
        meta = meta,
        name = name
    )


def PriceField(widget='Phone', default=None, required=False, meta={}, name=None):
    return TextField(
        widget = widget,
        default = default,
        required = required,
        converters = DecimalConverter(),
        validators = ValueValidator(min=0),
        meta = meta,
        name = name
    )


SORT_OPTIONS = ['asc', 'desc']
ACCESS_FIELD_OPTIONS = ['private', 'friends', 'public']
ACCESS_WIDGET_OPTIONS = [(_l('private'), {'class': 'fa fa-left fa-lock'}), (_l('friends'), {'class': 'fa fa-left fa-users'}), (_l('public'), {'class': 'fa fa-left fa-globe'})]


def AccessField(default='private', required=True):
    return ChoiceField(
        SelectWidget('', options=ACCESS_WIDGET_OPTIONS, template='AccessWidget.html', template_dirs=[op.join(__dir__, 'bootstrap/templates')] + SelectWidget.template_dirs),
        choices = ACCESS_FIELD_OPTIONS,
        default = default,
        required = required,
    )



__all__ = (
    # FIELDS
    'Form',
    'FilterForm',
    'SortForm',
    'RecaptchaField',

    # SHORTCUTS
    'SortField',
    'PhoneField',
    'PriceField',
    'AccessField',
)
