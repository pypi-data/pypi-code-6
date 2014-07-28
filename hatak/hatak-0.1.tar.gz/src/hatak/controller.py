class Controller(object):

    def __init__(self, request):
        self.request = request
        self._unpack_request()

    def _unpack_request(self):
        for name, value in self._request_args().items():
            setattr(self, name, value)

    def _request_args(self):
        return {
            'POST': self.request.POST,
            'GET': self.request.GET,
            'matchdict': self.request.matchdict,
            'settings': self.request.registry['settings'],
            'session': self.request.session,
        }

    def __call__(self):
        self.data = {}
        self.before_filter()
        data = self.make() or {}
        self.data.update(data)
        self.after_filter()
        return self.data

    def make(self):
        pass

    def before_filter(self):
        for method in self.before():
            method()

    def after_filter(self):
        for method in self.after():
            method()

    def before(self):
        return []

    def after(self):
        return []


class DatabaseController(Controller):

    def _request_args(self):
        data = super()._request_args()
        data['db'] = self.request.registry['db']
        return data
