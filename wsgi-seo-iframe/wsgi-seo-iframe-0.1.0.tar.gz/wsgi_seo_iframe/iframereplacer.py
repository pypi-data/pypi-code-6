# coding: utf-8
import time
import urlparse
from werkzeug import wsgi
from wsgi_content_modifier import ContentModifier
from pyquery import PyQuery as pQ
import selenium.webdriver


class IframeReplacerMiddleware(ContentModifier):
    '''
    Replaces iframes with a src attribute by divs.

    Selenium WebDriver is used to render links on
    'src' attribute of all iframes and the renderend
    content replaces the iframe on the original page.

    As the iframes contain Ajax it is not easy to detect
    that all Ajax requests have finished, so a wee hack
    is used:

    When the page finishes rendering a loop runs for 5 times,
    this loop waits some time and then it checks whether the
    length of the page has changed. If it has changed the counter
    is reset to 5, if not the counter is decremented.

    Finally, the body of the rendered html is put inside a div that
    replaces the original iframe.

    '''

    def __call__(self, environ, start_response):
        '''
        If there is '_escaped_fragment_' in the querystring,
        runs the middleware.
        '''

        qs_dict = urlparse.parse_qs(wsgi.get_query_string(environ),
                                    keep_blank_values=True)
        if '_escaped_fragment_' in qs_dict:
            self.qs = qs_dict
            return super(IframeReplacerMiddleware, self) \
                .__call__(environ, start_response)
        else:
            app_iter = self.app(environ, start_response)

        return app_iter

    def response_modifier(self, app_iter):
        '''
        Replaces all iframes with 'src' attributes
        by their rendered html code
        '''

        browser = selenium.webdriver.PhantomJS()
        html = [line for line in app_iter]
        html = '\n'.join(html)

        dom = pQ(html)
        iframes = dom('iframe[src]')
        for iframe in iframes:
            dom_node = pQ(iframe)
            start_time = time.time()
            browser.get(dom_node.attr['src'])
            end_time = time.time()

            WAIT_SEC = end_time - start_time
            TRIES_LEFT = 5
            '''
            Loop to wait all ajax script to finish.
            Everytime the length of the page source changes
            the counter is reset.

            In each interaction it waits the time the
            page took to load initally
            '''
            last_length = len(browser.page_source)
            while TRIES_LEFT:
                time.sleep(WAIT_SEC)
                new_length = len(browser.page_source)
                if new_length == last_length:
                    TRIES_LEFT -= 1
                else:
                    last_length = new_length
                    TRIES_LEFT = 5

            rendered_iframe = browser.page_source

            div = pQ(rendered_iframe)
            # Gets only the content of the body tag
            div = div.children('body')
            div.insertAfter(dom_node)
            dom_node.remove()

        ret = dom.outerHtml()

        # Converts to str encoded in UTF-8
        return [ret.encode('utf-8')]

    def header_modifier(self, status, headers, exc_info=None):
        # Remove ``content-length``, as the size of the body is going to change
        headers = filter(lambda h: h[0].lower() != 'content-length', headers)
        return status, headers, exc_info
