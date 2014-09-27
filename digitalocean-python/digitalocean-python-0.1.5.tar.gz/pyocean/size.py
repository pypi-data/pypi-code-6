# encoding: utf-8

from .base import Resource, ResourceIterator


class Size(Resource):
    """This class represents a Size.
    """

    def __init__(self, attrs={}):
        super(Size, self).__init__(attrs)

    def get(self, *args, **kwargs):
        raise AttributeError("'Size' object has no attribute 'get'.")

    def create(self, *args, **kwargs):
        raise AttributeError("'Size' object has no attribute 'create'.")

    def destroy(self, *args, **kwargs):
        raise AttributeError("'Size' object has no attribute 'create'.")

    def __str__(self):
        return "<Size '%s'>" % self.slug


class SizeIterator(ResourceIterator):
    """This class represents collection of the Size objects.
    """

    def __init__(self):
        super(SizeIterator, self).__init__()

