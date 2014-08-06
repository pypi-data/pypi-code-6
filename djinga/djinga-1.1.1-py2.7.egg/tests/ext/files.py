from tests.base import TestCase


class StaticTests(TestCase):

    extensions = ('djinga.ext.static',
                  'djinga.ext.css',
                  'djinga.ext.js',
                  'djinga.ext.media',)

    def test_static(self):
        self.template = "{% static 'img/astaticimage.png' %}"
        self.assertRender('/static/img/astaticimage.png')

    def test_static_abs(self):
        self.template = "{% static '/files/astaticimage.png' %}"
        self.assertRender('/files/astaticimage.png')

    def test_css(self):
        self.template = "{% css 'base.css' %}"
        self.assertRender('<link rel="stylesheet" type="text/css" '
                          'href="/static/css/base.css">')

    def test_js(self):
        self.template = "{% js 'script.js' %}"
        self.assertRender('<script type="text/javascript" '
                          'src="/static/js/script.js"></script>')

    def test_media(self):
        self.template = "{% media 'img/astaticimage.png' %}"
        self.assertRender('/media/img/astaticimage.png')

    def test_media_abs(self):
        self.template = "{% media '/media2/img/astaticimage.png' %}"
        self.assertRender('/media2/img/astaticimage.png')
