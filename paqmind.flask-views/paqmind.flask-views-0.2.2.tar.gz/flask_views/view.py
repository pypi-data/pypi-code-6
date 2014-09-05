from functools import partial
from flask import url_for, redirect, session, Blueprint


class View:
    endpoint = None
    url = None


    def __init__(self, bp):
        if not self.endpoint:
            raise Exception('`{!s}.endpoint` is not defined'.format(self))
        self.bp = bp
        self.url = self.endpoint if self.url is None else self.url
        self.session = session.setdefault(self.endpoint, {})


    # HELPERS ------------------------------------------------------------------
    def redirect(self, endpoint, **kwargs):
        return redirect(self.url_for(endpoint, **kwargs))


    def url_for(self, endpoint, **values):
        if isinstance(self.bp, Blueprint):
            return url_for('{bp}.{self.endpoint}:{endpoint}'.format(
                bp=self.bp.name, self=self, endpoint=endpoint), **values
            )
        else:
            return url_for('{self.endpoint}:{endpoint}'.format(
                self=self, endpoint=endpoint), **values
            )


    def lazy_url_for(self, endpoint, **values):
        if isinstance(self.bp, Blueprint):
            return partial(url_for, '{bp}.{self.endpoint}:{endpoint}'.format(
                bp=self.bp.name, self=self, endpoint=endpoint), **values
            )
        else:
            return partial(url_for, '{self.endpoint}:{endpoint}'.format(
                self=self, endpoint=endpoint), **values
            )
