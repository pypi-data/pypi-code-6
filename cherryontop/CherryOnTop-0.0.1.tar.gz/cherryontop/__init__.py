__doc__ = """CherryOnTop is a wrapper for building JSON APIs with CherryPy.

CherryOnTop consists of the following features:
    - proximity of route binding to handler definition, a la Bottle
    - typecasting of query parameters
"""


from cherryontop.cache import map_all_routes
from cherryontop.controller import Controller
from cherryontop.decorators import delete, get, post, put, route
from cherryontop.decorators import typecast_query_params, validate_body
from cherryontop.spinup import start_server


__all__ = [
    'Controller', 'delete', 'get', 'map_all_routes', 'post', 'put', 'route',
    'start_server', 'typecast_query_params', 'validate_body',
]
