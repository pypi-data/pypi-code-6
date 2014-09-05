from functools import wraps

from flask import Blueprint, request

from bosun import network, settings
from .base import BaseListener


class Route(object):
    def __init__(self, path, func, instance):
        self.path = path
        self.func = func
        self.instance = instance

    def __call__(self, *args, **kwargs):
        if not self.instance:
            raise TypeError('Cannot call route without a Device instance (eg, outside a request)')

        # call the func with our instance
        return self.func(self.instance, *args, **kwargs)

    def get_url(self):
        """ Returns returns http://host:port/path """
        if not self.instance:
            raise TypeError('Cannot call get_url() without a Device instance')
        return 'http://{host}:{port}{path}'.format(
            host=network.get_my_host(self.instance.host),
            port=settings.HTTP_PORT,
            path=self.path,
        )


class RouteWrapper(object):
    def __init__(self, partial_path, func, blueprint, route_args, route_kwargs):
        if not partial_path.startswith('/'):
            partial_path = '/' + partial_path
        self.partial_path = partial_path
        self.func = func

        # store all of our blueprint / routing data
        self.blueprint = blueprint
        self.route_args = route_args
        self.route_kwargs = route_kwargs

        # this is set later, by contribute_to_class()
        self.DeviceClass = None

    def __get__(self, instance, owner):
        if not owner:
            raise Exception("Route must be attached to a class")
        # if we don't have an instance, but we're in a request context,
        # make an instance with the remote ip of this request
        if not instance and request:
            instance = owner(request.remote_addr)

        return self.get_route(instance)

    def __call__(self, *args, **kwargs):
        # This is called directly by Flask, so we need to provide the device instance from the class
        instance = self.DeviceClass(request.remote_addr)
        # then get the route for that instance
        route = self.get_route(instance)
        # and, finally, execute the route
        return route(*args, **kwargs)

    def get_route(self, instance):
        return Route(self.full_safe_path, self.func, instance)

    def contribute_to_class(self, DeviceClass):
        self.DeviceClass = DeviceClass
        # make this RouteWrapper a route for the blueprint by manually applying the route decorator to ourselves
        self.blueprint.route(self.full_safe_path, *self.route_args, **self.route_kwargs)(self)

    @property
    def full_safe_path(self):
        if not self.DeviceClass:
            raise ValueError("Must call contribute_to_class() beforing using this property")

        return '/listeners/' + self.DeviceClass.__module__ + '.' + self.DeviceClass.__name__ + self.partial_path


class HTTPListener(BaseListener):

    # make a blueprint for this so we can deal with app registration later
    # this is at the *class* level so that one instance is shared for all subclasses
    blueprint = Blueprint('HTTPListener', __name__)

    def route(self, path, *route_args, **route_kwargs):
        def decorator(func):
            return (
                # make this class instance wrap the function
                wraps(func)(
                    RouteWrapper(path, func, self.blueprint, route_args, route_kwargs)
                )
            )

        return decorator
