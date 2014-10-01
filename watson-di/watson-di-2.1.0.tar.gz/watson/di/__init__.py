# -*- coding: utf-8 -*-
__version__ = '2.1.0'


class ContainerAware(object):
    """An interface for classes that should have a container.

    Primarily used by the IocContainer, any class that subclasses it will
    have the container it was called from automatically injected into it.

    This allows classes to use the container as a service locator.

    By defining a __ioc_definition__ on the class, any class that is retrieved
    from the container that hasn't been defined can create itself based off
    the definition.

    Attributes:
        container (watson.di.container.IocContainer): A reference to the container
        __ioc_definition__ (dict): A definition required to create the object
    """
    _container = None
    __ioc_definition__ = {}

    @property
    def container(self):
        """
        Returns:
            The instance of the injected container.
        """
        return self._container

    @container.setter
    def container(self, container):
        self._container = container
