import os

from django.views.generic import ListView

from django_master.conf import settings
from django_master.views import MasterMixin


class HomeView(ListView, MasterMixin):
    template_name = 'django_master/home.html'
    context_object_name = 'object'
    menu_item = 'home'


    def get_queryset(self):
        ret = {}
        ret['requirements'] = self.get_requirements()

        return ret


    def get_requirements(self):
        if settings.BASE_DIR is None:
            return {'BASE_DIR_ERROR': True}

        path = os.path.join(settings.BASE_DIR, settings.REQUIREMENTS_TXT)
        if not os.path.isfile(path):
            return {'REQUIREMENTS_ERROR': True, 'path': path}

        return {'content': open(path).read()}
