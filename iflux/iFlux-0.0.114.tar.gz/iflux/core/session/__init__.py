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
import iflux.conf
import importlib
from iflux.util import random_string


# TODO Send to util!?
def get_class_from_conf(conf):
    module = importlib.import_module(conf['module'])
    return getattr(module, conf['class'])

class SessionEngine(object):
    """SessionEngine provides to an application session support.
    """

    session_handler = None
    session_encoder = None
    session_aware_instance = None

    def __init__(self, session_aware_instance):
        # TODO: By the way session could be disabled. How do we 
        # handle that?
        # TODO: check if session type exists. Maybe disable it if type is not
        # defined. We need to inform the error here
        handler_class = get_class_from_conf(
            iflux.conf.session['handlers'][iflux.conf.session['type']]
        ) 
        self.session_aware_instance = session_aware_instance
        self.session_handler = handler_class(self)
        self.session_handler.set_settings({})
        self.session_handler.configure()

        encoder_class = get_class_from_conf(
            iflux.conf.session['encoding']['encoders'][
                iflux.conf.session['encoding']['type']
            ]
        )
        self.session_encoder = encoder_class()

    def get_session(self, request_handler):
        """Returns a valid session object. This session is handler by the
        session handler defined on the application configuration.
        """
        session = Session()
        if iflux.conf.session['enabled']:
            cookie_created_on_request = False
            session_id = self.session_handler.get_session_id_cookie(
                request_handler)
            if session_id is None:
                cookie_created_on_request = True
                session_id = self.session_handler.create_session_id_cookie(
                    request_handler)
                self.session_handler.create_session(
                    session_id, self.encode_session_data(session.data))
            # TODO: Check if the session is stored
            if not self.session_handler.is_session_stored(session_id):
                if not cookie_created_on_request:
                    # Regenerating the session id. Because the
                    # cookie was not created during at the same request
                    # the file is being created.
                    session_id = self.session_handler.create_session_id_cookie(
                        request_handler)
                    self.session_handler.create_session(session_id,
                        self.encode_session_data(session.data))
            session_data = self.decode_session_data(
                self.session_handler.read_stored_session(session_id))
            session = Session(session_data)
            session.id = session_id
            return session

    def store_session(self, request_handler):
        """Sends the session data to be stored by the session handler defined
        on the application configuration.
        """
        if iflux.conf.session['enabled']:
            session_id = request_handler.session.id
            encoded_session_data = self.encode_session_data(
                request_handler.session.data)
            self.session_handler.write_stored_session(session_id,
                                                      encoded_session_data)

    def encode_session_data(self, data):
        return self.session_encoder.encode(data)

    def decode_session_data(self, data):
        return self.session_encoder.decode(data)

    def get_session_aware_instance(self):
        return self.session_aware_instance


class SessionEngineMixin(object):
    """
    This mixin includes a configured session engine to an iflux application.
    The engine will be used by the session reads and writes triggered by
    the current handler.

    Example:
    >>> class MyApplication(iflux.core.Application, SessionEngineMixin):

    Refer to SessionEngine documentation in order to know which methods are
    available.
    """

    @property
    def session_engine(self):
        """
        Returns a SessionManager instance
        """
        return create_session_engine(self, '__session_engine', SessionEngine)


class Session(object):

    id = None

    data = None

    def __init__(self, data={}):
        self.data = data

    def get(self, key):
        """
        Returns the value from the session data by a given key
        """
        if self.data.has_key(key):
            return self.data[key]
        return None

    def set(self, key, value):
        """
        Set a value into the session data labeled by a given key
        """
        self.data[key] = value


class SessionHandler(object):

    engine = None

    settings = None

    def __init__(self, engine):
        self.engine = engine
        self.settings = {}

    def create_session(self, session_id, data):
        pass

    def read_stored_session(self, session_id):
        pass

    def write_stored_session(self, session_id, data):
        pass

    def create_session_id_cookie(self, request_handler):
        session_id = self.__generate_session_id()
        request_handler.set_cookie(iflux.conf.session['name'], session_id,
                                   **self.__session_id_cookie_settings())
        return session_id

    def get_session_id_cookie(self, request_handler):
        return request_handler.get_cookie(iflux.conf.session['name'])

    def is_session_stored(self, session_id):
        pass

    def configure(self):
        pass

    def set_settings(self, settings):
        self.settings = settings

    def __session_id_cookie_settings(self):
        """
        Defines some settings to be used with the session id cookie
        """
        cookie_settings = {}
        cookie_settings.setdefault('expires', None)
        cookie_settings.setdefault('expires_days', None)
        return cookie_settings

    def __generate_session_id(self):
        # TODO we should make this generation more secure
        # TODO I think this is a good place to put a customized session
        # generator based on the configuration
        return random_string(64)


def create_session_engine(obj, session_engine_attribute, session_engine_class):
    if not hasattr(obj, session_engine_attribute):
        session_engine_instance = session_engine_class(obj)
        setattr(obj, session_engine_attribute, session_engine_instance)
    return getattr(obj, session_engine_attribute)


def read(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        session = self.application.session_engine.get_session(self)
        self.session = session
        return method(self, *args, **kwargs)
    return wrapper


def write(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        self.application.session_engine.store_session(self)
        return method(self, *args, **kwargs)
    return wrapper


class SessionEncoder(object):
    
    def encode(self, data):
        return data

    def decode(self, data):
        return data


class PickeSessionEncoder(SessionEncoder):

    def encode(self, data):
        import pickle
        return pickle.dumps(data, 2)

    def decode(self, data):
        import pickle
        return pickle.loads(data)
