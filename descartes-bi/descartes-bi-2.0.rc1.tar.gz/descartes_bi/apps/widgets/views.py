import logging
import traceback

from django.views.generic import DetailView

from django.contrib.auth.decorators import login_required

from .models import WidgetBase

logger = logging.getLogger(__name__)

# TODO: login required

class WidgetRenderView(DetailView):
    context_object_name = 'widget'
    queryset = WidgetBase.objects.select_subclasses()
    exception = None

    def get_template_names(self):
        if self.exception:
            return 'widgets/error.html'
        else:
            return self.get_object().template_name

    def get_context_data(self, **kwargs):
        context = super(WidgetRenderView, self).get_context_data(**kwargs)
        context['element_pk'] = self.request.GET.get('element_pk', None)

        try:
            context.update(self.get_object().get_context())
        except Exception as exception:
            context['exception'] = self.exception = traceback.format_exc()

        return context
