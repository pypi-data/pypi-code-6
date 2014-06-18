from django.conf import settings
from django.views.generic import ListView



class Route(object):
    """ Wraps a RegexURLPattern or RegexURLResolver to create
    a common interface """

    def __init__(self, obj, base=''):
        self.obj = obj
        self.base = base

    @property
    def name(self):
        return getattr(self.obj, 'name', '')

    @property
    def url(self):
        return "%s %s" % (self.base, self.obj.regex.pattern)

    @property
    def view(self):
        if getattr(self.obj, 'callback', None):
            return "%s.%s" % (self.obj.callback.__module__, self.obj.callback.__name__)
        elif getattr(self.obj, '_get_callback', None):
            return "%s.%s" % (self.obj._get_callback().__module__, self.obj._get_callback().__name__)
        elif getattr(self.obj, 'urlconf_module', None):
            return self.obj.urlconf_module.__name__
        else:
            return ''

    @property
    def sub_urls(self):
        urls = getattr(self.obj, 'url_patterns', [])
        return sorted([Route(url, base=self.url) for url in urls], key=lambda x: x.url)


class RoutesListView(ListView):
    template_name = 'django_master/routes.html'
    context_object_name = "route_list"


    def get_queryset(self):
        root_urls = __import__(settings.ROOT_URLCONF)
        ret = []

        for url in root_urls.urls.urlpatterns:
            ret.append(Route(url))

        return ret
