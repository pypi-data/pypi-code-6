import ConfigParser
from enum import Enum


class LfTest:
    NETWORK_NAME = '<NETWORK-NAME>'
    NETWORK_KEY = '<NETWORK-KEY>'
    SITE_ID = '<SITE-ID>'
    SITE_KEY = '<SITE-KEY>'
    COLLECTION_ID = '<COLLECTION-ID>'
    USER_ID = '<USER-ID>'
    ARTICLE_ID = '<ARTICLE-ID>'
    
    def __init__(self):
        self.set_prop_values(LfEnvironments.PROD)

    def set_prop_values(self, env):
        config = ConfigParser.RawConfigParser()
        config.read('test.properties')
        
        self.NETWORK_NAME = config.get(env.value, 'NETWORK_NAME')
        self.NETWORK_KEY = config.get(env.value, 'NETWORK_KEY')
        self.SITE_ID = config.get(env.value, 'SITE_ID')
        self.SITE_KEY = config.get(env.value, 'SITE_KEY')
        self.COLLECTION_ID = config.get(env.value, 'COLLECTION_ID')
        self.USER_ID = config.get(env.value, 'USER_ID')
        self.ARTICLE_ID = config.get(env.value, 'ARTICLE_ID')
        
            
class LfEnvironments(Enum):
    QA = 'qa'
    UAT = 'uat'
    PROD = 'prod'