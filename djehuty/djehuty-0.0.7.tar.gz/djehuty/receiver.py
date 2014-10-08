import abc

from cornice import Service as CorniceService


class Receiver(CorniceService):

    __metaclass__ = abc.ABCMeta

    def __init__(self,
                 name=None, path=None, description=None, cors_policy=None, depth=0,
                 **kwargs):

        name = name or self.__class__.__name__.lower()

        CorniceService.__init__(
            self,
            name=name,
            path=path or '/{}'.format(name),
            description=description or 'service for {}'.format(path),
            cors_policy=cors_policy,
            depth=depth + 2,
            validators=self.validate,
            **kwargs
        )

        self.post()(self.receive)

    def validate(self, request):
        pass

    @abc.abstractmethod
    def receive(self, request):
        return {}
