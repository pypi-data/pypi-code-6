import time
import jwt, requests

from livefyre.src.core.site import Site
from livefyre.src.api import Domain


class Network(object):
    DEFAULT_USER = 'system'
    DEFAULT_EXPIRES = 86400
    
    def __init__(self, name, key):
        self.name = name
        self.key = key
        self.ssl = True
        self.network_name = name.split('.')[0]
    
    
    def set_user_sync_url(self, url_template):
        assert '{id}' in url_template, 'url_template should have {id}.'
        
        url = Domain.quill(self)+'/'
        data = {'actor_token' : self.build_livefyre_token(), 'pull_profile_url' : url_template}
        headers = {'Content-type': 'application/json'}
        
        request = requests.post(url=url, data=data, headers=headers)
        return request.status_code is 204
        
        
    def sync_user(self, user_id):
        url = '{0}/api/v3_0/user/{1}/refresh'.format(Domain.quill(self), user_id)
        data = {'lftoken' : self.build_livefyre_token()}
        headers = {'Content-type': 'application/json'}
        
        request = requests.post(url=url, data=data, headers=headers)
        return request.status_code is 200
    
    
    def build_livefyre_token(self):
        return self.build_user_auth_token(self.DEFAULT_USER, self.DEFAULT_USER, self.DEFAULT_EXPIRES)
    
    
    def build_user_auth_token(self, user_id, display_name, expires):
        assert user_id.isalnum(), 'user_id should only contain alphanumeric characters'

        return jwt.encode({
                'domain': self.name,
                'user_id': user_id,
                'display_name': display_name,
                'expires': int(time.time()) + expires},
            self.key)
    
    
    def validate_livefyre_token(self, lf_token):
        token_attr = jwt.decode(lf_token, self.key)
        return (token_attr['domain'] == self.name
            and token_attr['user_id'] == self.DEFAULT_USER
            and token_attr['expires'] >= int(time.time()))
        
    
    def get_site(self, site_id, site_key):
        return Site(self, site_id, site_key)
    
    
    def get_network_name(self):
        return self.network_name
    
        
    def get_urn(self):
        return 'urn:livefyre:' + self.name
    
    
    def get_user_urn(self, user):
        return self.get_urn() + ':user=' + user
