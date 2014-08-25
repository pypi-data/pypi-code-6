from __future__ import unicode_literals


from distributed_task import settings

try:
    from django.utils.module_loading import import_string
except ImportError:
    """
    Backward compatibility to Django < 1.7
    """
    from ..utils.module_loading import import_string


def get_broker():
    return factory.get_backend()


class BrokerBackendFactory(object):

    b = None

    def get_backend(self):
        if self.b is None:
            self.load_backend()

        return self.b

    def load_backend(self):
        path = getattr(settings, 'BROKER_BACKEND')

        Backend = import_string(path)
        self.b = Backend()


factory = BrokerBackendFactory()