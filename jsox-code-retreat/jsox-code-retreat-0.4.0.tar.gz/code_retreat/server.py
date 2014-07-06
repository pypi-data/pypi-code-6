import logging
import json
import socket
import sys

import requests


log = logging.getLogger('code-retreat')


class NoData(Exception):
    pass


def build_response(info, user_code):
    action = info['action'],
    generation = info['payload']['generation'],
    result = info['payload']['result'],

    user_result = getattr(user_code, action)(result)

    types = {
        'tickBoard': [{
            'generation': generation,
            'result': result,
        }, {
            'generation': generation + 1,
            'result': user_result,
        }],
        'tickCell': {
            'generation': generation,
            'x': info['payload']['x'],
            'y': info['payload']['y'],
            'from': info['payload']['from'],
            'lives': user_result,
        },
    }

    # build payload
    response = json.dumps({
        'success': True,
        'respondingTo': action,
        'payload': types[action],
    })

    return response


def get_data(sock):
    """
    Get data from the socket

    Defensively try to get data from the socket.
    """
    if sock is None:
        sock = get_socket()
        if sock is None:
            # the server really doesn't want to respond
            log.debug('Couldn\'t create socket')
            raise NoData

    data = sock.recv(4096)
    log.debug('Data 1: {}'.format(data))
    if len(data) == 0:
        # socket is dead so try to connect again
        sock = get_socket()
        if sock is None:
            log.debug('Socket was dead. Failed to recreate it.')
            raise NoData

        data = sock.recv(1024)
        log.debug('Data 2: {}'.format(data))
        if len(data) == 0:
            # socket is dead again, bail out
            log.debug('Failed to receive data two versions of the socket.')
            raise NoData

    return data


def get_socket():
    """
    Create a socket to the GoL Server

    The IP is retrieved from a JSON document hosted at jsoxford.com to avoid
    IP changing issues on networks we can't control.
    """
    url = 'http://jsoxford.com/cr.json'
    r = requests.get(url)
    if not r.ok:
        log.debug('Could not get server address data: {}'.format(r.status_code))
        return None

    endpoint = r.json()['endpoint']
    address = (endpoint['host'], endpoint['port'])

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(address)
    except socket.error:
        log.debug('Failed to create socket.')
        return None

    log.debug('Socket connected to: {}:{}'.format(*address))
    return s


def send(sock, user_code):
    """Send return value of the user's function to the server"""
    data = get_data(sock)

    # It's alive!
    info = json.loads(data.split('\n')[0])
    log.debug('Parsed: {}'.format(info))

    if info['action'] not in ('tickBoard', 'tickCell'):
        log.debug('Unknown action: "{}"'.format())
        return

    args = (
        user_code,
    )
    try:
        response = getattr(user_code, info['action'])(*args)
    except Exception as e:
        log.debug('Error in user code: {}'.format(e))
        sys.stderr.write('There was an error in your code: {}\n'.format(e))

        response = {
            'success': False,
            'respondingTo': info['action'],
            'payload': {
                'error': 'The function could not be executed.'
            }
        }

    log.debug('Sending: {}'.format(response))

    sock.sendall(response)


def send_test_data(ran, failed):
    sock = get_socket()

    response = json.dumps({
        'action': 'consumeTestsResults',
        'payload': {
            'testsRun': ran,
            'testsFailed': failed,
            'testsIgnored': 0,
        }
    })

    sock.sendall(response)
