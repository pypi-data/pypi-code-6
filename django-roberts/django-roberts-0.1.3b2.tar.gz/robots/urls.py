try:
    from django.conf.urls import url
except ImportError:
    from django.conf.urls.defaults import url

try:
    from django.views.generic import TemplateView

    view = TemplateView.as_view(
        template_name='robots/robots.txt',
        content_type='text/plain'
        )
    kwargs = None

except (TypeError, ImportError):
    from django.views.generic.simple import direct_to_template as view
    kwargs = {'template': 'robots/robots.txt', 'mimetype': 'text/plain'}


urlpatterns = [
    url(r'^robots.txt$', view, kwargs, name='robots.views.robotstxt')
]
