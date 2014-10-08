import abc

from cStringIO import StringIO
from contextlib import closing

from djehuty.receiver import Receiver

from djehuty.app import App
from djehuty.command import Result


class Service(Receiver):

    def __init__(self,
                 name=None, path=None, description=None, cors_policy=None, depth=0,
                 args_def=None, **kwargs):

        self.__args_def = args_def or {}

        Receiver.__init__(self, name, path, description, cors_policy, depth + 1, **kwargs)

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

    def receive(self, request):
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
