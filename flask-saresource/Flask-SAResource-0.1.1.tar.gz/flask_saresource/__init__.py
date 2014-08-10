from flask import current_app
from flask.ext.restful import Api

try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack

from .resource import create_single_resource
from .resource import create_list_resource

class SAResource(object):
    def __init__(self, app=None, session=None, url_prefix=None):
        """Initialize SAResource object. Accepts an app object,
        a SQLAlchemy database session object and a url_prefix 
        for the resource's URIs.

        e.g. SAResource(my_app, my_session, '/api/v1')
        """
        self.app = app
        self.session = session
        self.url_prefix = url_prefix
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)

        self.api = Api(app)

    def add_resource(self, model):
        """Add single and collection endpoints for a given SQLAlchemy 
        declarative model class.

        """
        tablename = model.__tablename__
        self.api.add_resource(create_list_resource(model, self.session),
                              '/{}'.format(tablename),
                              endpoint=tablename)
        self.api.add_resource(create_single_resource(model, self.session),
                              '/{}/<string:id>'.format(tablename),
                              endpoint=tablename[:-1])

    def teardown(self, exception):
        ctx = stack.top
