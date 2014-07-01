from __future__ import unicode_literals
import inspect

from pyramid.view import view_defaults

from .resources import ModelBackedResource


class Controller(object):
    def __init__(self, context, request):
        super(Controller, self).__init__()
        self.request = request
        self.context = context


class RestController(Controller):
    registry = {}

    @classmethod
    def register(cls, name, **kwargs):

        def wrapped(controller):
            cls.registry[name] = controller
            controller = view_defaults(**kwargs)(controller)

            return controller

        return wrapped

    @classmethod
    def operations(cls):
        base_methods = inspect.getmembers(
            RestController, predicate=inspect.ismethod
        )
        to_exclude = [name for name, _ in base_methods]
        operation_map = {
            'index': ('GET', False),
            'create': ('POST', False),
            'show': ('GET', True),
            'update': (('PUT', 'PATCH'), True),
            'delete': ('DELETE', True),
            'upsert': ('PUT', True),
        }

        methods = inspect.getmembers(cls, predicate=inspect.ismethod)
        views = [
            method_name
            for method_name, _ in methods
            if not method_name.startswith('_')
            and method_name not in to_exclude
        ]

        for method_name in views:
            if method_name not in operation_map:
                continue
            verbs, for_resource = operation_map[method_name]
            if not isinstance(verbs, (tuple, list)):
                verbs = (verbs,)

            yield method_name, verbs, for_resource

    @classmethod
    def scan(cls, config):
        for resource, controller in cls.registry.iteritems():
            for method_name, verbs, resource in controller.operations():
                view_kwargs = dict(
                    view=controller,
                    request_method=verbs,
                    attr=method_name,
                )
                defaults = controller.__view_defaults__
                context = defaults['context']
                view_kwargs.update(defaults)
                # a resource specific view with a model associated to it will
                # use a resource predicate to lookup the object.
                if resource and issubclass(context, ModelBackedResource):
                    view_kwargs['resource'] = context.model_cls
                config.add_view(**view_kwargs)


def includeme(config):
    RestController.scan(config)
