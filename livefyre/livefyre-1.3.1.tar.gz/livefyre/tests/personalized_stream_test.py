import unittest

from livefyre import Livefyre
from livefyre.tests import LfTest
from livefyre.src.entity import Topic
from livefyre.src.api.personalizedstream import PersonalizedStream
from livefyre.src.factory import CursorFactory


class LivefyreTestCase():#unittest.TestCase):
    def setUp(self):
        self.test = LfTest()
        self.network = Livefyre.get_network(self.test.NETWORK_NAME, self.test.NETWORK_KEY)
#         self.network.ssl = False
        self.site = self.network.get_site(self.test.SITE_ID, self.test.SITE_KEY)
        

    def test_network_topic(self):
        topic = PersonalizedStream.create_or_update_topic(self.network, '1', 'UN')
        topic = PersonalizedStream.get_topic(self.network, 1)
        deleted = PersonalizedStream.delete_topic(self.network, topic)
        topics = PersonalizedStream.get_topics(self.network)
     
     
    def test_site_topic(self):
        topic = PersonalizedStream.create_or_update_topic(self.site, '2', 'DEUX')
        topic = PersonalizedStream.get_topic(self.site, 2)
        deleted = PersonalizedStream.delete_topic(self.site, topic)
        topics = PersonalizedStream.get_topics(self.site)
     
     
    def test_network_topics(self):
        topics = {'1': 'UN', '2': 'DEUX'}
        returned_topics = PersonalizedStream.create_or_update_topics(self.network, topics)
        returned_topics = PersonalizedStream.get_topics(self.network)
        deleted = PersonalizedStream.delete_topics(self.network, returned_topics)
        topics = PersonalizedStream.get_topics(self.network)
     
     
    def test_site_topics(self):
        topics = {'1': 'UN', '2': 'DEUX'}
        returned_topics = PersonalizedStream.create_or_update_topics(self.site, topics)
        returned_topics = PersonalizedStream.get_topics(self.site)
        deleted = PersonalizedStream.delete_topics(self.site, returned_topics)
        topics = PersonalizedStream.get_topics(self.site)
     
     
    def test_collection_topics(self):
        topic_dict = {'1': 'UN', '2': 'DEUX'}
        topics = PersonalizedStream.create_or_update_topics(self.site, topic_dict)
         
        added = PersonalizedStream.add_collection_topics(self.site, self.test.COLLECTION_ID, topics)
        added, removed = PersonalizedStream.replace_collection_topics(self.site, self.test.COLLECTION_ID, [topics[0]])
        removed = PersonalizedStream.remove_collection_topics(self.site, self.test.COLLECTION_ID, [topics[0]])
        collection_topics = PersonalizedStream.get_collection_topics(self.site, self.test.COLLECTION_ID)
         
        PersonalizedStream.delete_topics(self.site, topics)

     
    def test_subscription_api(self):
        user_token = self.network.build_user_auth_token(self.test.USER_ID, self.test.USER_ID + '@' + self.test.NETWORK_NAME, self.network.DEFAULT_EXPIRES)
        topic_dict = {'1': 'UN', '2': 'DEUX'}
        topics = PersonalizedStream.create_or_update_topics(self.network, topic_dict)
         
        added = PersonalizedStream.add_subscriptions(self.network, user_token, topics)
        user_subs = PersonalizedStream.get_subscriptions(self.network, self.test.USER_ID)
        added, removed = PersonalizedStream.replace_subscriptions(self.network, user_token, [topics[1]])
        user_subs = PersonalizedStream.get_subscribers(self.network, topics[1])
        removed = PersonalizedStream.remove_subscriptions(self.network, user_token, [topics[1]])
         
        PersonalizedStream.delete_topics(self.network, topics)
    
    def test_timeline_cursor(self):
        topic = Topic.create(self.network, "1", "UN")
        
        cursor = CursorFactory.get_topic_stream_cursor(self.network, topic)
        data1 = cursor.previous()
        data2 = cursor.next()

        self.assertEquals(data1['data'], data2['data'])
    
        
if __name__ == '__main__':
    unittest.main()