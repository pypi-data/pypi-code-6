import cherrypy

RENDERER = 'templating.renderer'
TEMPLATE_NAME = '_template_name'


_templating_config = {}


def _templating_namespace(k, v):
    _templating_config[k] = v

cherrypy.config.namespaces['templating'] = _templating_namespace


def _template_tool(next_handler, *args, **kwargs):
    template_name = getattr(next_handler.callable, TEMPLATE_NAME)
    renderer = cherrypy.request.config.get(RENDERER)
    context = next_handler(*args, **kwargs)

    return renderer(template_name, context)

cherrypy.tools.template = cherrypy._cptools.HandlerWrapperTool(_template_tool)


def template(template_name):
    """
    Decorator for setting the template on the handler function

    :param template_name: The name of the template
    :type template_name: str
    """
    def closure(handler):
        setattr(handler, TEMPLATE_NAME, template_name)
        return cherrypy.tools.template()(handler)
    return closure