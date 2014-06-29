from cosmos.service import requesthandler

__author__ = 'Maruf Maniruzzaman'

from tornado import gen


class FormHandler(requesthandler.RequestHandler):
    @gen.coroutine
    def get(self):
        self.render('form.html')
