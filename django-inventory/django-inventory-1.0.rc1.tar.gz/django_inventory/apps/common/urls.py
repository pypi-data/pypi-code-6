from __future__ import absolute_import

from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy

from .views import AboutView

urlpatterns = patterns('common.views',
    url(r'^about/$', AboutView.as_view(), name='about'),
    url(r'^password/change/done/$', 'password_change_done', (), name='password_change_done'),
)

urlpatterns += patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'common/login.html'}, name='login_view'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': reverse_lazy('home')}, name='logout_view'),

    url(r'^password/change/$', 'django.contrib.auth.views.password_change', {'template_name': 'common/password_change_form.html', 'post_change_redirect': reverse_lazy('password_change_done')}, name='password_change_view'),
    url(r'^password/reset/$', 'django.contrib.auth.views.password_reset', {'email_template_name': 'common/password_reset_email.html', 'template_name': 'common/password_reset_form.html', 'post_reset_redirect': '/password/reset/done'}, name='password_reset_view'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'template_name': 'common/password_reset_confirm.html', 'post_reset_redirect': '/password/reset/complete/'}, name='password_reset_confirm_view'),
    url(r'^password/reset/complete/$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'common/password_reset_complete.html'}, name='password_reset_complete_view'),
    url(r'^password/reset/done/$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'common/password_reset_done.html'}, name='password_reset_done_view'),
)

urlpatterns += patterns('',
    url(r'^set_language/$', 'django.views.i18n.set_language', name='set_language'),
)
