from django.conf.urls import url, patterns
from studiogdo.pip.views import LoginView, AccueilView

urlpatterns = patterns('',
    url(r'^$', view=LoginView.as_view(), name="login"),
    url(r'^accueil/$', view=AccueilView.as_view(), name="accueil"),
)
