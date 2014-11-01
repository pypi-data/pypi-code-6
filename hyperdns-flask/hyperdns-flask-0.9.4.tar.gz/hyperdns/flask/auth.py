"""Authentication and Security Support including CORS support

"""
import json
import datetime
from functools import update_wrapper
from flask import request,make_response,_request_ctx_stack,Response
import jwt
import hyperdns.flask
import base64
from hyperdns.flask import UserLoaderNotFound
from .result import result
#
#
def crossdomain(origin=None, methods=None, headers=None,max_age=21600, attach_to_all=True,automatic_options=True):
    """ Wrapper functions for CORS """
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, str):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, str):
        origin = ', '.join(origin)
    if isinstance(max_age, datetime.timedelta):
        max_age = max_age.total_seconds()
    
    def get_methods():
        if methods is not None:
            return methods
        
        options_resp = hyperdns.flask._FLASKAPP.make_default_options_response()
        return options_resp.headers['allow']
    
    def decorator(f):
        def _crossdomain(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = hyperdns.flask._FLASKAPP.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp
            h = resp.headers
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp
        
        f.provide_automatic_options = False
        f.required_methods = ['OPTIONS']
        return update_wrapper(_crossdomain, f)
    return decorator



# primary authentication object
class auth(object):
    """
    from:
        http://www.vinaysahni.com/best-practices-for-a-pragmatic-restful-api#json-requests
        http://broadcast.oreilly.com/2011/06/the-good-the-bad-the-ugly-of-rest-apis.html
        http://blog.auth0.com/2014/01/07/angularjs-authentication-with-cookies-vs-token/
    
    HTTPS/SSL
    
    SSL is required at all times.  Files served to the client are public, and can be delivered
    via HTTP from public sources like CDNs or S3.  Any data that is not in the public domain
    must be protected, minimally, by SSL.
    
    
    Authentication
    
    (I got this from somewhere I think?)
    
    A RESTful API should be stateless. This means that request authentication should not
    depend on cookies or sessions. Instead, each request should come with some sort
    authentication credentials.  Every request should be authenticated and authorized.
    Revocation must be available in real-time via a blacklist.
    
    REST api credentials should not directly involve the principal credentials.  Instead,
    an API consumer should request an access token with a fixed viability duration.  Periodically
    this token must be refreshed using the principal tokens.
    
    Authentication data should arrive via headers and should itself be considered public.
    HTTPS w/ Basic authentication has the problem of passing principal credentials on every
    request and requiring direct validation against the primary principal verification database.
    Use of an ancillary token minimizes the exposure of principal credentials and decouples
    the primary verification mechanism from each request while retaining the REST requirement
    of per-request authentication and authorization.
    
    """
    CLIENT_ID = "<to-be-set>"
    """This is the identity of the user registry and must match the 'aud' claim
    in the JWT.  This is set by calling web.auth.config().
    """
    CLIENT_SECRET = "<to-be-set>"
    """This is the client encryption key for the user registry identified by
    the CLIENT_ID field.  This is set by calling web.auth.config().  See the
    documentation of that method for additional information about the encoding
    of the CLIENT_SECRET.
    """
    def __init__(self):
        pass
        
    @classmethod
    def config(cls,config):
        """Configures the authentication environment so that we can decode and
        verify JWTs.
        
        Example::
            web.auth.config({
                'CLIENT_ID':'23j908u09vzko3k09f32',
                'CLIENT_SECRET':'2j309z098109k90e2kf9023h8f89aijfg9awj489j9f3k20':'
            })
            
        The CLIENT_ID must match the 'aud' claim in the JWT claim set.  This is a
        simple string comparison.
        
        The CLIENT_SECRET is expected to be the base64 encoded value, and some
        substitutions are made prior to base64 decoding.  I'm not sure why those
        replacements are necessary, but this was develoepd using CLIENT_SECRETS
        provided by Auth0, and in their examples, the substitution of "_" characters
        for "/" characters and of "-" with "+" characters is required before the
        CLIENT_SECRET can be decoded by the :meth:`base64.b64decode` method.
        """
        assert config!=None
        cls.CLIENT_ID=config['CLIENT_ID']
        # client ids from auth0 are base64 encoded, and have to have a few
        # characters replaced - i saw the replacement bit in some of the code
        # examples, but not sure what it's all about
        raw=config['CLIENT_SECRET'].replace("_","/").replace("-","+")
        cls.CLIENT_SECRET=base64.b64decode(raw)        
          
    @staticmethod
    def _load_user_and_roots(jwt_payload,request):
        """This method is invoked when a valid JWT is decoded.
        """
        raise UserLoaderNotFound('Use @web.auth.user_loader annotation somewhere')

    @classmethod
    def _extract_payload_from_jwt(cls,request):
        """This method validates the JWT and returns the claim set in the body
        """
        auth = request.headers.get('Authorization', None)
        if not auth:
          return result.unauthorized({
                      'code': 'authorization_header_missing',
                      'description': 'Authorization header is expected'})
        
        parts = auth.split()                
        if parts[0].lower() != 'bearer':
          return result.unauthorized({
                    'code': 'invalid_header',
                    'description': 'Authorization header must start with Bearer'})
        elif len(parts) == 1:
          return result.unauthorized({
                  'code': 'invalid_header',
                  'description': 'Token not found'})
        elif len(parts) > 2:
          return result.unauthorized({
                  'code': 'invalid_header',
                  'description': 'Authorization header must be Bearer + \s + token'})

        # now we have a token
        token = parts[1]
        try:
            token=token.encode('utf-8')
            payload = jwt.decode(token,cls.CLIENT_SECRET,verify=True)
        except jwt.ExpiredSignature:
            return result.unauthorized({
                    'code': 'token_expired',
                    'description': 'token is expired'})
        except jwt.DecodeError as E:
            return result.unauthorized({
                'code': 'token_invalid_signature',
                'description': 'token signature is invalid',
                'reason':str(E)})
        
        if payload.get('aud') != cls.CLIENT_ID:
          return result.unauthorized({
                'code': 'invalid_audience',
                'description': 'the audience does not match.'})
                
        return (jwt,payload)

    @classmethod
    def _manage_authentication(cls,f,*args, **kwargs):
        """Wrap authentcation calls as follows:
            1. ignore OPTIONS
            2. extract the payload, abort if the extraction resulted in a 401 error
            3. return a 401 if the user could not be loaded
            4. store the user, account, token, and roots in the global context
        """
        # do not require authentication for 'OPTIONS' requests
        # can we truncate here?
        if request.method=='OPTIONS':
            return None
        else:
            # abort if the extractor generated a 401
            resp=cls._extract_payload_from_jwt(request)
            if isinstance(resp,Response):
                return resp
            (token,payload)=resp
            
            # obtain user context, abort if the User is not found
            (user,account,roots)=cls._load_user_and_roots(payload,request) 
            if user is None:
                return result.unauthorized({
                    'code':'user_not_found',
                    'description':"No such user '%s'" % payload.get('sub')
                })
                
            # available as request.hyperdns pass
            _request_ctx_stack.top.hyperdns = {
                'user':user,
                'account':account,
                'jwt':token,
                'available_roots':roots
            }
                            
            return f(*args, **kwargs)
    
    def __call__(self,f):
        """Attach the security wrapper that called _manage_authentication"""
        def security_wrapper(*args,**kwargs):
            return self.__class__._manage_authentication(f,*args,**kwargs)
        d=security_wrapper
        d.__name__=f.__name__
        return d
        
    @classmethod
    def user_loader(cls,callback):
        """Decorator to tag a callback as the function returning the user and
        the roots
        """
        cls._load_user_and_roots=staticmethod(callback)
        return callback
        
    
    @classmethod
    def create_jwt(cls,payload):
        """Return a JWT with the specified payload, encrypted using the configured
        application secret.
        """
        payload['aud']=cls.CLIENT_ID
        return str(jwt.encode(payload,cls.CLIENT_SECRET),'utf-8')
            
#
