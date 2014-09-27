# encoding: utf-8

from .base import Resource, ResourceIterator
from .exceptions import InvalidResponse


class DomainRecord(Resource):
    """This class represent a Domain Record.
    """

    def __init__(self, attrs, parent):
        super(DomainRecord, self).__init__(attrs, parent)
        self._resource = 'domains/%s/records' % parent
        self._json_key = 'domain_records'

    def rename(self, name):
        path = '%s/%s' % (self._resource, self.id)
        res = self.call_api(path, method='put', data={'name': name})
        try:
            self._attrs = res['domain_record']
            return self
        except KeyError:
            raise InvalidResponse('Retrieved invalid response from the API.')

    def delete(self):
        return self.destroy()

    def __str__(self):
        if self.name:
            return "<DomainRecord '%s' (%s, %s)>" % (self.type, self.name, self.data)
        else:
            return "<DomainRecord '%s' (%s)>" % (self.type, self.data)


class DomainRecordIterator(ResourceIterator):
    """This class is the container for the Domain Record objects.
    """

    def __init__(self, domain):
        super(DomainRecordIterator, self).__init__(domain)
        self._resource = 'domains/%s/records' % domain
        self._json_key = 'domain_records'
