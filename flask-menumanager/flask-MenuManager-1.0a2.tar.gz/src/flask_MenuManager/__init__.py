# coding=utf-8
#
# (C) Copyright 2014 Alan Cabrera
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
"""
    flaskext.MenuManager
    ~~~~~~~~~~~~~~~~~~~~

    :copyright: © 2014 Alan Cabrera
    :email: `Alan Cabrera (adc@toolazydogs.com)`
    :license: ASL20, see LICENSE for more details.
"""

import flask
from werkzeug import local


class MenuManager(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.extensions['MenuManager'] = MenuContext()
        app.context_processor(lambda: {'menu_context': menu_context})


class SortedDict(dict):
    def keys(self):
        return [k for o, k in sorted([(v.order, k)
                                      for k, v in self.iteritems()])]

    def values(self):
        return [self[k] for k in self.keys()]


LAMBDA_FALSE = lambda: False
LAMBDA_TRUE = lambda: True
LAMBDA_DICT = lambda: dict()


class MenuContext(SortedDict):
    def __init__(self):
        super(MenuContext, self).__init__()
        self.endpoints = {}

    def register_menu_item(self, path, endpoint, text, order,
                           active_fn, hidden_fn, generated_fn, endpoint_fn):
        menu_item = MenuItem(endpoint, text, order,
                             active_fn, hidden_fn, generated_fn, endpoint_fn)
        self.endpoints[endpoint] = menu_item

        key = path.split('#')[-1:][0]
        parent = self.lookup_parent(path)
        if key in parent:
            menu_item.update(parent[key])
        parent[key] = menu_item

    @property
    def current_menu_item(self):
        return self.endpoints[flask.request.endpoint]

    def lookup_parent(self, path):
        parent = self
        for p in path.split('#')[1:-1]:
            if p not in parent:
                parent[p] = MenuItem(None, p)
            parent = parent[p]
        return parent


class MenuEntry(object):
    def __init__(self, path, name,
                 order=0, values=None,
                 active_fn=LAMBDA_TRUE, hidden_fn=LAMBDA_FALSE):
        self.path = path
        self.name = name
        self.order = order
        self.endpoint_fn = lambda: values if values is not None else {}
        self.active_fn = active_fn
        self.hidden_fn = hidden_fn

    def as_menu_item(self, endpoint):
        return MenuItem(endpoint, self.name,
                        order=self.order,
                        active_fn=self.active_fn,
                        hidden_fn=self.hidden_fn,
                        endpoint_fn=self.endpoint_fn)


class MenuItem(SortedDict):
    def __init__(self, endpoint, text,
                 order=0,
                 active_fn=LAMBDA_TRUE,
                 hidden_fn=LAMBDA_FALSE,
                 generated_fn=None,
                 endpoint_fn=None):
        super(MenuItem, self).__init__()
        self.endpoint = endpoint
        self.text = text
        self.order = order
        self.active_fn = active_fn
        self.hidden_fn = hidden_fn
        self.generated_fn = generated_fn
        self.endpoint_fn = endpoint_fn

    def __repr__(self):
        return 'MenuItem(%r, %r)' % (self.endpoint, self.text)

    @property
    def selected(self):
        return flask.request.endpoint == self.endpoint

    @property
    def url(self):
        if self.endpoint_fn:
            return flask.url_for(self.endpoint, **self.endpoint_fn())
        else:
            return flask.url_for(self.endpoint)

    @property
    def branch_selected(self):
        if self.selected:
            return True
        for menu_item in self.values():
            if menu_item.branch_selected:
                return True
        return False

    @property
    def active(self):
        return self.active_fn()

    @property
    def hidden(self):
        return self.hidden_fn()

    def iteritems(self):
        for k, v in super(MenuItem, self).items():
            yield k, v

        if self.generated_fn:
            if not hasattr(flask.request, 'zzzz'):
                flask.request.zzzz = {}
            if self.generated_fn not in flask.request.zzzz:
                flask.request.zzzz[self.generated_fn] = self.generated_fn()
            for me in flask.request.zzzz[self.generated_fn]:
                yield me.path[1:], me.as_menu_item(self.endpoint)

    def __getitem__(self, path):
        for k, v in self.iteritems():
            if path == k:
                return v
        raise KeyError


def register_menu(app, path, text,
                  order=0,
                  active_fn=LAMBDA_TRUE,
                  hidden_fn=LAMBDA_FALSE,
                  generated_fn=None,
                  endpoint=None,
                  endpoint_fn=LAMBDA_DICT):

    def decorator(f):
        endpoint_name = endpoint or f.__name__
        if isinstance(app, flask.Blueprint):
            before_first_request = app.before_app_first_request
            constructed_endpoint = app.name + '.' + endpoint_name
        else:
            before_first_request = app.before_first_request
            constructed_endpoint = endpoint_name

        @before_first_request
        def register_menu_item():
            menu_context.register_menu_item(path,
                                            constructed_endpoint,
                                            text, order,
                                            active_fn,
                                            hidden_fn,
                                            generated_fn,
                                            endpoint_fn)

        return f

    return decorator


def current_context():
    return flask.current_app.extensions['MenuManager']


# context locals
menu_context = local.LocalProxy(current_context)
