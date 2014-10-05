from django.core.urlresolvers import reverse
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    Http404,
)
from .exceptions import RedirectException


class ExceptionsMiddleware(object):
    """Middleware to process custom exception and redirect
    the user to the view
    """
    def process_exception(self, request, exception):
        if isinstance(exception, RedirectException):
            view_name = exception.view_name
            template_name = exception.template_name
            if view_name:
                try:
                    view = reverse(view_name)
                    return HttpResponseRedirect(view)
                except:
                    raise Http404
            elif template_name:
                from django.views.generic import TemplateView
                return TemplateView.as_view(
                        template_name=template_name
                    )(request)
