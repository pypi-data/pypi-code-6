import cherrypy


def redirect(to=None, default_key=None):
    """
    Sends a redirect, checking for the presence of a trailing slash to avoid an aditional redirect

    :param to: The path redirect
    :param default_key: The key in the config to look for a default path
    """
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