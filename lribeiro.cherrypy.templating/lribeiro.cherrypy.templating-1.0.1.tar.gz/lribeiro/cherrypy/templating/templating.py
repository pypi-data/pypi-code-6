import cherrypy

RENDERER = 'templating.renderer'
TEMPLATE_NAME = '__template_name'
TEMPLATE_ARGS = '__template_args'
TEMPLATE_KWARGS = '__template_kwargs'


_templating_config = {}


def _templating_namespace(k, v):
    _templating_config[k] = v

cherrypy.config.namespaces['templating'] = _templating_namespace


def _template_tool(next_handler, *args, **kwargs):
    template_name = getattr(next_handler.callable, TEMPLATE_NAME)
    template_args = getattr(next_handler.callable, TEMPLATE_ARGS)
    template_kwargs = getattr(next_handler.callable, TEMPLATE_KWARGS)

    renderer = cherrypy.request.config.get(RENDERER)
    context = next_handler(*args, **kwargs)

    return renderer(template_name, context, *template_args, **template_kwargs)

cherrypy.tools.template = cherrypy._cptools.HandlerWrapperTool(_template_tool)


def template(template_name, *args, **kwargs):
    """
    Decorator for setting the template on the handler function

    :param template_name: The name of the template
    :type template_name: str
    """
    def decorate(handler):
        setattr(handler, TEMPLATE_NAME, template_name)
        setattr(handler, TEMPLATE_ARGS, args)
        setattr(handler, TEMPLATE_KWARGS, kwargs)
        return cherrypy.tools.template()(handler)
    return decorate