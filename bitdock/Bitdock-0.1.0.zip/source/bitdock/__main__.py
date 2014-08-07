# :coding: utf-8
# :copyright: Copyright (c) 2014 ftrack

import argparse
import logging
import sys
import json

import cherrypy
import requests


class Bitdock(object):
    '''Bitdock main handler.'''

    def __init__(self, flowdock_api_key, user_mapping=None):
        '''Initialise handler with *flowdock_api_key*.

        In addition, optionally specify a *user_mapping* to use when mapping
        users. It should be a dictionary of Bitbucket user names against
        Flowdock user dictionaries. The Flowdock user dictionary should contain
        keys for username, display_name and email.


        '''
        super(Bitdock, self).__init__()
        self.flowdock_api_key = flowdock_api_key
        self.user_mapping = user_mapping or {}
        self._flowdock_api_url = (
            'https://api.flowdock.com/v1/messages/team_inbox'
        )

    @property
    def flowdock_api_url(self):
        '''Return flowdock api url.'''
        return '{0}/{1}'.format(self._flowdock_api_url, self.flowdock_api_key)

    @cherrypy.tools.json_in()
    @cherrypy.expose()
    def bitbucket_pull_request(self):
        '''Handle bitbucket pull request notification.'''
        data = cherrypy.request.json

        if 'pullrequest_created' in data:
            action = 'created'
            data = data['pullrequest_created']

        elif 'pullrequest_merged' in data:
            action = 'merged'
            data = data['pullrequest_merged']

        elif 'pullrequest_declined' in data:
            action = 'declined'
            data = data['pullrequest_declined']

        else:
            raise ValueError('Unrecognised pull request action.')

        # Convert author to flowdock user if possible.
        author = self.user_mapping.get(data['author']['username'])
        if author is None:
            author = {
                'username': data['author']['username'],
                'display_name': data['author']['display_name'],
                'email': 'no-reply@bitbucket.org'
            }

        # Add tags, including a user tag for each reviewer that can be mapped to
        # a flowdock user.
        tags = ['pull-request']

        reviewers = []
        for reviewer in data.get('reviewers', []):
            flowdock_user = self.user_mapping.get(reviewer['username'])
            if flowdock_user:
                tags.append('@{0}'.format(flowdock_user['username']))
                reviewers.append(flowdock_user)
            else:
                reviewers.append(reviewer)

        # Construct main message content.
        content = [
            ('respository', data['source']['repository']['name']),
            ('branches', '{0} > {1}'.format(
                data['source']['branch']['name'],
                data['destination']['branch']['name']
            )),
            ('author', author['display_name'])
        ]

        if reviewers:
            content.append((
                'reviewers',
                ', '.join([reviewer['display_name'] for reviewer in reviewers])
            ))

        if data['description']:
            content.append(('description', data['description']))

        # Declines sometimes have a reason.
        reason = data.get('reason')
        if reason:
            content.insert(0, ('reason', reason))

        content = '<br/>'.join([
            '<b>{0}: </b>{1}'.format(key.capitalize(), value)
            for key, value in content
        ])

        # Construct payload for Flowdock.
        payload = {
            'source': 'Bitbucket',
            'subject': 'Pull Request {0}: {1}'.format(
                action.capitalize(), data['title']
            ),
            'from_name': author['display_name'],
            'from_address': author['email'],
            'project': data['source']['repository']['name'],
            'tags': tags,
            'content': content
        }

        # For some odd reason, only created pull requests include a link to
        # themselves.
        link = data.get('links', {}).get('html', {}).get('href')
        if link:
            payload['link'] = link.replace('//api.', '//')

        # Send request.
        response = requests.post(
            self.flowdock_api_url,
            headers={'content-type': 'application/json'},
            data=json.dumps(payload)
        )
        response.raise_for_status()

    def _get_flowdock_user(self, bitbucket_user):
        '''Return flowdock user for *bitbucket_user*.'''
        user = self.user_mapping.get(bitbucket_user['username'])
        if user is None:
            user = {
                'username': bitbucket_user['username'],
                'display_name': bitbucket_user['display_name'],
                'email': 'no-reply@bitbucket.org'
            }
        return user


def main(arguments=None):
    '''Bitdock: Connect Bitbucket and Flowdock.'''
    if arguments is None:
        arguments = []

    parser = argparse.ArgumentParser('bitdock')
    parser.add_argument(
        'flowdock_api_key',
        help='The API key to use for communicating with Flowdock.'
    )

    parser.add_argument(
        '--host', help='Host interface to run on.', default='0.0.0.0'
    )

    parser.add_argument(
        '--port', help='Host port to run on.', type=int, default=9000
    )

    parser.add_argument(
        '--user-mapping',
        help='Optional path to a user mapping json file. The contents should '
             'in the form {"bitbucket_username": '
             '{username: "flowdock_username", '
             '"display_name": "flowdock_display_name", '
             '"email": "email_address"}}'
    )

    # Allow setting of logging level from arguments.
    loggingLevels = {}
    for level in (
        logging.NOTSET, logging.DEBUG, logging.INFO, logging.WARNING,
        logging.ERROR, logging.CRITICAL
    ):
        loggingLevels[logging.getLevelName(level).lower()] = level

    parser.add_argument(
        '-v', '--verbosity',
        help='Set the logging output verbosity.',
        choices=loggingLevels.keys(),
        default='info'
    )

    namespace = parser.parse_args(arguments)

    logging.basicConfig(level=loggingLevels[namespace.verbosity])
    log = logging.getLogger('bitdock.main')

    # Read user map.
    user_mapping = None
    if namespace.user_mapping is not None:
        with open(namespace.user_mapping, 'r') as file_descriptor:
            user_mapping = json.load(file_descriptor)

    # Construct and start application.
    application = Bitdock(
        flowdock_api_key=namespace.flowdock_api_key,
        user_mapping=user_mapping
    )

    cherrypy.config.update({
        'server.socket_host': namespace.host,
        'server.socket_port': namespace.port
    })
    cherrypy.quickstart(application)


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
