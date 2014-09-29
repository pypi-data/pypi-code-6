from django.conf.urls import url, include


urlpatterns = [
    url(r'^faq/', include('qanda.urls')),
    ]
