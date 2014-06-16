from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from .views import (
    ChickenWingsCreateView, ChickenWingsListView
)

urlpatterns = patterns('',  # NOQA

    url(r'^$', ChickenWingsListView.as_view(), name='list'),
    url(r'^create/$', ChickenWingsCreateView.as_view(), name='create'),
    url(r'^created/$', TemplateView.as_view(
        template_name='forthewing/chickenwings_created.html'), name='created'),
    # url(r'^detail/(?P<pk>[0-9]*)$', PizzaDetailView.as_view(), name='detail'),
    # url(r'^update/(?P<pk>[0-9]*)$', PizzaUpdateView.as_view(), name='update'),
    # url(r'^updated/$', TemplateView.as_view(
    #     template_name='pizzagigi/pizza_updated.html'), name='updated'),
    # url(r'^delete/(?P<pk>[0-9]*)$', PizzaDeleteView.as_view(), name='delete'),
    # url(r'^deleted/$', TemplateView.as_view(
    #     template_name='pizzagigi/pizza_deleted.html'), name='deleted'),

)
