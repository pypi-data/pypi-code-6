from djangomaster.conf import settings as conf


class MasterMixin(object):

    def get_context_data(self, **kwargs):
        context = {}
        context['menu_item'] = getattr(self, 'menu_item', '')
        context['settings'] = conf
        return context
