from cratis.features import Feature
#
#from cms.appresolver import applications_page_check
#
#
#class LazyPage(object):
#    def __get__(self, request, obj_type=None):
#        from cms.utils.page_resolver import get_page_from_request
#        if not hasattr(request, '_current_page_cache'):
#            request._current_page_cache = get_page_from_request(request)
#            if not request._current_page_cache:
#                # if this is in a apphook
#                # find the page the apphook is attached to
#                request._current_page_cache = applications_page_check(request)
#        return request._current_page_cache
#
#
#class CurrentPageMiddleware(object):
#    def process_request(self, request):
#        request.__class__.current_page = LazyPage()
#        return None


class Cms(Feature):

    def configure_settings(self):
        self.append_apps([
            'cms',
            'mptt',
            'menus',
            'south',
            'sekizai',

            # 'cms.plugins.flash',
            'cms.plugins.googlemap',
            'cms.plugins.link',
            'cms.plugins.text',
            # 'cms.plugins.twitter'
        ])

        self.append_middleware([
            'cms.middleware.page.CurrentPageMiddleware',
            'cms.middleware.user.CurrentUserMiddleware',
            'cms.middleware.toolbar.ToolbarMiddleware',
            'cms.middleware.language.LanguageCookieMiddleware'
        ])

        self.append_template_processor([
            'cms.context_processors.media',
            'sekizai.context_processors.sekizai',
            'django.core.context_processors.request'
        ])

        self.settings.CMS_TEMPLATES = self.settings.CMS_TEMPLATES or ()


    def configure_urls(self, urls):

        from django.conf.urls import url, patterns
        from cms.views import details
        from django.views.decorators.cache import cache_page

        try:
            from cratis.app.i18n.utils import localize_url as _
        except ImportError:
            _ = lambda x: x

        if self.settings.DEBUG:
            urls += patterns('',
                             url(_(r'^$'), details, {'slug': ''}, name='pages-root'),
                             url(_(r'^(?P<slug>[0-9A-Za-z-_.//]+)$'), details, name='pages-details-by-slug'),
            )
        else:
            urls += patterns('',
                             url(_(r'^$'), cache_page(60 * 24)(details), {'slug': ''}, name='pages-root'),
                             url(_(r'^(?P<slug>[0-9A-Za-z-_.//]+)$'), cache_page(60 * 24)(details),
                                 name='pages-details-by-slug'),
            )
