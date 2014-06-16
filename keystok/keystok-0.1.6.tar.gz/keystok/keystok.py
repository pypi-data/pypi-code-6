from __future__ import print_function
import sys
import os
import argparse
import base64
import json
import time
# These imports require the pycrypto, pbkdf2, requests modules to be installed
import requests
from Crypto.Cipher import AES
from pbkdf2 import PBKDF2
try:
    from urllib.parse import urlencode
except:
    from urllib import urlencode

# Shortcut for creating a KeystokClient with the specified options.
# The options parameter can be an access token or a dictionary with these keys:
# 'access_token': The access token to use (required)
# 'api_host': API server to use
# 'auth_host': Authentication server to use
# 'cache_dir': Cache directory to use
# 'verbose': Verbose mode if set to True
# 'force': Force action (overwrite existing files)

def connect(options):
    return KeystokClient(options)

def printerr(*args):
    sys.stderr.write(' '.join(args) + '\n')

def safe_mkdir(path, mode=0o700):
    try:
        os.makedirs(path, mode)
    except OSError:
        pass

class KeystokClient:
    def __init__(self, options=None):
        self.options = options or {}
        if isinstance(self.options, str):
            self.options = {
                'access_token': self.options
            }
        self.token = self.decode_access_token(self.options['access_token'])
        if not self.options.get('api_host', None):
            self.options['api_host'] = 'https://api.keystok.com'
        if not self.options['api_host'].startswith('http'):
            self.options['api_host'] = 'https://' + self.options['api_host']
        if not self.options.get('auth_host', None):
            self.options['auth_host'] = 'https://keystok.com'
        if not self.options['auth_host'].startswith('http'):
            self.options['auth_host'] = 'https://' + self.options['auth_host']
        self.options['auth_host'] += '/oauth/token'
        if not self.options.get('dir', None):
            self.options['dir'] = os.path.join(os.path.expanduser('~'), '.keystok')
        if not self.options.get('cache_dir', None):
            self.options['cache_dir'] = os.path.join(self.options['dir'], 'cache')
        if not self.options.get('verbose', None):
            self.options['verbose'] = False
        if not self.options.get('force', None):
            self.options['force'] = False
        # Ensure cache directory exists
        safe_mkdir(self.options['cache_dir'], 0o700)
        # Create full cache path with application ID in it
        self.cache_path = os.path.join(self.options['cache_dir'], str(self.token['id']))
        safe_mkdir(self.cache_path, 0o700)

    def get_key(self, key_id):
        url = '%s/apps/%s/deploy/%s?access_token=%s' % (self.options['api_host'], self.token['id'], key_id, self.refresh_access_token(self.token))
        r = requests.get(url)
        if r.status_code != 200:
            raise Exception('Error retrieving key from server: ' + str(r.status_code))
        response = r.json()
        return self.decrypt_data(self.token, response[key_id]['key'])

    def list_keys(self):
        url = '%s/apps/%s/keys?access_token=%s' % (self.options['api_host'], self.token['id'], self.refresh_access_token(self.token))
        r = requests.get(url)
        if r.status_code != 200:
            raise Exception('Error retrieving keys from server: ' + str(r.status_code))
        response = r.json()
        return response

    def cmd_ls(self):
        response = self.list_keys()
        if self.options['verbose']:
            # Show headers and descriptions
            print('KEY ID                         DESCRIPTION')
            print('------------------------------ -----------------------------------------------')
            for key in response:
                print('%-30s %s' % (key['id'], key.get('description', '')))
        else:
            # Show key ids only
            for key in response:
                print(key['id'])

    def cmd_get(self, key_id):
        sys.stdout.write(self.get_key(key_id))

    def cmd_sshautoconfig(self):
        # Autoconfigure ssh with private/public keypair from Keystok and some default options.
        # This is mainly intended for unattended deployments like Dockerfiles.
        ssh_path = os.path.join(os.path.expanduser('~'), '.ssh')
        ssh_config_path = os.path.join(ssh_path, 'config')
        ssh_private_key_path = os.path.join(ssh_path, 'id_rsa')
        ssh_public_key_path = os.path.join(ssh_path, 'id_rsa.pub')
        ssh_private_key = self.get_key('ssh_private_key')
        ssh_public_key = self.get_key('ssh_public_key')
        if not ssh_private_key or not ssh_public_key:
            # Key(s) not configured, give up
            sys.stderr.write('keystok: sshautoconfig: ssh key(s) not configured in application, aborting.\n')
            return 1
        if not self.options['force'] and (os.path.isfile(ssh_public_key_path) or os.path.isfile(ssh_private_key_path)):
            # Key(s) already saved, give up
            sys.stderr.write('keystok: sshautoconfig: ssh key(s) already exist, aborting.\n')
            return 1
        # Make sure the keys end up with LF for convenience
        if not ssh_private_key.endswith('\n'):
            ssh_private_key += '\n'
        if not ssh_public_key.endswith('\n'):
            ssh_public_key += '\n'
        safe_mkdir(ssh_path)
        if not os.path.isfile(ssh_config_path):
            # Create ~/.ssh/config with allowing options
            if self.options['verbose']:
                printerr('Creating', ssh_config_path, 'with non-strict defaults.')
            with open(ssh_config_path, 'w') as f:
                f.write('Host *\n    UserKnownHostsFile /dev/null\n    StrictHostKeyChecking no\n')
        # Create ~/.ssh/id_rsa(.pub)
        if self.options['verbose']:
            printerr('Creating', ssh_private_key_path)
        with open(ssh_private_key_path, 'w') as f:
            os.chmod(ssh_private_key_path, 0o600);
            f.write(ssh_private_key)
        if self.options['verbose']:
            printerr('Creating', ssh_public_key_path)
        with open(ssh_public_key_path, 'w') as f:
            f.write(ssh_public_key)

    def decode_access_token(self, token):
        return json.loads(base64.b64decode(token.replace('-', '+').replace('_', '/')).decode('utf-8'))

    def refresh_access_token(self, token):
        # First see what we already have in the token
        access_token = token.get('at')
        refresh_token = token.get('rt')
        if access_token:
            # Already have an access token
            return access_token

        # Do we have an access token cached?
        try:
            cached_token = json.load(open(os.path.join(self.cache_path, 'access_token')))
            if cached_token['expires_at'] > int(time.time()):
                return cached_token['access_token']
        except IOError:
            # Could not read it
            pass

        # Must refresh to get new access token
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
        }
        r = requests.post(self.options['auth_host'], data)
        if r.status_code != 200:
            # Failed to refresh
            raise Exception('Error refreshing OAuth access token: ' + str(r.status_code))
        response = r.json()
        if not ('expires_in' in response and 'access_token' in response):
            # Invalid response
            raise Exception('Invalid OAuth access token refresh response')
        response['expires_at'] = int(time.time()) + response['expires_in']

        with open(os.path.join(self.cache_path, 'access_token'), 'w') as f:
            json.dump(response, f)
        return response['access_token']

    def make_decryption_key(self, password, keysize, salt, iterations):
        return PBKDF2(password, salt, iterations).read(keysize//8)

    def decrypt_data(self, token, data):
        if not data.startswith(':aes256:'):
            raise Exception('Unsupported encryption scheme')
        data = json.loads(base64.b64decode(data[8:]).decode('utf-8'))
        # First we need to make the actual encryption key
        decryption_key = self.make_decryption_key(token['dk'], data['ks'], base64.b64decode(data['salt']), data['iter'])
        iv = base64.b64decode(data['iv'])
        cipher_text = base64.b64decode(data['ct'])
        aes = AES.new(decryption_key, AES.MODE_CBC, iv)
        clear_text = aes.decrypt(cipher_text)
        if clear_text:
            padding = clear_text[-1]
            if isinstance(padding, str):
                padding = ord(padding)
            clear_text = clear_text[:0-padding]
        return clear_text.decode('utf-8')

def main():
    access_token = os.environ.get('KEYSTOK_ACCESS_TOKEN', '')
    keystok_dir = os.environ.get('KEYSTOK_DIR', '')
    cache_dir = os.environ.get('KEYSTOK_CACHE_DIR', '')
    parser = argparse.ArgumentParser(description='Keystok shell access')
    parser.add_argument('-a', '--access-token', type=str, help='Specify access token (overrides $KEYSTOK_ACCESS_TOKEN)')
    parser.add_argument('-d', '--dir', type=str, help='Specify Keystok directory (overrides $KEYSTOK_DIR, defaults to ~/.keystok)')
    parser.add_argument('-c', '--cache-dir', type=str, help='Specify cache directory (overrides $KEYSTOK_CACHE_DIR, defaults to ~/.keystok/cache)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Show verbose output')
    parser.add_argument('-f', '--force', action='store_true', help='Force action (overwrite existing files)')
    parser.add_argument('command', choices=['ls', 'get', 'sshautoconfig'], help='Command to execute')
    parser.add_argument('args', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    
    # Allow overriding Keystok dir
    if args.dir:
        keystok_dir = args.dir
    if not keystok_dir:
        # We need a default
        keystok_dir = os.path.join(os.path.expanduser('~'), '.keystok')

    # Access token is required
    if args.access_token:
        access_token = args.access_token
    if not access_token:
        # See if we can get it from a file in the current directory
        try:
            access_token = open(os.path.join(os.getcwd(), '.keystok', 'access_token')).read().decode('utf-8').strip()
        except IOError:
            # Ignore not found
            pass
    if not access_token:
        # See if we can get it from a file in the global config directory
        try:
            access_token = open(os.path.join(keystok_dir, 'access_token')).read().decode('utf-8').strip()
        except IOError:
            # Ignore not found
            pass
    if not access_token:
        sys.stderr.write('Access token is not configured. Please set KEYSTOK_ACCESS_TOKEN environment variable or use the -a option.\n');
        sys.exit(1)

    # Allow overriding cache dir
    if args.cache_dir:
        cache_dir = args.cache_dir

    # Execute the command
    client = KeystokClient({
        'access_token': access_token,
        'dir': keystok_dir,
        'cache_dir': cache_dir,
        'verbose': args.verbose,
        'force': args.force,
    })
    cmd = getattr(client, 'cmd_' + args.command)
    if not cmd:
        sys.stderr.write('Invalid command \'%s\'". Try -h for help.\n' % args.command)
        sys.exit(2)
    sys.exit(cmd(*args.args) or 0)

if __name__ == '__main__':
    main()
