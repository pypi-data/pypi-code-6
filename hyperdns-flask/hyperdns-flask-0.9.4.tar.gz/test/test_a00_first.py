from flasksupport import HyperDNSFlaskTestCase
from flask import make_response
import hyperdns.flask as web

class TestCase(HyperDNSFlaskTestCase):

    def test_a00_sanity_check(self):
        
        @self.app.route('/test')
        def first_test():
            return make_response("ok",200)
        
        result=self.get("/test",as_json=False)
        assert result=='ok'
        
    def test_a01_returns_json(self):
        
        @self.app.route('/test')
        @web.result.returns_json
        def first_test():
            return web.result.ok()
        
        result=self.get("/test")
        assert result=={'status':'ok'}
