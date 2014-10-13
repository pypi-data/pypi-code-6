import bottle
from pymobile import shared, wsfunc

@bottle.route('/wsfunc.js')
@bottle.view('wsfunc')
def websocketfunctionindex():
    bottle.response.content_type = 'text/javascript; charset=UTF8'
    #if not shared.session['user']:
    #    bottle.abort(403)
    return dict(host=bottle.request.environ.get('HTTP_HOST','localhost').split(':')[0], port=wsfunc.port)
