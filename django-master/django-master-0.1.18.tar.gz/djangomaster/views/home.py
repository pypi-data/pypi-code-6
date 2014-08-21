import os

from djangomaster.conf import settings
from djangomaster.views import MasterView


class HomeView(MasterView):
    template_name = 'djangomaster/home.html'
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
