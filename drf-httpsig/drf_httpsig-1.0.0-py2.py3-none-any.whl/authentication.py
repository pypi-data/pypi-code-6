from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
from httpsig import HeaderSigner
import re

try:
    # Python 3
    from urllib.request import parse_http_list
except ImportError:
    # Python 2
    from urllib2 import parse_http_list


class SignatureAuthentication(authentication.BaseAuthentication):
    algorithm = "hmac-sha256"
    
    request = None
    
    def fetch_user_data(self, keyId):
        """Retuns a tuple (User, secret) or (None, None)."""
        return (None, None)

    
    def authenticate(self, request):
        # Check if request has a "Signature" request header.
        authorization_header = self.request_header(request, 'Authorization')
        if not authorization_header:
            return None
            
        authorization_fields = self.parse_authorization_header(authorization_header)

        if authorization_fields == None or len(authorization_fields) == 0:
            raise exceptions.AuthenticationFailed('Invalid signature.')
        
        # Fetch the secret associated with the keyid
        user, secret = self.fetch_user_data(authorization_fields["keyId"])
        if not (user and secret):
            raise exceptions.AuthenticationFailed('Invalid signature.')
        
        # Sign the message ourselves to compare.
        computed_header = self.build_signature(
            authorization_fields['keyId'],
            secret,
            request)
        computed_fields = self.parse_authorization_header(computed_header)
        computed_signature = computed_fields['signature']
        
        if computed_signature != authorization_fields['signature']:
            raise exceptions.AuthenticationFailed('Invalid signature.')
        
        return (user, None)
    
    
    @classmethod
    def parse_authorization_header(cls, auth_header):
        # Ensure this is our type of header
        if not auth_header.startswith("Signature "):
            return None
        
        # Trim the type off
        auth_header = auth_header[len("Signature "):]
        
        # Split up the args into a dictionary
        result = {}
        if auth_header and len(auth_header):
            auth_field_list = parse_http_list(auth_header)
            for item in auth_field_list:
                key, value = item.split('=', 1)
                if value[0] == '"' or value[0] == '\'':
                    value = value[1:-1]
                result[key] = value
        return result
        

    @classmethod
    def canonical_header(cls, header_name):
        """Translate HTTP headers to Django header names."""
        
        header_name = header_name.upper()
        if header_name == 'CONTENT-TYPE' or header_name == 'CONTENT-LENGTH':
            return header_name
        
        # Translate as stated in the docs:
        # https://docs.djangoproject.com/en/1.6/ref/request-response/#django.http.HttpRequest.META
        return "HTTP_" + header_name.replace('-', '_')
    
    
    @classmethod
    def get_headers_from_signature(cls, signature):
        """Returns a list of headers fields to sign."""
        headers = []
        authorization = SignatureAuthentication.parse_authorization_header(signature)
        headers_string = authorization.get('headers')
        
        if headers_string:
            headers.extend(headers_string.split())
        
        return headers


    @classmethod
    def request_header(cls, request, header_name):
        return request.META.get(SignatureAuthentication.canonical_header(header_name), None)

    
    @classmethod
    def build_dict_to_sign(cls, request, signature_headers):
        """
        Build a dict with headers and values used in the signature.
        
        "signature_headers" is a list of header names.
        """
        d = {}
        for header in signature_headers:
            header = header.lower()
            if header == '(request-line)':
                continue #Handled by the signer.
            d[header] = SignatureAuthentication.request_header(request, header)
        return d


    def build_signature(self, keyId, secret, request):
        """Return the signature for the request."""
        
        authorization_header = self.request_header(request, 'Authorization')
        host = self.request_header(request, "Host")
        method = request.method
        path = request.get_full_path()
        
        headers_list = self.get_headers_from_signature(authorization_header)
        headers = self.build_dict_to_sign(request, headers_list)
        
        signer = HeaderSigner(
            key_id=keyId,
            secret=secret,
            algorithm=self.algorithm,
            headers=headers_list,
            )
        
        signed = signer.sign(headers, host=host, method=method, path=path)
        
        return signed['Authorization']
