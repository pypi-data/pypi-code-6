from pyramid.session import check_csrf_token
from hatak.unpackrequest import unpack

from formskit import Form, Field
from formskit.formvalidators import FormValidator


class PostForm(Form):

    def __init__(self, request):
        self.request = request
        unpack(self, self.request)
        super().__init__()

        self.addField(Field('csrf_token'))
        self.addFormValidator(CsrfMustMatch())

    def __call__(self, initial_data=None):
        initial_data = initial_data or {}
        initial_data['csrf_token'] = [self.request.session.get_csrf_token()]
        return super().__call__(
            self.request.POST.dict_of_lists(),
            initial_data=initial_data)


class CsrfMustMatch(FormValidator):

    message = "CSRF token do not match!"

    def validate(self):
        return check_csrf_token(self.form.request, raises=False)
