from django.conf.urls import url
from kvtags import views


urlpatterns = [
    url(r'^import-tags/$', views.import_tags, name='kvtags_import_tags'),
]
