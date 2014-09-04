import cherrypy


def redirect(to=None, default_key=None):
    if to:
        redir = to
    elif default_key:
        default_path = cherrypy.request.config.get(default_key, None)
        redir = default_path if default_path else '/'
    else:
        redir = '/'

    if not redir.endswith('/'):
        redir += '/'

    raise cherrypy.HTTPRedirect(redir)