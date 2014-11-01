from flasksupport import AuthTestFramework
import hyperdns.flask as web
import jwt
import base64

class TestCase(AuthTestFramework):
                
    def test_bearer_with_good_jwt_and_user_not_found(self):
      
        @web.auth.user_loader
        def load_user(token,payload):
            return ("user",None,None)
          
        def do_test():
            _headers={
                'Authorization':'Bearer %s' % self.good_token
            }
            (resp,result)=self.get_response("/protected",headers=_headers)
        
        do_test()