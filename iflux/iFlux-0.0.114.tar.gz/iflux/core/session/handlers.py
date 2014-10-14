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

import iflux.conf
from iflux.util import file
import os


class FileSessionHandler(iflux.core.session.SessionHandler):
    """
    Session handler that deals with file data stored in files.

    The FileSessionHandler blocks tornado requests as long we are reading and
    writing files. We will try to minimize the blocking effect but by now don't
    use this for high traffic sites.
    """

    path = None

    def configure(self):
        if os.path.exists(iflux.conf.session['path']):
            self.path = iflux.conf.session['path']
        else:
            # TODO: Need to think about this. I don't know if this is a
            # good behaviour. Maybe just crash the app here
            # or disable the session with a good warning.
            self.path = '/tmp'

    def create_session(self, session_id, data):
        # TODO: What could possibly go wrong here? Let's handle it!
        session_file = os.path.join(self.path, self.__get_filename(session_id))
        if os.path.exists(iflux.conf.session['path']):
            file.touch(session_file)
            file.write(session_file, data)

    def read_stored_session(self, session_id):
        session_file = os.path.join(self.path, self.__get_filename(session_id))
        return file.read(session_file)

    def write_stored_session(self, session_id, data):
        session_file = os.path.join(self.path, self.__get_filename(session_id))
        file.write(session_file, data)

    def is_session_stored(self, session_id):
        return os.path.isfile(os.path.join(self.path, self.__get_filename(
            session_id)))

    def __get_filename(self, session_id):
        return 'iflux_%s.sess' % session_id


class RedisSessionHandler(iflux.core.session.SessionHandler):
    """
    Session handler that deals with file data stored  in a redis database.
    """

    connection_handler = None

    def configure(self):
        import redis
        configuration = iflux.conf.session['redis_configuration']
        self.connection_handler = self.engine.get_session_aware_instance().\
            get_connection_handler(configuration['connection'])

    def create_session(self, session_id, data):
        self.write_stored_session(session_id, data)

    def read_stored_session(self, session_id):
        return self.connection_handler.get_connection().get(
            self.__get_key(session_id))

    def write_stored_session(self, session_id, data):
        self.connection_handler.get_connection().set(
            self.__get_key(session_id), data)

    def is_session_stored(self, session_id):
        return self.connection_handler.get_connection().get(
            self.__get_key(session_id)) is not None

    def __get_key(self, session_id):
        return '%s:%s' % (iflux.conf.session['redis_prefix'], session_id)

