from __future__ import unicode_literals
from django.core.cache import cache
from django.http import HttpResponse
import selenium.webdriver

from .settings import crawler_settings

# Delete fragment meta tag from handled source
script = '''
var i, refAttr;
var metaTags = document.getElementsByTagName('meta');
for (i=metaTags.length-1; i>=0; i--) {
    if( (nameAttr = metaTags[i].getAttribute("name")) && (nameAttr == 'fragment') ) {
        metaTags[i].parentNode.removeChild(metaTags[i]);
    }
}
'''


class EscapedFragmentMiddleware(object):

    def get_driver_data(self, url, use_cache=True):

        driver = selenium.webdriver.PhantomJS(port=64738)

        if use_cache:
            content = cache.get(url)
            if content:
                return content

        driver.get(url)
        driver.execute_script(script)
        content = driver.page_source
        driver.quit()

        if use_cache:
            cache.set(url, content, crawler_settings['CACHE_TIMEOUT'])

        return content

    def process_response(self, request, response):
        if '_escaped_fragment_' in request.GET:
            url = "{0}{1}".format(crawler_settings['SITE_URL'], request.path)
            return HttpResponse(content=self.get_driver_data(url))
        return response
