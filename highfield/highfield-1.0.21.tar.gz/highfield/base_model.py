from pymongo import MongoClient

from highfield import naming
from highfield.errors import *
from highfield.defaults import *
from config import *

class MetaModel(type):
    def __init__(cls, name, bases, clsdict):
        cls.canonical_name = naming.class_to_canonical(name)
        cls.human_name = naming.canonical_to_words(cls.canonical_name)
        if 'database_name' in clsdict:
            cls.mongo = MongoClient(cls.database_uri)
            pass
        cls.collection = getattr(getattr(cls.mongo, cls.database_name), cls.canonical_name)
        cls.set_properties()
        super(MetaModel, cls).__init__(name, bases, clsdict)
        pass
    pass

class BaseModel(object):
    __metaclass__ = MetaModel

    database_name = default_database_name
    database_uri = default_database_uri
    properties = type('ModelProperties', (object,), {})

    class Property(object):
        def __init__(self, canonical_name, validator=None, *args, **kwargs):
            self.canonical_name = canonical_name
            self.human_name = naming.canonical_to_words(self.canonical_name)
            self.validator = validator
            for purpose, required in kwargs.iteritems():
                setattr(self, purpose, True if required else False)
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
    def new_property(cls, canonical_name, validator=None, *args, **kwargs):
        setattr(cls.properties, canonical_name, cls.Property(canonical_name, validator, *args, **kwargs))
        pass

    @classmethod
    def set_properties(cls):
        pass

    @classmethod
    def required_properties(cls, purpose):
        iterator = cls.properties.__dict__.iteritems()
        condfunc = lambda p: isinstance(p, cls.Property) and getattr(p, purpose, False)
        return [prop for c_name, prop in iterator if condfunc(prop)]

    @classmethod
    def missing_properties(cls, purpose, doc):
        c_required = [p.canonical_name for p in cls.required_properties(purpose)]
        c_missing = set(c_required) - set(doc.keys())
        return [p for p in cls.required_properties(purpose) if p.canonical_name in c_missing]

    @classmethod
    def has_required_properties(cls, purpose, doc):
        return False if len(cls.missing_properties(purpose, doc)) > 0 else True

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
    def remove(cls, **kwargs):
        return cls.collection.remove(kwargs)

    @classmethod
    def exists(cls, **kwargs):
        return True if cls.one(**kwargs) else False

    @classmethod
    def existing(cls, **kwargs):
        existing = cls.one(**kwargs)
        if not existing:
            properties = naming.enumeration([getattr(cls.properties, key).human_name for key in kwargs.keys()])
            string = 'Could not find a %s with the given %s' % (cls.human_name, properties)
            raise ValidationError({cls.canonical_name: string})
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
        for canonical_name, value in kwargs.iteritems():
            if not getattr(cls.properties, canonical_name).valid(value):
                invalid.append(getattr(cls.properties, canonical_name).human_name)
                pass
            pass
        if len(invalid):
            raise ValidationError({cls.canonical_name: 'Invalid %s' % naming.enumeration(invalid)})
            pass
        return True

    @classmethod
    def available(cls, **kwargs):
        return not cls.exists(**kwargs)
    pass
