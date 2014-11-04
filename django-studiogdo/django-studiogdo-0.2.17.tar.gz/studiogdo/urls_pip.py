from django.conf.urls import url, patterns
from django.conf import settings
from studiogdo.pip.views import LoginView, AccueilView

urlpatterns = patterns('',
                       url(r'^%s$' % getattr(settings, 'LOGIN_URL', ''), view=LoginView.as_view(), name="login"),
                       url(r'^accueil/$', view=AccueilView.as_view(), name="accueil"),
)
