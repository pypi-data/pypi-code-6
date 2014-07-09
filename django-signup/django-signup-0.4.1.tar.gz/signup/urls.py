from django.conf.urls import patterns, url, include

from .views import SignUpView, SignupClosedView, SignUpCompleteView, ActivateView, ActivateCompleteView

urlpatterns = patterns('',
	url(r'^signup/$', SignUpView.as_view(), name='signup_signup'),
	url(r'^signup/closed/$', SignupClosedView.as_view(), name='signup_closed'),
	url(r'^signup/complete/$', SignUpCompleteView.as_view(), name='signup_signup_complete'),
	url(r'^activate/complete/$', ActivateCompleteView.as_view(), name='signup_activate_complete'),
	url(r'^activate/(?P<activation_key>\w+)/$', ActivateView.as_view(), name='signup_activate'),
	url(r'', include('django.contrib.auth.urls')),
)
