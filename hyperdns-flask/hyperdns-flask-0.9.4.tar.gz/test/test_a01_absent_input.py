from flasksupport import HyperDNSFlaskTestCase
from flask import make_response
import hyperdns.flask as web


class TestCase(HyperDNSFlaskTestCase):

    def setUp(self):
        super(TestCase,self).setUp()
        
        app=self.app
        class wrap_to_catch_errors(object):
            def __init__(self,route,method):
                self.route=route
                self.method=method
                
            def __call__(self,f):
                return app.route(self.route,methods=[self.method])(
                    web.result.catch_errors(f))

        self.app.wrap_to_catch_errors=wrap_to_catch_errors
        
    
    def test_a00_sanity_check(self):
        
        @self.app.wrap_to_catch_errors('/test','GET')
        def first_test():
            return make_response("ok",200)
        
        result=self.get("/test",as_json=False)
        assert result=='ok'
        
        
    def test_a01_expect_data(self):
        
        @self.app.wrap_to_catch_errors('/test','POST')
        def first_test():
            raise web.InputExpected()
        
        result=self.post("/test",allow4xx=True)
        assert result=={'status': 'error', 'message': 'A request body was expected, but none was provided'}
