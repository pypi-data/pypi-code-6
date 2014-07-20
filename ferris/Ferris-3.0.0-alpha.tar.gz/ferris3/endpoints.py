from __future__ import absolute_import
from protorpc import message_types
from protorpc import messages
import endpoints
from .anodi import annotated
import inspect
from . import apis
import re


def underscore(string):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def auto_class(cls=None, api=None, **kwargs):
    def auto_class_decr(cls):
        if 'resource_name' not in kwargs:
            name = underscore(cls.__name__).replace('_api', '')
            kwargs['resource_name'] = name

        if 'path' not in kwargs:
            kwargs['path'] = kwargs['resource_name']

        ep_api = apis.get(api)
        return ep_api.api_class(**kwargs)(cls)

    if cls:
        return auto_class_decr(cls)
    return auto_class_decr


def auto_method(func=None, returns=message_types.VoidMessage, name=None, http_method='GET'):
    def auto_api_decr(func):
        func_name = func.__name__ if not name else name
        func = annotated(returns=returns)(func)
        f_annotations = func.__annotations__
        f_args, f_varargs, f_kwargs, f_defaults = inspect.getargspec(func)

        if f_defaults:
            f_args_to_defaults = {f_args[len(f_args) - len(f_defaults) + n]: x for n, x in enumerate(f_defaults)}
        else:
            f_args_to_defaults = {}

        RequestMessage = f_annotations.pop('request', message_types.VoidMessage)
        ResponseMessage = f_annotations.pop('return', message_types.VoidMessage)

        RequestMessageOrContainer, request_args = annotations_to_resource_container(f_annotations, f_args_to_defaults, RequestMessage)

        ep_dec = endpoints.method(
            RequestMessageOrContainer,
            ResponseMessage,
            http_method=http_method,
            name=func_name,
            path=func_name  #TODO: include required params
        )

        def inner(self, request):
            kwargs = {}
            for arg_name in request_args:
                if hasattr(request, arg_name):
                    kwargs[arg_name] = getattr(request, arg_name)
                if arg_name in f_args_to_defaults and kwargs.get(arg_name) is None:
                    kwargs[arg_name] = f_args_to_defaults[arg_name]

            return_val = func(self, request, **kwargs)

            # return voidmessage if the return val is none
            if ResponseMessage == message_types.VoidMessage and return_val is None:
                return message_types.VoidMessage()

            return return_val

        return ep_dec(inner)

    if func:
        return auto_api_decr(func)

    return auto_api_decr


def annotations_to_resource_container(annotations, defaults, RequestMessage):
    args = {}

    if annotations:
        for n, (name, type) in enumerate(annotations.iteritems(), 1):
            required = True if name not in defaults else False

            if type == str:
                args[name] = messages.StringField(n, required=required)
            if type == int:
                args[name] = messages.IntegerField(n, required=required)
            #TODO: more types

    if args:
        return endpoints.ResourceContainer(RequestMessage, **args), args.keys()

    return RequestMessage, args.keys()
