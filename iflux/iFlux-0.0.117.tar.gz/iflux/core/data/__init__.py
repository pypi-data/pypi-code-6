# Copyright 2013-2014 Flavio Garcia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import functools
import importlib
import types

def configure_connection(connection_instances, data_connected):
    if isinstance(connection_instances, types.StringTypes):
        import iflux.conf as iflux_conf
        # TODO Handler unknow connection instance here
        config = iflux_conf.data['connection']['instances'][connection_instances]
        connection_handler_config = iflux_conf.data['connection']['handlers'][config['type']]
        module = importlib.import_module(connection_handler_config['module'])
        handler_class = getattr(module, connection_handler_config['handler'])
        connection_handler = handler_class(data_connected)
        connection_handler.configure(config)
        data_connected.set_connection_handler(connection_instances, connection_handler)
        # Testing the connection
        # Without that the error will just happen during the handler execution
    elif isinstance(connection_instances, types.ListType):
        for connection_instance in connection_instances:
            configure_connection(connection_instance, data_connected)
    #TODO Throw an error here if it is not string or list

def configure(connection_instances):
    def f_wrapper(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            configure_connection(connection_instances, self)
            return method(self, *args, **kwargs)
        return wrapper
    return f_wrapper


class DataConnectedMixin(object):
    """
    This mixin includes a configured session engine to an iflux application. The engine will be used by the session
    reads and writes triggered by the current handler.

    Example:
    >>> class MyClass(..., DataConnectedMixin):

    Refer to SessionEngine documentation in order to know which methods are available.
    """
    @property
    def connection_handlers(self):
        """Returns the data connections holded by the data connected object
        """
        return get_connection_handlers(self, '__connection_handlers')
    

    def get_connection_handler(self, name):
        """Returns a data connection instance
        """
        return self.connection_handlers[name]

    def set_connection_handler(self, name, connection_handler):
        self.connection_handlers[name] = connection_handler


class DataConnectedHolderMixin(object):

    @property
    def data_connected(self):
        return self.get_data_connected()

    def get_data_connected(self):
        return None


def get_connection_handlers(obj, connection_handlers_attribute):
    if not hasattr(obj, connection_handlers_attribute):
        setattr(obj, connection_handlers_attribute, {})
    return getattr(obj, connection_handlers_attribute)


def served_by(service, connection_name):

    def f_wrapper(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            service_name = service.__name__
            first = True
            service_attribute = ''
            for s in service_name:
                if s.isupper():
                    if first:
                        service_attribute = ''.join([service_attribute, s.lower()])
                    else:
                        service_attribute = ''.join([service_attribute, '_', s.lower()])
                else:
                    service_attribute = ''.join([service_attribute, s])
                first = False
            setattr(self, service_attribute, service(self.data_connected.connection_handlers[connection_name]))
            return method(self, *args, **kwargs)

        return wrapper
    return f_wrapper
