try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

from django.conf import settings

from djangomaster.views import MasterView


class SettingsListView(MasterView):
    template_name = 'djangomaster/settings.html'
    context_object_name = 'settings_list'
    menu_item = 'settings'

    def get_queryset(self):
        ret = OrderedDict()
        items = settings._wrapped.__dict__.items()

        for key, value in sorted(items, key=lambda key: key):
            ret[key] = value

        return ret.items()
