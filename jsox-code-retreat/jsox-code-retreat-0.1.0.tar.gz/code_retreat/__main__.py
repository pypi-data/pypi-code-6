import collections
import imp
import json
import logging
import socket
import sys


logging.basicConfig(
    format='%(asctime)-15s %(levelname)-8s %(name)-11s %(message)s',
    level=logging.DEBUG,
)
log = logging.getLogger('code-retreat-runner')


def get_user_data(path):
    Data = collections.namedtuple('Data', ['team', 'session_id'])

    with open(path, 'r') as f:
        first = f.readline()

    # check the format
    # team: name, name, name
    if not first.startswith('#'):
        sys.stderr.write('First line of your file needs to be the comment string!')
        sys.exit(1)

    first.split(':')[1]
    data = Data(
        team=['foo', 'bar'],
        session_id='',
    )

    return data


def get_user_file():
    try:
        path = sys.argv[1]
    except IndexError:
        sys.stderr.write('Specify a user file to run with.\n')
        sys.exit(1)

    return path


def get_socket():
    """Create an INET, STREAMing socket"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        sys.stderr.write('Failed to create socket.\n')
        sys.exit(1)

    s.connect(('', 3001))

    return s


def import_user_code(path):
    """Import user code from argument"""
    try:
        return imp.load_source('user_code', path)
    except IOError:
        sys.stderr.write('Could not find file "{}".\n'.format(path))
        sys.exit(1)


def main():
    # do some startup and sanity checks
    user_file = get_user_file()
    user_code = import_user_code(user_file)
    user_data = get_user_data(user_file)

    s = get_socket()

    while True:
        data = s.recv(4096)

        if data:
            log.debug('Received: {}'.format(data))
            info = json.loads(data)
            log.debug('Parsed: {}'.format(info))

            # run info through user function
            next_step = user_code.get_next_step(info['payload'])

            # build response
            response = json.dumps({
                'team': user_data.team,
                'foo': next_step,
                'session': user_data.session_id,
            })
            log.debug('Reponse: {}'.format(response))
            s.sendall(response)

    s.close()

    sys.exit(0)


def run():
    """
    Wrapper for the main function

    Wraps main with a keyboard interrupt catch so running the module directly
    and from the console_scripts can use the same functionality without having
    extra indentation in main.
    """
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == '__main__':
    run()
