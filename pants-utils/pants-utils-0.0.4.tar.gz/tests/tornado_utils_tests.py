import tornado.web
import tornado.testing

from pants_utils import tornado_utils

class TestTemplateLoaderHandler(tornado.web.RequestHandler):
    def get(self):
        loader = tornado_utils.PexTemplateLoader('tests','templates')
        self.write(loader.load('index.html').generate())

class PantsUtilsTornadoTestCase(tornado.testing.AsyncHTTPTestCase):
    def get_app(self):
        return tornado.web.Application(
            [
                (r'/', TestTemplateLoaderHandler),
                (r'/static/(.*)', tornado_utils.PexStaticFileHandler,
                 dict(path='tests', subdir='static'))
            ])

    def test_get_staticfile_200(self):
        self.http_client.fetch(self.get_url('/static/staticfile.txt'), self.stop)
        response = self.wait()
        self.assertEqual(response.code, 200)

    def test_get_staticfile_404(self):
        self.http_client.fetch(self.get_url('/static/i/dont/exist.txt'), self.stop)
        response = self.wait()
        self.assertEqual(response.code, 404)

    def test_template_loader(self):
        self.http_client.fetch(self.get_url('/'), self.stop)
        response = self.wait()
        self.assertEqual(response.body, 'hello world\n')
