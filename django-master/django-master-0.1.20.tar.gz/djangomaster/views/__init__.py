from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.utils import simplejson as json
from django.utils.decorators import method_decorator
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import ListView

from djangomaster.conf import settings as conf


class MasterView(ListView):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied

        return super(MasterView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MasterView, self).get_context_data(**kwargs)
        context['menu_item'] = getattr(self, 'menu_item', '')
        context['settings'] = conf
        return context


class JSONResponseMixin(object):
    """
    # @see https://docs.djangoproject.com/en/1.4/topics/class-based-views/
    """

    def render_to_response(self, context):
        "Returns a JSON response containing 'context' as payload"
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        return HttpResponse(content, content_type='application/json',
                            **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.

        if 'object' in context:
            return json.dumps(context['object'], cls=DjangoJSONEncoder)
        else:
            return json.dumps(context, cls=DjangoJSONEncoder)


class JSONDetailView(JSONResponseMixin, BaseDetailView):
    pass


class MasterJSONView(JSONResponseMixin, ListView):
    @method_decorator(login_required)
    def dispach(self, *args, **kwargs):
        if not self.request.user.is_admin:
            raise PermissionDenied

        return super(JSONDetailView, self).dispach(*args, **kwargs)
