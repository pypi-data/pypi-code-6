import re
import json

from flask import request
from json_patch import Patch

from . import response

from json_patch import PatchError
from json_resource import ResourceNotFound, ValidationError, ResourceExists
from .authorization import UnAuthorized, Forbidden


EXCEPTION_MAP = {
    ResourceNotFound: 404,
    ResourceExists: 409,
    ValidationError: 422,
    PatchError: 400,
    ValueError: 400,
    UnAuthorized: 401,
    Forbidden: 403
}


class BaseView(object):
    rel = 'self'

    def __init__(self, resource, authorization=None):
        self.resource = resource

        if authorization:
            self.authorization = authorization

    def __call__(self, **kwargs):
        try:
            return getattr(self, request.method.lower())(**kwargs)
        except Exception, e:
            if e.__class__ in EXCEPTION_MAP:
                return response.ErrorResponse(e, EXCEPTION_MAP[e.__class__])

            raise

    @property
    def __name__(self):
        return '%s-%s' % (self.rel, self.resource.schema['id'].split('.')[0])

    def authorize(self, resource):
        try:
            self.authorization.authorize(resource)
        except AttributeError:
            pass

    @property
    def options(self):
        return {'methods': self.methods}

    @property
    def route(self):
        try:
            link = [link for link in self.resource.schema['links']
                    if link['rel'] == self.rel][0]
        except IndexError:
            return

        return re.sub(r'\{(?P<var>[\-\w]+)\}', '<path:\g<var>>', link['href'])


class ResourceView(BaseView):
    methods = ['HEAD', 'GET', 'PUT', 'PATCH', 'DELETE']

    def get(self, **kwargs):
        resource = self.resource(kwargs)
        resource.load()
        self.authorize(resource)

        return response.ResourceResponse(resource)

    def put(self, **kwargs):
        resource = self.resource(json.loads(request.data))

        if resource.rel('create'):
            upsert = False
        else:
            upsert = True

        self.authorize(resource)

        resource.save(upsert=upsert)

        return response.ResourceResponse(resource)

    def patch(self, **kwargs):
        resource = self.resource(json.loads(request.data))
        self.authorize(resource)
        resource.load()

        patch = Patch(json.loads(request.data))

        resource.patch(patch)
        resource.save()

        return response.ResourceResponse(resource)

    def delete(self, **kwargs):
        resource = self.resource(kwargs)
        self.authorize(resource)

        resource.delete()

        return response.DeleteResponse(resource)


class ResourceCreateView(BaseView):
    rel = 'create'
    methods = ['POST']

    def post(self, *args):
        resource = self.resource(json.loads(request.data))
        self.authorize(resource)

        resource.save(create=True)

        return response.ResourceCreatedResponse(resource)


class SchemaView(ResourceView):
    methods = ['GET']


class CollectionView(ResourceView):
    methods = ['GET']

    def get(self, **kwargs):
        resource = self.resource(kwargs)
        resource['meta'].update(request.args.to_dict())

        self.authorize(resource)

        return response.ResourceResponse(resource.load())
