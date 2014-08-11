import requests, jwt

from livefyre.src.api import get_lf_token_header, Domain
from livefyre.src.entity import Topic, Subscription, SubscriptionType

try:
    import simplejson as json
except ImportError:
    import json


def get_url(core):
    return PersonalizedStream.BASE_URL.format(Domain.quill(core))


class PersonalizedStream(object):
    BASE_URL = '{}/api/v4'
    STREAM_BASE_URL = '{}/api/v4'
    
    TOPIC_PATH = '/{}/'
    MULTIPLE_TOPIC_PATH = '/{}:topics/';
    COLLECTION_TOPICS_PATH = '/{}:collection={}:topics/';
    USER_SUBSCRIPTION_PATH = '/{}:subscriptions/';
    TOPIC_SUBSCRIPTION_PATH = '/{}:subscribers/';
    TIMELINE_PATH = '/timeline/';
    
    
    @staticmethod
    def get_topic(core, topic_id):
        url = get_url(core) + PersonalizedStream.TOPIC_PATH.format(Topic.generate_urn(core, topic_id))
        headers = get_lf_token_header(core)

        response = requests.get(url, headers = headers)
        data = response.json()['data']
        
        return Topic.serialize_from_json(data['topic']) if 'topic' in data else None


    @staticmethod
    def create_or_update_topic(core, topic_id, label):
        return PersonalizedStream.create_or_update_topics(core, { topic_id: label })[0]
        
    
    @staticmethod
    def delete_topic(core, topic):
        return PersonalizedStream.delete_topics(core, [topic]) == 1


    @staticmethod
    def get_topics(core, limit = 100, offset = 0):
        url = get_url(core) + PersonalizedStream.MULTIPLE_TOPIC_PATH.format(core.get_urn())
        headers = get_lf_token_header(core)

        response = requests.get(url, params = {'limit': limit, 'offset': offset}, headers = headers)
        data = response.json()['data']
        
        return [Topic.serialize_from_json(x) for x in data['topics']] if 'topics' in data else []


    @staticmethod
    def create_or_update_topics(core, topic_map):
        topics = []
        try:
            topics = [Topic.create(core, k, v) for k, v in topic_map.iteritems()]
        except:
            topics = [Topic.create(core, k, v) for k, v in topic_map.items()]
        
        for topic in topics:
            assert topic.label and len(topic.label) <= 128, 'topic label should not be empty and have 128 or less characters'
        
        url = get_url(core) + PersonalizedStream.MULTIPLE_TOPIC_PATH.format(core.get_urn())
        form = json.dumps({'topics': [x.to_dict() for x in topics]})
        headers = get_lf_token_header(core)
        headers['Content-Type'] = 'application/json'
        
        response = requests.post(url, data = form, headers = headers)
        response.json()['data']
        
        return topics
        
        
    @staticmethod
    def delete_topics(core, topics):
        url = get_url(core) + PersonalizedStream.MULTIPLE_TOPIC_PATH.format(core.get_urn())
        form = json.dumps({'delete': [x.topic_id for x in topics]})
        headers = get_lf_token_header(core)
        headers['Content-Type'] = 'application/json'
        
        response = requests.patch(url, data = form, headers = headers)
        data = response.json()['data']
        
        return data['deleted'] if 'deleted' in data else 0
    
    
    @staticmethod
    def get_collection_topics(site, collection_id):
        url = get_url(site) + PersonalizedStream.COLLECTION_TOPICS_PATH.format(site.get_urn(), collection_id)
        headers = get_lf_token_header(site)

        response = requests.get(url, headers = headers)
        data = response.json()['data']
        
        return data['topicIds'] if 'topicIds' in data else None


    @staticmethod
    def add_collection_topics(site, collection_id, topics):
        url = get_url(site) + PersonalizedStream.COLLECTION_TOPICS_PATH.format(site.get_urn(), collection_id)
        form = json.dumps({'topicIds': [x.topic_id for x in topics]})
        headers = get_lf_token_header(site)
        headers['Content-Type'] = 'application/json'
        
        response = requests.post(url, data = form, headers = headers)
        data = response.json()['data']

        return data['added'] if 'added' in data else 0
    
    
    @staticmethod
    def replace_collection_topics(site, collection_id, topics):
        url = get_url(site) + PersonalizedStream.COLLECTION_TOPICS_PATH.format(site.get_urn(), collection_id)
        form = json.dumps({'topicIds': [x.topic_id for x in topics]})
        headers = get_lf_token_header(site)
        headers['Content-Type'] = 'application/json'
        
        response = requests.put(url, data = form, headers = headers)
        data = response.json()['data']
        
        added = data['added'] if 'added' in data else 0
        removed = data['removed'] if 'removed' in data else 0
            
        return added, removed
        
        
    @staticmethod
    def remove_collection_topics(site, collection_id, topics):
        url = get_url(site) + PersonalizedStream.COLLECTION_TOPICS_PATH.format(site.get_urn(), collection_id)
        form = json.dumps({'delete': [x.topic_id for x in topics]})
        headers = get_lf_token_header(site)
        headers['Content-Type'] = 'application/json'
        
        response = requests.patch(url, data = form, headers = headers)
        data = response.json()['data']
    
        return data['removed'] if 'removed' in data else 0
    
    
    @staticmethod
    def get_subscriptions(network, user_id):
        url = get_url(network) + PersonalizedStream.USER_SUBSCRIPTION_PATH.format(network.get_user_urn(user_id))
        headers = get_lf_token_header(network)

        response = requests.get(url, headers = headers)
        data = response.json()['data']
        
        return [Subscription.serialize_from_json(x) for x in data['subscriptions']] if 'subscriptions' in data else []


    @staticmethod
    def add_subscriptions(network, user_token, topics):
        user_id = jwt.decode(user_token, network.key)['user_id']
        user_urn = network.get_user_urn(user_id)
        url = get_url(network) + PersonalizedStream.USER_SUBSCRIPTION_PATH.format(user_urn)
        form = json.dumps({'subscriptions': [Subscription(x.topic_id, user_urn, SubscriptionType.personalStream).to_dict() for x in topics]})
        headers = get_lf_token_header(network, user_token)
        headers['Content-Type'] = 'application/json'
        
        response = requests.post(url, data = form, headers = headers)
        data = response.json()['data']
        
        return data['added'] if 'added' in data else 0
    
    
    @staticmethod
    def replace_subscriptions(network, user_token, topics):
        user_id = jwt.decode(user_token, network.key)['user_id']
        user_urn = network.get_user_urn(user_id)
        url = get_url(network) + PersonalizedStream.USER_SUBSCRIPTION_PATH.format(user_urn)
        form = json.dumps({'subscriptions': [Subscription(x.topic_id, user_urn, SubscriptionType.personalStream).to_dict() for x in topics]})
        headers = get_lf_token_header(network, user_token)
        headers['Content-Type'] = 'application/json'
        
        response = requests.put(url, data = form, headers = headers)
        data = response.json()['data']
        
        added = data['added'] if 'added' in data else 0
        removed = data['removed'] if 'removed' in data else 0
            
        return added, removed
        
        
    @staticmethod
    def remove_subscriptions(network, user_token, topics):
        user_id = jwt.decode(user_token, network.key)['user_id']
        user_urn = network.get_user_urn(user_id)
        url = get_url(network) + PersonalizedStream.USER_SUBSCRIPTION_PATH.format(user_urn)
        form = json.dumps({'delete': [Subscription(x.topic_id, user_urn, SubscriptionType.personalStream).to_dict() for x in topics]})
        headers = get_lf_token_header(network, user_token)
        headers['Content-Type'] = 'application/json'
        
        response = requests.patch(url, data = form, headers = headers)
        data = response.json()['data']
    
        return data['removed'] if 'removed' in data else 0
    
    
    @staticmethod
    def get_subscribers(network, topic, limit = 100, offset = 0):
        url = get_url(network) + PersonalizedStream.TOPIC_SUBSCRIPTION_PATH.format(topic.topic_id)
        headers = get_lf_token_header(network)

        response = requests.get(url, params = {'limit': limit, 'offset': offset}, headers = headers)
        data = response.json()['data']
        
        
        return [Subscription.serialize_from_json(x) for x in data['subscriptions']] if 'subscriptions' in data else []
    
    
    @staticmethod
    def get_timeline_stream(core, resource, limit, until, since):
        url = PersonalizedStream.STREAM_BASE_URL.format(Domain.bootstrap(core)) + PersonalizedStream.TIMELINE_PATH
        headers = get_lf_token_header(core)
        params = {'resource': resource, 'limit': limit}
        if until is not None:
            params['until'] = until
        elif since is not None:
            params['since'] = since

        return requests.get(url, params = params, headers = headers).json()
    