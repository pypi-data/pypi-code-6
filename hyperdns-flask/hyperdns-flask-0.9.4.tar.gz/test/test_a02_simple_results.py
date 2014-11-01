from flasksupport import HyperDNSFlaskTestCase
from flask import make_response
import hyperdns.flask as web

class TestCase(HyperDNSFlaskTestCase):

    def test_a00_ok_without_body(self):
        
        @self.app.route('/test')
        def first_test():
            return web.result.ok()
        
        (resp,result)=self.get_response("/test")
        assert resp.status_code==200
        assert resp.content_type=='application/json'
        assert result=={'status': 'ok'}

    def test_a00_ok_with_body(self):
        
        @self.app.route('/test')
        def first_test():
            return web.result.ok(data={'test':'pass'})
        
        (resp,result)=self.get_response("/test")
        assert resp.status_code==200
        assert resp.content_type=='application/json'
        assert result=={'test': 'pass'}
        
    def test_a00_fail(self):
        
        @self.app.route('/test')
        def first_test():
            return web.result.fail(e='fail')
        
        (resp,result)=self.get_response("/test")
        assert resp.status_code==500
        assert resp.content_type=='application/json'
        assert result=={'status': 'error', 'message': 'fail'}
        
