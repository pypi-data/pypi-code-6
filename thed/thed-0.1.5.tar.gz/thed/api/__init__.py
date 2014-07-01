from __future__ import unicode_literals
import itertools

from pyramid.config import Configurator
from pyramid.authorization import ACLAuthorizationPolicy

from .auth import AuthenticationPolicy
from .controllers import Controller, RestController
import decorators, predicates, requests, resources, responses
from .requests import Request
from .resources import Resource, DBModelBackedResource, ModelBackedResource
from .responses import Response


class Application(object):

    @classmethod
    def configurator_cls(cls):
        return Configurator

    @classmethod
    def request_cls(cls):
        return Request

    @classmethod
    def authentication_policy(cls):
        return AuthenticationPolicy()

    @classmethod
    def authorization_policy(cls):
        return ACLAuthorizationPolicy()

    tweens = []

    config_includes = []

    @classmethod
    def create(cls, default_settings, hook=None, includes=None, tweens=None,
               **overrides):
        """
        This function returns a Pyramid WSGI application.
        """
        app_settings = default_settings.copy()
        app_settings.update(overrides)

        config = cls.configurator_cls()(
            settings=app_settings,
            request_factory=cls.request_cls(),
            authentication_policy=cls.authentication_policy(),
            authorization_policy=cls.authorization_policy(),
        )

        for tween in itertools.chain(cls.tweens, tweens or []):
            config.add_tween(tween)

        for include in itertools.chain(cls.config_includes, includes or []):
            config.include(include)

        if hook:
            hook(config)

        config.scan()

        return config.make_wsgi_app()
