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
from tornado.web import HTTPError


# Security constants
DEFAULT_LOGIN_URL = '/login'
DEFAULT_LOGIN_PROCESS_URL = ''

try:
    import urlparse  # py2
except ImportError:
    import urllib.parse as urlparse  # py3

try:
    from urllib import urlencode  # py2
except ImportError:
    from urllib.parse import urlencode  # py3


class Credential(object):

    __authenticated = False

    def is_authenticated(self):
        return self.__authenticated

    def set_authenticated(self, authenticated):
        self.__authenticated = authenticated


class Secured(object):
    @property
    def credential(self):
        """
        Returns a SessionManager instance
        """
        return self.__get_credential(self, '__credential_manager', Credential)

    def __get_credential(self, obj, credential_attribute, credential_class):
        if not hasattr(obj, credential_attribute):
            setattr(obj, credential_attribute, credential_class())
        return getattr(obj, credential_attribute)

def secured(cls):
   for name, method in cls.__dict__.iteritems():
        if hasattr(method, "use_class"):
            # do something with the method and class
            print name, cls
   return cls


def identify(method):
    """
    Decorator that gets all security data from the session and adds to the credential.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        # TODO finish the session -> credential identification
        if self.session.get('UserId') is None:
            self.credential.set_authenticated(False)
        else:
            self.credential.set_authenticated(True)
        return method(self, *args, **kwargs)
    return wrapper


def authenticated(method):
    """
    Decorator that checks if the user is authenticated. If not send the user to the login page.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        is_authenticated = False
        if hasattr(self, 'credential'):
            if self.credition.is_authenticated():
                is_authenticated = True
        if not is_authenticated:
            if self.request.method in ("GET", "HEAD"):
                try:
                    url = self.get_login_url()
                except Exception:
                    # If url is not defined an exception will be raised
                    url = DEFAULT_LOGIN_URL
                if urlparse.urlsplit(url).scheme:
                    # if login url is absolute, make next absolute too
                    self.session.set('next_url', self.request.full_url())
                else:
                    self.session.set('next_url', self.request.uri)
                self.redirect(url)
                return
            raise HTTPError(403)
        return method(self, *args, **kwargs)
    return wrapper


def permissions(roles=[]):

    def f_wrapper(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            print permissions
            print method
            return method(self, *args, **kwargs)

        return wrapper
    return f_wrapper
