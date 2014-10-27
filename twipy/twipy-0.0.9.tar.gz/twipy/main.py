# -*- coding: utf-8 -*-

from twipy.keys import Keys, KeyFiles
from twipy.command import Command
from twipy.capture import CaptureSignals
from twipy.capture import eoferror_exception


def get_keys(keys):
    oauth_client = keys.get_auth_token()
    keys.get_token(oauth_client)
    oauth_client, pin_code = keys.authorize()
    keys.get_access(oauth_client, pin_code)


def first_time_storage():
    file_storage = KeyFiles()
    if not file_storage.exists_token_file():
        file_storage.create_folder()

    keys = Keys()

    if not file_storage.exists_token_file():
        get_keys(keys)
        keys.save_keys()


def main():
    CaptureSignals().capture_signals()

    c = ''

    first_time_storage()
    command = Command()

    while c != 'q':
        try:
            c = raw_input('Command: ')
            command.dispatch(c)
        except EOFError:
            eoferror_exception()

    exit(0)


if __name__ == '__main__':
    main()
