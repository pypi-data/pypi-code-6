from django.views.generic.base import ContextMixin

from django_master.conf import settings as conf


class MasterMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super(MasterMixin, self).get_context_data(**kwargs)
        context['menu_item'] = getattr(self, 'menu_item', '')
        context['settings'] = conf
        return context
