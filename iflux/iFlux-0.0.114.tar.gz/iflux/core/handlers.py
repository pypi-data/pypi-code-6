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

from __future__ import absolute_import, division, print_function, with_statement

from iflux.core import session as isession
from iflux.core import template as itemplate
import iflux.core.data

from tornado.escape import json_encode
import tornado.web
import tornado


class RequestHandler(tornado.web.RequestHandler, iflux.core.data.DataConnectedHolderMixin):
    
    """ The Application Module that packs this request. This will be used
    to resolve the template path relative to the module."""
    module = None

    def initialize(self, application_module=None):
        if application_module is not None:
            self.module = application_module

    @isession.read
    def prepare(self):
        pass        

    @isession.write
    def on_finish(self):
        pass

    def render_string(self, template_name, **kwargs):
        ignore_module = False
        application_module = None
        for key in ('ignore_module', 'module',):
            if key in kwargs:
                if key is 'ignore_module':
                    ignore_module = kwargs[key]
                if key is 'module':
                   pass 
        kwargs['user_agent'] = self.user_agent if hasattr(self, 'user_agent') else None
        kwargs['credential'] = self.credential if hasattr(self, 'credential') else None
        return super(RequestHandler, self).render_string(template_name, **kwargs)

    def write(self, chunk):
        self.application.session
        if type(chunk) == JSONResponse:
            self.content_type = 'application/json'
            chunk = chunk.get_response()
        super(RequestHandler, self).write(chunk)

    def write_error(self, status_code, **kwargs):
        error_stack = {'code': status_code}

        exc_info = None
        for key in kwargs:
            if key == 'exc_info':
                exc_info = kwargs[key]
        error = exc_info[1]

        if type(error) == JSONError:
            error_stack.update(error.data)
            response = JSONResponse(data=None, error=error_stack)
            self.write(response)
        else:
            raise error

    def get_iflux_template_path(self):
        """Override to customize iflux template path for each handler.

        By default, we use the ``iflux_template_path`` application setting.
        Return None to load templates relative to the calling file.
        """
        return self.application.settings.get('iflux_template_path')

    def get_template_path(self):
        """Override to customize template path for each handler.

        By default, we use the ``template_path`` application setting.
        Return None to load templates relative to the calling file.
        """
        if self.module is None:
            # This is the default behaviour provided by Tornado.
            # No modules on the request no fancy template path.
            return super(RequestHandler, self).get_template_path()
        else:
            return self.module.get_template_path()

    def create_template_loader(self, template_path):
        """Returns a new template loader for the given path.

        May be overridden by subclasses.  By default returns a
        directory-based loader on the given path, using the
        ``autoescape`` application setting.  If a ``template_loader``
        application setting is supplied, uses that instead.
        """
        settings = self.application.settings
        kwargs = {}
        if "autoescape" in settings:
            # autoescape=None means "no escaping", so we have to be sure
            # to only pass this kwarg if the user asked for it.
            kwargs["autoescape"] = settings["autoescape"]
        return itemplate.ModuleLoader(template_path, module=self.module, **kwargs)

    def get_xsrf_token(self):
        return self.xsrf_token

    def get_data_connected(self):
        return self.application


class JSONResponse(object):

    def __init__(self, data={}, error=None):
        self.data = data
        self.error = error

    def get_response(self):
        return {'data': self.data, 'error': self.error}


class JSONError(tornado.web.HTTPError):

    data = {}

    def __init__(self, status_code, log_message=None, *args, **kwargs):
        self.data.update(log_message)
        if not isinstance(log_message, basestring):
            json_log_message = self.data
            json_log_message['code'] = status_code
            json_log_message = json_encode(json_log_message)
        super(JSONError, self).__init__(status_code, json_log_message, *args, **kwargs)
