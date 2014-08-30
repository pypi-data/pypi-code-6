import datetime, os
import re

HISTORY = os.path.join(os.path.expanduser('~'), 'history', 'shell')
DATESTAMP = re.compile(r'^#[0-9]{10}$')

def historian(directory = HISTORY, skip = []):
    '''
    directory: Directory containing the shell history
    already_read: Names of history files to skip (because they have
        already been processed)
    '''
    sessions = sorted(set(os.listdir(directory)).difference(skip))
    for session in sessions:
        result = {
            'session': session,
            'session_date': session_date(session),
        }
        with open(os.path.join(directory, session), 'r') as fp:
            result['commands'] = list(read_session(fp))
        yield result

def session_date(session:str):
    '''
    >>> session_date('2014-08-28 04:00:44.588995803+00:00')
    datetime.datetime(2014, 8, 28, 4, 0, 44)
    '''
    return datetime.datetime.strptime(session.split('.')[0], '%Y-%m-%d %H:%M:%S')

def read_session(fp):
    'This keeps comments.'
    for line in fp:
        line = line.rstrip()
        if re.match(DATESTAMP, line):
            try:
                yield command_date, command
            except NameError:
                pass
            command_date = datetime.datetime.fromtimestamp(int(line[1:]))
            command = ''
        else:
            if command != '':
                command += '\n'
            command += line
