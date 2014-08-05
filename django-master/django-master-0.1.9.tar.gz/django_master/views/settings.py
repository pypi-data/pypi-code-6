from collections import OrderedDict

from django.conf import settings
from django.views.generic import ListView

from django_master.views import MasterMixin


class SettingsListView(ListView, MasterMixin):
    template_name = 'django_master/settings.html'
    context_object_name = 'settings_list'
    menu_item = 'settings'

    def get_queryset(self):
        ret = OrderedDict()
        items = settings._wrapped.__dict__.items()

        for key, value in sorted(items, key=lambda key: key):
            ret[key] = value

        return ret.items()
