import base64, sys, hashlib
import jwt, requests

from livefyre.src.utils import is_valid_full_url
from livefyre.src.api import Domain

try:
    import simplejson as json
except ImportError:
    import json


class Site(object):
    TYPE = ['reviews', 'sidenotes', 'ratings', 'counting', 'liveblog', 'livechat', 'livecomments']
    
    def __init__(self, network, s_id, key):
        self.network = network
        self.s_id = s_id
        self.key = key
    
    
    def build_collection_meta_token(self, title, article_id, url, options={}):
        assert is_valid_full_url(url), 'url must be a full domain. ie. http://livefyre.com'
        assert len(title) <= 255, "title's length should be under 255 char"
        
        collection_meta = {
            'title': title,
            'url': url,
            'articleId': article_id
        }

        if 'type' in options and options['type'] not in self.TYPE:
            raise AssertionError('type is not a recognized type. must be in {0}'.format(self.TYPE))
        
        collection_meta.update(options)
        return jwt.encode(collection_meta, self.key)
    
    
    def build_checksum(self, title, url, tags=''):
        assert is_valid_full_url(url), 'url must be a full domain. ie. http://livefyre.com'
        assert len(title) <= 255, "title's length should be under 255 char"
        
        meta_string = '{{"tags":"{0}","title":"{1}","url":"{2}"}}'.format(tags, title, url)

        return hashlib.md5(meta_string).hexdigest()
    
    
    def create_collection(self, title, article_id, url, options={}):
        uri = '{0}/api/v3.0/site/{1}/collection/create/'.format(Domain.quill(self), self.s_id)
        data = {
            'articleId': article_id,
            'collectionMeta': self.build_collection_meta_token(title, article_id, url, options),
            'checksum': self.build_checksum(title, url, (options['tags'] if 'tags' in options else '')),
        }
        headers = {'Content-Type': 'application/json', 'Accepts': 'application/json'}
            
        response = requests.post(uri, params={'sync':1}, data=json.dumps(data), headers=headers)
        
        if response.status_code == 200:
            return response.json()['data']['collectionId']
        return None
    
    
    def get_collection_content(self, article_id):
        if sys.version_info >= (3, 0):
            article_bytes = bytes(str(article_id), 'utf-8')
        else:
            article_bytes = bytes(str(article_id))
        encoded_article_id = base64.b64encode(article_bytes).decode('utf-8')
        url = '{0}/bs3/{1}/{2}/{3}/init'.format(Domain.bootstrap(self), self.network.name, self.s_id, encoded_article_id)
        
        response = requests.get(url=url)
        if response.status_code == 200:
            return response.json()
        return None


    def get_collection_id(self, article_id):
        json = self.get_collection_content(article_id)
        if json:
            return json['collectionSettings']['collectionId']
        return None
    
    
    def build_livefyre_token(self):
        return self.network.build_livefyre_token()


    def get_network_name(self):
        return self.network.get_network_name()
    

    def get_urn(self):
        return self.network.get_urn() + ":site=" + self.s_id
