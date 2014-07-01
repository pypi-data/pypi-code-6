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
            'upsert': ('PUT', False),
            'options': ('OPTIONS', False),
        }

        methods = inspect.getmembers(cls, predicate=inspect.ismethod)
        views = [
            (method_name, impl)
            for method_name, impl in methods
            if not method_name.startswith('_')
            and method_name not in to_exclude
        ]

        for method_name, impl in views:
            if (not hasattr(impl, 'view_config')
                    and method_name not in operation_map):
                continue
            verbs, for_resource = operation_map.get(
                method_name, (('GET', ), True)
            )
            if not isinstance(verbs, (tuple, list)):
                verbs = (verbs,)

            yield method_name, impl, verbs, for_resource

    @classmethod
    def requires_resource(cls, resource, context):
        return resource and issubclass(context, ModelBackedResource)

    @classmethod
    def configure(cls, config):
        cls_settings = getattr(cls, 'view_config', {})
        for method_name, impl, verbs, resource in cls.operations():
            # view_kwargs come from
            # 1. cls_settings (@view_config decorator on class)
            # 2. __view_defaults__ (@view_defaults decorator on class)
            # 3. impl.view_config (@view_config decorator on method)
            view_kwargs = cls_settings.copy()
            view_kwargs.update(cls.__view_defaults__)
            # set verbs from operation map, allow them to be updated from
            # view_config on the method since that will override the class
            # defaults
            view_kwargs['request_method'] = verbs
            meth_settings = getattr(impl, 'view_config', {})
            view_kwargs.update(meth_settings)
            view_kwargs.update(dict(
                view=cls,
                attr=method_name,
            ))
            context = view_kwargs.get('context', None)
            # a resource specific view with a model associated to it will
            # use a resource predicate to lookup the object.
            if cls.requires_resource(resource, context):
                view_kwargs['resource'] = context.model_cls
            config.add_view(**view_kwargs)

    @classmethod
    def scan(cls, config):
        for resource, controller in cls.registry.iteritems():
            controller.configure(config)


def includeme(config):
    RestController.scan(config)
