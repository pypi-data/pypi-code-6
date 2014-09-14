from pymongo import MongoClient

from highfield import naming
from highfield.defaults import *
from config import *

mongo = MongoClient(mongodb_uri)

class MetaModel(type):
    def __init__(cls, name, bases, clsdict):
        cls.canonical_name = naming.class_to_canonical(name)
        cls.human_name = naming.canonical_to_words(cls.canonical_name)
        cls.collection = getattr(getattr(mongo, db_name), cls.canonical_name)
        cls.properties = type('ModelProperties', (object,), {})
        cls.set_properties()
        super(MetaModel, cls).__init__(name, bases, clsdict)
        pass
    pass

class BaseModel(object):
    __metaclass__ = MetaModel

    class Property(object):
        def __init__(self, canonical_name, validator=None):
            if '*' in canonical_name:
                parts = canonical_name.split('*', 1)
                self.canonical_group = parts[0]
                self.human_group = naming.canonical_to_words(self.canonical_group)
                self.canonical_name = parts[1].lstrip('_')
                pass
            else:
                self.canonical_name = canonical_name
                pass
            self.human_name = naming.canonical_to_words(self.canonical_name)
            self.validator = validator
            pass

        def valid(self, value):
            if not self.validator:
                return True
            elif hasattr(self.validator, 'match'):
                if self.validator.match(value):
                    return True
                pass
            elif hasattr(self.validator, '__call__'):
                if self.validator(value):
                    return True
                pass
            return False
        pass

    @classmethod
    def new_property(cls, canonical_name, validator=None):
        setattr(cls.properties, canonical_name, cls.Property(canonical_name, validator))
        pass

    @classmethod
    def set_properties(cls):
        pass

    @classmethod
    def extract_properties(cls, doc):
        result = {}
        for k, v in cls.properties.__dict__.iteritems():
            if isinstance(v, cls.Property) and k in doc:
                result[k] = doc[k]
                pass
            pass
        return result

    @classmethod
    def such(cls, that, limit=25, page=1):
        skip = limit * (page - 1)
        return [item for item in cls.collection.find(that,
                                                     skip=skip,
                                                     limit=limit)]

    @classmethod
    def every(cls, max=25, page=1):
        return cls.such({}, limit=limit, page=page)

    @classmethod
    def one(cls, **kwargs):
        return cls.collection.find_one(kwargs)

    @classmethod
    def update(cls, query, update, upsert=True, new=False):
        return cls.collection.find_and_modify(query=query,
                                              update=update,
                                              upsert=upsert,
                                              new=new)

    @classmethod
    def new(cls, doc):
        return cls.collection.insert(doc)

    @classmethod
    def exists(cls, **kwargs):
        return True if cls.one(**kwargs) else False

    @classmethod
    def existing(cls, **kwargs):
        existing = cls.one(**kwargs)
        if not existing:
            properties = naming.enumeration([getattr(cls.properties, key).human_name for key in kwargs.keys()])
            string = 'Could not find a %s with the given %s' % (cls.human_name, properties)
            raise cls.namespace.ValidationError({cls.canonical_name: string})
            pass
        return existing

    @classmethod
    def validates(cls, **kwargs):
        for (k, v) in kwargs.iteritems():
            if not getattr(cls.properties, k).valid(v):
                return False
            pass
        return True

    @classmethod
    def validate(cls, **kwargs):
        invalid = []
        for (k, v) in kwargs.iteritems():
            if not getattr(cls.properties, k).valid(v):
                invalid.append(cls.properties[k].human_name)
                pass
            pass
        if len(invalid):
            raise cls.namespace.ValidationError({cls.canonical_name: 'Invalid %s' % naming.enumeration(invalid)})
            pass
        return True

    @classmethod
    def available(cls, **kwargs):
        return not cls.exists(**kwargs)
    pass
