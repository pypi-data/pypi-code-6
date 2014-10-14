import copy

from .exceptions import ValidationError


class ResourceMeta(type):
    _types = []

    def __new__(cls, *args, **kwargs):
        result = type.__new__(cls, *args, **kwargs)

        if hasattr(result, 'type'):
            cls._types.append((result.type, result.blacklist, result))


        if hasattr(result, 'schema') and result.schema is not None:
            result.schema.load()

        return result


class JSONInstance(object):
    __metaclass__ = ResourceMeta
    blacklist = None

    schema = None

    def __init__(self, data=None, schema=None):
        if schema is not None:
            self.schema = schema

    @classmethod
    def load(cls, data, schema=None):
        if schema is None:
            schema = {}

        if data is True or data is False or data is None:
            return data

        for type, blacklist, cls in ResourceMeta._types:
            if blacklist and isinstance(data, blacklist):
                continue

            if isinstance(data, type):
                return cls(data, schema=schema)

        return data

    def patch(self, patch):
        patch.apply(self)

    def links(self, rel=None):

        links = copy.deepcopy(self.schema.get('links', []))
        if rel:
            links = [link for link in links if link['rel'] == rel]

        for link in links:
            try:
                link['href'] = link['href'].format(**self)
            except KeyError:
                pass

        #links.append({'href': self.schema.url, 'rel': 'describedby'})

        return links

    @classmethod
    def content_type(cls):
        return 'application/json; profile=%s' % cls.schema.url

    def rel(self, rel):
        try:
            link = self.links(rel=rel)[0]
            return link['href']
        except IndexError:
            return None

    @property
    def url(self):
        """
        Url where the instance can be retrieved

        :returns: a string with the url where the instance can be retrieved.
        This is infered from the schema.

        :raises AttributeError: when no url can be inferred
        """
        if self.schema is None:
            raise TypeError('Trying to validate instance without a schema')

        try:
            return self.rel('self')
        except IndexError:
            raise AttributeError('No self link defined for resource')

    def validate(self, schema=None):
        if schema is None:
            schema = self.schema

        if not schema.validator.is_valid(self):
            raise ValidationError(schema.validator.iter_errors(self))
