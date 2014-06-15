from django.shortcuts import _get_queryset, get_object_or_404, get_list_or_404
from django.template import Template, Context, RequestContext
from django.http import Http404, HttpResponse
from django.template import loader

from jmb.core.middleware.thread_local import get_request

def render_to_response(template_name, request=None, **kwargs):
    httpresponse_kwargs = {'mimetype': kwargs.pop('mimetype', None)}
    request = request or get_request()
    context_instance = RequestContext(request)
    if not kwargs.has_key('is_popup'):
        kwargs.update({
            'is_popup': request.REQUEST.has_key('_popup'),
        })

    return HttpResponse(
        loader.render_to_string(
            template_name=template_name,
            dictionary=kwargs,
            context_instance=context_instance,
        ),
        **httpresponse_kwargs
    )

def render_to_string(template_name, request=None, context_instance=None, **kwargs):
    request = request or get_request()
    if not context_instance:
        if request:
            context_instance = RequestContext(request)
        else:
            context_instance = Context(kwargs)
    return loader.render_to_string(
        template_name=template_name,
        dictionary=kwargs,
        context_instance=context_instance,
    )

def render_from_string(template_string, request=None, **kwargs):
    t = Template(template_string)
    if request:
        context_instance = RequestContext(request, kwargs)
    else:
        context_instance = Context(kwargs)
    return t.render(context_instance)

def get_queryset_or_404(klass, *args, **kw):
    queryset = _get_queryset(klass)
    q = queryset.filter(*args, **kw)
    if not q:
        raise Http404('No %s matches the given query.' % queryset.model._meta.object_name)
    return q

