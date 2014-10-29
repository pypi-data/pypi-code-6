# -*- coding: utf-8 -*-
# copyright 2013-2014 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.

"""cubicweb-rqlcontroller views/forms/actions/components for web ui"""

import re

from cubicweb.predicates import ExpectedValuePredicate, match_http_method, match_form_params
from cubicweb.uilib import exc_message
from cubicweb.utils import json, json_dumps
from cubicweb.web import RemoteCallFailed, DirectResponse
from cubicweb.web.controller import Controller
from cubicweb.web.views.urlrewrite import rgx_action, SchemaBasedRewriter
from cubicweb import Binary

ARGRE = re.compile('__r(?P<ref>\d+)$')
DATARE = re.compile('__f(?P<ref>.+)$')


def rewrite_args(args, output, form):
    for k, v in args.items():
        if not isinstance(v, basestring):
            continue
        match = ARGRE.match(v)
        if match:
            numref = int(match.group('ref'))
            if 0 <= numref <= len(output):
                rset = output[numref]
                if not rset:
                    raise Exception('%s references empty result set %s' %
                                    (v, rset))
                if len(rset) > 1:
                    raise Exception('%s references multi lines result set %s' %
                                    (v, rset))
                row = rset.rows[0]
                if len(row) > 1:
                    raise Exception('%s references multi column result set %s' %
                                    (v, rset))
                args[k] = row[0]
            continue
        match = DATARE.match(v)
        if match:
            args[k] = Binary(form[v][1].read())

class match_request_content_type(ExpectedValuePredicate):
    """check that the request body has the right content type"""
    def _get_value(self, cls, req, **kwargs):
        header = req.get_header('Content-Type', None)
        if header is not None:
            header = header.split(';', 1)[0].strip()
        return header

class RqlIOController(Controller):
    """posted rql queries and arguments use the following pattern:

        [('INSERT CWUser U: U login %(login)s, U upassword %(pw)s',
          {'login': 'babar', 'pw': 'cubicweb rulez & 42'}),
         ('INSERT CWGroup G: G name %(name)s',
          {'name': 'pachyderms'}),
         ('SET U in_group G WHERE G eid %(g)s, U eid %(u)s',
          {'u': '__r0', 'g': '__r1'}),
         ('INSERT File F: F data %(content)s, F data_name %(fname)s',
          {'content': '__f0', 'fname': 'toto.txt'}),
        ]

        The later query is an example of query built to upload binety data as
        a file object. It requires to have a multipart query in which there is
        a part holding a file named '__f0'. See cwclientlib for examples of such
        queries.

        Limitations: back references can only work if one entity has been
        created.

    """
    __regid__ = 'rqlio'
    __select__ = (match_http_method('POST') &
                  match_request_content_type('application/json', 'multipart/form-data', mode='any') &
                  match_form_params('version'))

    def json(self):
        try:
            if self._cw.get_header('Content-Type') == 'application/json':
                args = json.load(self._cw.content)
                self._cw.content.seek(0, 0)
            else:
                args = json.load(self._cw.form['json'][1])

        except ValueError as exc:
            self.exception('error while decoding json arguments for '
                           'rqlio: %s', exc)
            raise RemoteCallFailed(exc_message(exc, self._cw.encoding))
        if not isinstance(args, (list, tuple)):
            args = (args,)
        return args

    def publish(self, rset=None):
        self._cw.ajax_request = True
        self._cw.set_content_type('application/json')

        if self._cw.form['version'] != '1.0':
            raise RemoteCallFailed('unknown rqlio version %r', self._cw.form['version'])
        args = self.json()

        try:
            result = self.rqlio(*args)
        except (RemoteCallFailed, DirectResponse):
            raise
        except Exception as exc:
            self.exception('an exception occurred while calling rqlio(%s): %s',
                           args, exc)
            raise RemoteCallFailed(exc_message(exc, self._cw.encoding))
        if result is None:
            return ''
        return json_dumps(result)

    def rqlio(self, *rql_args):
        try:
            output = self._rqlio(rql_args)
        except Exception as exc:
            self._cw.cnx.rollback()
            raise
        else:
            self._cw.cnx.commit()
        return [o.rows for o in output]

    def _rqlio(self, rql_args):
        output = []
        for rql, args in rql_args:
            if args is None:
                args = {}
            rewrite_args(args, output, self._cw.form)
            output.append(self._cw.execute(rql, args))
        return output

class RQLIORewriter(SchemaBasedRewriter):
    rules = [
            (re.compile('/rqlio/(?P<version>.+)$'), rgx_action(controller='rqlio', formgroups=('version',)))
            ]
