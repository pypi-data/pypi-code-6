import bottle
from pymobile import shared

@bottle.error(401)
@bottle.view('error')
def error401(error):
    error.body = 'You are not logged in. Access denied.'
    return dict(e=error)

@bottle.error(403)
@bottle.view('error')
def error403(error):
    error.body = 'You are not logged in. Access denied.'
    return dict(e=error)