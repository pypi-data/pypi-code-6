# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
pycsync.auth
============

Module for authentication related functions.
'''

from os.path import join as pjoin
import flickr_api as fapi


def request_token(rootdir, input_func=raw_input):
    '''
    Request an auth token. Prompt the user to accept the client API key and
    submit a verifier code. Then record out the auth file to ``rootdir``.

    rootdir
        The root directory to sync.
    '''
    set_api_keys()
    authfile = pjoin(rootdir, '.pycsync')
    prompt = 'Please visit to get an verifier code:\n' \
             '---------------------------------\n' \
             '{0}\n' \
             '---------------------------------\n' \
             'Please input the verifier code here: '
    auth = fapi.auth.AuthHandler()
    url = auth.get_authorization_url('write')
    verifier = input_func(prompt.format(url))
    auth.set_verifier(str(verifier))
    auth.write(authfile)
    return True


def setup_auth_handler(rootdir):
    '''
    Set up the auth handler using the authfile in ``rootdir``

    rootdir
        The root directory to sync.
    '''
    set_api_keys()
    authfile = pjoin(rootdir, '.pycsync')
    fapi.set_auth_handler(authfile)
    return True


def set_api_keys():
    '''
    Set up the client api keys.
    '''
    fapi.keys.set_keys('e81b828b075041b2a22b7c1663efc492', 'b1174b27c8cdb649')
