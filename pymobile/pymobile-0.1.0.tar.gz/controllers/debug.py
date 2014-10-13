import bottle
from pymobile import shared

@bottle.route('/debug')
@bottle.view('page')
def debug():
    if not shared.session['user']:
        bottle.abort(403)
        
    return dict(title='debug', content=('''
        <span style="word-wrap: break-word;">
        <h1>Header</h1>         <pre>{header}</pre>
        <h1>Environ</h1>        <pre>{env}</pre>
        <h1>Beaker session</h1> <pre>{bk}</pre>
        <h1>State</h1>          <pre>{state}</pre>
        <h1>Shared session</h1> <pre>{sess}</pre>
        </span>
        '''.format(
            header = str(list(bottle.request.headers.items())).replace(", ",",\n"),
            env = str(['{}:  {!r}'.format(e[0], e[1]) for e in list(bottle.request.environ.items()) if e[0].startswith(('HTTP','wsgi', 'REMOTE'))]).replace(", ",",\n"),
            bk = str(bottle.request.environ.get('beaker.session')).replace(", ",",\n"),
            state = repr(shared.state).replace(", ",",\n"),
            sess = repr(shared.session.items()).replace(", ",",\n")
            )))
