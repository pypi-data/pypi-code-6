"""Expose Flask-SQLAlchemy models as HAL objects.
"""
from werkzeug.local import LocalProxy,LocalStack
from flask import _request_ctx_stack

# make the user and account available - these come from auth.py ultimately
# but we define them here - @todo - is this the right place?
hyperdns_context = LocalProxy(lambda: _request_ctx_stack.top.hyperdns)

# local reference to 'the app object' - there has *got* to be a better way to do this
_FLASKAPP=None

from .sql import init_sqlalchemy_support
def init_app(app):
    """
    Initializes components of the flask module that require access to
    the actual app.
     - initialize the app.db.Map and app.db.Scalar elements.
     - allows the crossdomain decorator to call _app.make_default_options_response
    """
    global _FLASKAPP
    _FLASKAPP=app

    init_sqlalchemy_support(app)

class UserLoaderNotFound(Exception):
    pass
    

class ExceptionWithResponse(Exception):
    """This exception can be raised, and the catch_errors method
    below will unwrap it and return the provided response"""
    def __init__(self,resp):
        self.resp=resp

class InputExpected(ExceptionWithResponse):
    def __init__(self):
        import hyperdns.flask as web
        super(InputExpected,self).__init__(resp=web.result.input_expected())

        

# now, pull in the sub-modules
from .api import api
from .auth import auth,crossdomain
from .result import result

