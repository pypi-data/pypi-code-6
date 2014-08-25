# -*- coding: utf-8 -*-

import abc

from cStringIO import StringIO
from contextlib import closing

from cornice import Service as CorniceService

from djehuty.app import App
from djehuty.command import Result


class Service(CorniceService):

    __metaclass__ = abc.ABCMeta

    def __init__(self,
                 name=None, path=None, description=None, cors_policy=None, depth=1,
                 args_def=None, **kwargs):

        self.__args_def = args_def or {}
        name = name or self.__class__.__name__.lower()

        CorniceService.__init__(
            self,
            name=name,
            path=path or u'/{}'.format(name),
            description=description or u'service for {}'.format(path),
            cors_policy=cors_policy,
            depth=depth + 1,
            validators=self.validate,
            **kwargs
        )

        self.post()(self.__post)

    def validate(self, request):
        pass

    def get_user(self, request):
        return self.get_service_argument('user', request)

    def get_room(self, request):
        return self.get_service_argument('room', request)

    @abc.abstractmethod
    def get_service_argument(self, arg_name, request):
        return ''

    @abc.abstractmethod
    def make_command_line(self, request):
        return []

    @abc.abstractmethod
    def make_response(self, result):
        return {}

    def __post(self, request):
        with closing(StringIO()) as stdout, closing(StringIO()) as stderr:
            app = App(self.__args_def, stdout=stdout, stderr=stderr)
            result = app.run(self.__make_service_command_line(app.args_def, request))
            if isinstance(result, Result):
                result = result.value
            elif result == 0:
                result = stdout.getvalue()
            else:
                result = stderr.getvalue()
        return self.make_response(result)

    def __make_service_command_line(self, args_def, request):
        return [
            item
            for arg_name in args_def.keys()
            for item in self.__get_service_argument(arg_name, request)
        ] + self.make_command_line(request)

    def __get_service_argument(self, arg_name, request):
        return self.__make_argument(
            arg_name,
            self.get_service_argument(arg_name, request)
        )

    @staticmethod
    def __make_argument(arg_name, value):
        return ['--{}'.format(arg_name), value] if arg_name and value else []
