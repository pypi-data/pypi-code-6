from django.views.generic.list import ListView

from djangomaster.conf import settings as conf


class MasterView(ListView):

    def get_context_data(self, **kwargs):
        context = super(MasterView, self).get_context_data(**kwargs)
        context['menu_item'] = getattr(self, 'menu_item', '')
        context['settings'] = conf
        return context
