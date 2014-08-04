from django.views.generic import TemplateView
from django.views.generic.base import ContextMixin


class MasterContextMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super(MasterContextMixin, self).get_context_data(**kwargs)
        context['menu_item'] = getattr(self, 'menu_item', '')
        return context


class HomeView(TemplateView, MasterContextMixin):
    template_name = 'django_master/home.html'
    menu_item = 'home'

