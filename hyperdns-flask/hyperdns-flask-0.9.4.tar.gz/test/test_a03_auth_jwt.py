from flasksupport import AuthTestFramework
import hyperdns.flask as web
import jwt
import base64

class TestCase(AuthTestFramework):

    def test_no_header(self):
        (resp,result)=self.get_response("/protected")
        assert resp.status_code==401
        assert resp.content_type=='application/json'
        assert result=={'code': 'authorization_header_missing', 'description': 'Authorization header is expected'}


    def test_bad_header(self):        
        _headers={
            'Authorization':'junk'
        }
        (resp,result)=self.get_response("/protected",headers=_headers)
        assert resp.status_code==401
        assert resp.content_type=='application/json'
        assert result=={'description': 'Authorization header must start with Bearer', 'code': 'invalid_header'}
        
    def test_bearer_junk_jwt(self): 
        _headers={
            'Authorization':'Bearer junk'
        }
        (resp,result)=self.get_response("/protected",headers=_headers)
        assert resp.status_code==401
        assert resp.content_type=='application/json'
        assert result=={'description': 'token signature is invalid', 'code': 'token_invalid_signature', 'reason': 'Not enough segments'}
    
    def test_bearer_with_good_jwt_but_no_user(self):
        def do_test():
            _headers={
                'Authorization':'Bearer %s' % self.good_token
            }
            (resp,result)=self.get_response("/protected",headers=_headers)
        
        self.assertRaises(web.UserLoaderNotFound,do_test)
        
