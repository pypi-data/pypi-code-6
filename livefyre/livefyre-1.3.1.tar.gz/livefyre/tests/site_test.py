import datetime, unittest

import jwt
from livefyre import Livefyre
from livefyre.tests import LfTest


class LivefyreTestCase(unittest.TestCase):
    CHECKSUM = '4464458a10c305693b5bf4d43a384be7'
    
    def setUp(self):
        self.test = LfTest()
    
#     def test_basic_site_api(self):
#         site = Livefyre.get_network(self.test.NETWORK_NAME, self.test.NETWORK_KEY).get_site(self.test.SITE_ID, self.test.SITE_KEY)
# #         site.network.ssl = False
#         name = 'PythonCreateCollection' + str(datetime.datetime.now())
#         c_id = site.create_collection(name, name, 'http://answers.livefyre.com/PYTHON')
#         retrieved_id = site.get_collection_id(name)
#          
#         self.assertEquals(c_id, retrieved_id, 'The two ids should be the same')

    def test_build_collection_token(self):
        site = Livefyre.get_network(self.test.NETWORK_NAME, self.test.NETWORK_KEY).get_site(self.test.SITE_ID, self.test.SITE_KEY)
        
        with self.assertRaisesRegexp(AssertionError, 'url must be a full domain. ie. http://livefyre.com'):
            site.build_collection_meta_token('title', 'articleId', 'url.com')
        
        with self.assertRaisesRegexp(AssertionError, "title's length should be under 255 char"):
            site.build_collection_meta_token('1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456', 'article_id', 'http://url.com', 'tags')
        
        with self.assertRaises(AssertionError):
            site.build_collection_meta_token('title', 'articleId', 'http://livefyre.com', {'tags': 'tags', 'type': 'bad type'})
        
        token = site.build_collection_meta_token('title', 'articleId', 'https://livefyre.com')
        
        self.assertIsNotNone(token)
        
        token = site.build_collection_meta_token('title', 'articleId', 'https://livefyre.com', {'tags': 'tags', 'type': 'reviews'})
        self.assertEquals(jwt.decode(token, self.test.SITE_KEY)['type'], 'reviews')
        
        token = site.build_collection_meta_token('title', 'articleId', 'https://livefyre.com', {'type': 'liveblog'})
        self.assertEquals(jwt.decode(token, self.test.SITE_KEY)['type'], 'liveblog')
        
    def test_build_checksum(self):
        site = Livefyre.get_network(self.test.NETWORK_NAME, self.test.NETWORK_KEY).get_site(self.test.SITE_ID, self.test.SITE_KEY)
        
        with self.assertRaisesRegexp(AssertionError, 'url must be a full domain. ie. http://livefyre.com'):
            site.build_checksum('title', 'url', 'tags')
            
        with self.assertRaisesRegexp(AssertionError, "title's length should be under 255 char"):
            site.build_checksum('1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456', 'http://url.com', 'tags')
       
        checksum = site.build_checksum('title', 'https://www.url.com', 'tags')
        self.assertEquals(self.CHECKSUM, checksum, 'checksum is not correct.')
        
        
if __name__ == '__main__':
    unittest.main()