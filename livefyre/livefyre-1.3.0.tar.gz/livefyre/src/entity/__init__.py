from enum import Enum

try:
    import simplejson as json
except ImportError:
    import json
    

class Topic(object):
    TOPIC_IDENTIFIER = ':topic='
    
    def __init__(self, topic_id, label, created_at = None, modified_at = None):
        self.topic_id = topic_id
        self.label = label
        self.created_at = created_at
        self.modified_at = modified_at
    
    @staticmethod
    def serialize_from_json(json):
        return Topic(json['id'], json['label'], json['createdAt'], json['modifiedAt'])
    
    @staticmethod
    def create(core, topic_id, label):
        return Topic(Topic.generate_urn(core, topic_id), label)
    
    @staticmethod
    def generate_urn(core, topic_id):
        return core.get_urn() + Topic.TOPIC_IDENTIFIER + str(topic_id)
    
    def get_truncated_id(self):
        return self.topic_id[self.topic_id.find(self.TOPIC_IDENTIFIER) + len(self.TOPIC_IDENTIFIER):]
    
    def to_dict(self):
        topic_dict = {
            'id': self.topic_id,
            'label': self.label,
        }
        
        if self.created_at is not None:
            topic_dict['createdAt'] = self.created_at
        if self.modified_at is not None:
            topic_dict['modifiedAt'] = self.modified_at
        return topic_dict


class Subscription(object):
    def __init__(self, to, by, sub_type, created_at = None):
        self.to = to
        self.by = by
        self.sub_type = sub_type
        self.created_at = created_at
        
    @staticmethod
    def serialize_from_json(json):
        return Subscription(json['to'], json['by'], json['type'], json['createdAt'])
    
    def to_dict(self):
        sub_dict = {
                'to': self.to,
                'by': self.by,
                'type': self.sub_type.name,
        }
        
        if self.created_at is not None:
            sub_dict['createdAt'] = self.created_at
        return sub_dict 
        
        
class SubscriptionType(Enum):
    personalStream = 1