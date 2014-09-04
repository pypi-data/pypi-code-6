from django.forms import fields


class BaseField(fields.Field):

    def search(self, s, name, data):
        raise NotImplementedError


class Query(BaseField):

    fields = ['_all']

    def __init__(self, fields=None, **kwargs):
        super(Query, self).__init__(**kwargs)
        if fields is not None:
            self.fields = fields

    def search(self, s, name, data):
        value = data[name]
        if not value:
            return s

        fields = self.fields
        if len(fields) == 1:
            query = {
                'match': {
                    fields[0]: value,
                }
            }
        else:
            query = {
                'multi_match': {
                    'query': value,
                    'fields': fields,
                }
            }

        return s.query_raw(query)


class Filter(BaseField):

    field = None

    def __init__(self, field=None, **kwargs):
        super(Filter, self).__init__(**kwargs)
        if field is not None:
            self.field = field

    def search(self, s, name, data):
        field = self.field or name
        value = data[name]
        s.filter(**{field: value})
