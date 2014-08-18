from django.conf import settings
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic.base import RedirectView

from .views import AboutView, HomeView

urlpatterns = patterns('common.views',
    url(r'^$', login_required(HomeView.as_view()), name='home_view'),
    url(r'^set_language/$', 'set_language', name='set_language'),
    url(r'^about/$', login_required(AboutView.as_view()), name='about_view'),
)

urlpatterns += patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'core/login.html'}, name='login_view'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': 'common:home_view'}, name='logout_view'),
    url(r'^myaccount/password_change/$', 'django.contrib.auth.views.password_change', {'template_name': 'core/password_change_form.html'}, name='password_change_view'),
    url(r'^accounts/password_change_ok/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'core/password_change_done.html'}),

    (r'^favicon\.ico$', RedirectView.as_view(url='%simages/favicon.png' % settings.STATIC_URL)),
)
