from flasksupport import AuthTestFramework
import hyperdns.flask as web
import jwt
import base64

class TestCase(AuthTestFramework):
        
    def test_bearer_with_good_jwt_but_user_not_found(self):
        
        @web.auth.user_loader
        def load_user(token,payload):
            return (None,None,None)
            
        _headers={
            'Authorization':'Bearer %s' % self.good_token
        }
        (resp,result)=self.get_response("/protected",headers=_headers)

        assert resp.status_code==401
        assert resp.content_type=='application/json'
        assert result=={'code': 'user_not_found', 'description': "No such user 'edward-abbey'"}
        
