from django.conf.urls import patterns, include, url

from .views import upload_photos, recent_photos

urlpatterns = patterns('',
    url(r"^images/upload/$", upload_photos, name="drift_upload_photos"),
    url(r"^images/recent/$", recent_photos, name="drift_recent_photos"),
)
