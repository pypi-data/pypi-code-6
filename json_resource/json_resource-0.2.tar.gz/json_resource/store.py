from json_resource import Object, ResourceMeta
from json_resource.queryset import QuerySet


class StoredResourceMeta(ResourceMeta):
    def __new__(cls, name, bases, dct):
        result = super(StoredResourceMeta, cls).__new__(cls, name, bases, dct)

        if result.schema and not hasattr(result, 'objects'):
            result.objects = QuerySet(
                result
            )

        return result


class Resource(Object):
    __metaclass__ = StoredResourceMeta

    def __init__(self, *args, **kwargs):
        self.meta = kwargs.pop('meta', {})

        super(Resource, self).__init__(*args, **kwargs)

    @property
    def _id(self):
        return self.url

    @classmethod
    def collection(cls):
        return cls.db[cls.schema['id']]

    def load(self):
        self.objects.load(self)

        return self

    def save(self, validate=True, upsert=True, create=False):
        if validate:
            self.validate()

        if create:
            self.objects.insert(self, validate=validate)
        else:
            self.objects.save(self, validate=validate, upsert=upsert)

    def delete(self):
        self.objects.delete(self)

    @property
    def exists(self):
        data = self.collection().find_one({'_id': self.url})

        if not data:
            return False
        else:
            return True
