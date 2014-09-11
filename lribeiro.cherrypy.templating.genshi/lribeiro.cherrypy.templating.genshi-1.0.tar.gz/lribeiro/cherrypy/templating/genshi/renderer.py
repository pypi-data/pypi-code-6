import cherrypy

from .loader import get_loader

RENDER_OPTIONS = 'templating.genshi.render_options'
DEFAULT_METHOD = 'html'
DEFAULT_DOCTYPE = 'html5'


def genshi_renderer(template_name, context, *args, **kwargs):
    render_options = cherrypy.request.config.get(RENDER_OPTIONS, {})

    if 'method' not in render_options:
        render_options['method'] = DEFAULT_METHOD
        render_options['doctype'] = DEFAULT_DOCTYPE

    # options passed by the @template decorator override the options on the configuration
    render_options.update(kwargs)

    loader = get_loader()
    template = loader.load(template_name)
    return template.generate(**context).render(*args, **render_options)