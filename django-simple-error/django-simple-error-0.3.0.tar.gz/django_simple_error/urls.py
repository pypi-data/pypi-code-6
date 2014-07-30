from django.conf.urls import patterns, include, url
from django_simple_error.views import page_not_found, project_error, permission_denied, bad_request

urlpatterns = patterns('',)

handler500 = project_error
handler404 = page_not_found
handler403 = permission_denied
handler400 = bad_request
