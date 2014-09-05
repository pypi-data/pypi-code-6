from django.conf.urls import patterns, include, url

from django.contrib import admin
import huron.simple_medias_manager as simple_medias_manager
from huron.menus_manager import get_url as menu_patterns
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include("huron.blog.urls", namespace="blog")),
    url(r'^contact/', include("huron.contact_form.urls",
        namespace="contact_form")),
    url(r'^pages/', include("huron.pages.urls", namespace="pages")),
    url(r'^news/', include("huron.simple_news.urls", namespace="simple_news")),
)
urlpatterns += simple_medias_manager.get_url()
urlpatterns += menu_patterns()
