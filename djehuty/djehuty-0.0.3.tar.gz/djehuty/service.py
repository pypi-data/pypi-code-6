# -*- coding: utf-8 -*-

import abc

from cornice import Service as CorniceService

from djehuty.app import App


class Service(CorniceService):

    __metaclass__ = abc.ABCMeta

    def __init__(self, name=None, path=None, description=None, cors_policy=None, depth=1, **kwargs):

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

    @abc.abstractmethod
    def get_user(self, request):
        return ''

    @abc.abstractmethod
    def get_room(self, request):
        return ''

    @abc.abstractmethod
    def make_command_line(self, request):
        return []

    @abc.abstractmethod
    def make_response(self, result):
        return {}

    def __make_argument(self, request):
        return self.__make_service_argument('u', self.get_user(request)) + self.__make_service_argument('r', self.get_room(request)) + self.make_command_line(request)

    def __post(self, request):
        return self.make_response(App.run_and_get_result(self.__make_argument(request)))

    @staticmethod
    def __make_service_argument(arg_name, value):
        return ['-{}'.format(arg_name), value] if arg_name else []
