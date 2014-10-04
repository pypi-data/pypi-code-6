from django.conf.urls import url
from django.views.generic.detail import DetailView
from .models import Demo


urlpatterns = [

    url(r'^(?P<slug>[-_\w]+)/$',
        DetailView.as_view(queryset=Demo.objects.all()),
        name='demoapp.views.detail'
        ),

    ]
