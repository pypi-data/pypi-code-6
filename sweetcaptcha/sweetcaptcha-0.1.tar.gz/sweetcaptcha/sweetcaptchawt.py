from wtforms import Field, ValidationError
from sweetcaptcha import get_html, check


class SweetCaptchaField(Field):

    def __init__(self, label='', validators=None, app_id=None,
                 app_key=None, **kwargs):
        super(SweetCaptchaField, self).__init__(label, validators, **kwargs)

        if None in (app_id, app_key):
            raise TypeError('app_id and app_key must be provided.')

        self.app_id = app_id
        self.app_key = app_key

    def __call__(self,  **kwargs):
        return get_html(self.app_id, self.app_key)

    def pre_validate(self, form):
        if 'sckey' not in form:
            raise ValidationError('sckey must be defined on parent form.')
        if 'scvalue' not in form:
            raise ValidationError('scvalue must be defined on parent form.')

    def post_validate(self, form, validation_stopped):
        if validation_stopped:
            return
        if not check(self.app_id, self.app_key, form.sckey.data,
                     form.scvalue.data):
            raise ValidationError('Invalid captcha.')