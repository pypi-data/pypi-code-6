# -*- coding: utf-8 -*-

import os
import re
import shlex

from pyramid.httpexceptions import HTTPUnauthorized

from djehuty.service import Service


class Slack(Service):

    def validate(self, request):
        token = request.params.get('token')
        if not token or token != os.environ.get('DJEHUTY_SLACK_OUTGOING_TOKEN'):
            raise HTTPUnauthorized()

    def get_service_argument(self, name, request):
        if name == 'user':
            return request.params.get('user_name')
        elif name == 'room':
            return request.params.get('channel_name')
        else:
            raise ValueError('invalid argument name "{}"'.format(name))

    def make_command_line(self, request):
        m = re.match(
            r'^{}\W*(.*)$'.format(request.params.get('trigger_word', '')),
            request.params.get('text', '')
        )
        return shlex.split(m.group(1).encode('utf8')) if m is not None else []

    def make_response(self, result):
        return {
            'text': result,
            'link_names': 1,
            'parse': 'full',
        }

slack = Slack()
