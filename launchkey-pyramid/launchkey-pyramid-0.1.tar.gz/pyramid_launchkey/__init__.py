import launchkey
from functools import wraps
from pyramid.exceptions import ConfigurationError

def launchkey_setup(config, app_key, secret_key, private_key_path, test=False):
    def get_manager(request):
        return LaunchKeyManager(request, app_key, secret_key, private_key_path, test=test)
    config.set_request_property(get_manager, 'launch_key_manager')

def includeme(config):
    """ Set up Configurator methods for pyramid_launchkey """
    config.add_directive('launchkey_setup', launchkey_setup)

def get_launchkey_manager(request, id = '', use_session = True):
    """ Return the LaunchKeyManager attached to the request."""
    launch_key_manager = getattr(request, 'launch_key_manager', None)
    if launch_key_manager is None:
        raise ConfigurationError(
            'Please call Configurator.launchkey_setup during setup to use the LaunchKeyManager')

    launch_key_manager.id = id
    launch_key_manager.use_session = use_session

    return launch_key_manager

class LaunchKeyManager(object):
    '''
    Manager used to handle LaunchKey authentication.
    '''

    def __init__(self, request, app_key, secret_key, private_key_path, api_host='', manager_id = '', test=False):
        '''
        Manager initialization
        :param app_key: LaunchKey App Key
        :param secret_key: LaunchKey Secret Key
        :param private_key_path: Path to private key associated with LaunchKey Account.
        :param api_host: String. Custom LaunchKey API host. Safe to leave to default normally.
        :param use_session: Bool. Designates whether the authentication will be transaction or session based.
        '''
        self.app_key = app_key
        self.secret_key = secret_key
        self.private_key_path = private_key_path
        self.api_host = api_host
        self.test = test
        self.request = request
        self.session = request.session
        self.use_session = True
        self.id = manager_id

        if test:
            self.api = self._test_API()
        else:
            private_key = open(self.private_key_path, "r").read()
            launchkey_api = launchkey.API(self.app_key, self.secret_key, private_key, api_host=self.api_host)
            self.api = launchkey_api

    def _test_API(self):
        private_key, public_key = launchkey.generate_RSA()
        self.public_key = public_key
        return launchkey.API(1234567890, "abcdefghijklmnopqrstuvwyz1234567", private_key,
                   "testdomain.com", "v1")
    
    def _auth_in_progress(func):
        '''
        Session validation decorator
        '''
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if 'launchkey_auth_request_{0}'.format(self.id) in self.session and 'launchkey_username_{0}'.format(self.id) in self.session:
                return func(self, *args, **kwargs)
            else:
                return
        return wrapper

    @property
    @_auth_in_progress
    def username(self):
        return self.session['launchkey_username_{0}'.format(self.id)]
    
    def _clear_session(self):
        # Clean up all session variables
        self.session.pop('launchkey_auth_request_{0}'.format(self.id), None)
        self.session.pop('launchkey_auth_key_{0}'.format(self.id), None)
        self.session.pop('launchkey_username_{0}'.format(self.id), None)
    
    def authorize(self, username):
        '''
        Sends auth request to LaunchKey
        :param username: String. LaunchKey username for the request.
        :return: Bool. Authorization success based on whether the user exists.
        '''
        auth_request = self.api.authorize(username, session = self.use_session)
        
        # Check whether the user exists
        if "Error: " in auth_request:
            return False
        else:
            # The user exists, so create a user object for this session
            self.session['launchkey_username_{0}'.format(self.id)] = username
            self.session['launchkey_auth_request_{0}'.format(self.id)] = auth_request
            return True

    @_auth_in_progress
    def poll_request(self):
        '''
        Polls LaunchKey for a user response
        :return: Bool. Statement on whether the user has responded.
        '''
        auth_response = self.api.poll_request(self.session['launchkey_auth_request_{0}'.format(self.id)])
        # A status code is returned if still waiting on user input
        if 'status_code' in auth_response:
            return False
        # Otherwise a user hash and auth key will be returned
        elif 'auth' in auth_response:
            self.session['launchkey_auth_key_{0}'.format(self.id)] = auth_response['auth']
            return True

    @_auth_in_progress
    def is_authorized(self):
        '''
        Checks if the user has been authorized
        :return: Bool. Success of authorization attempt.
        '''
        if self.api.is_authorized(self.session['launchkey_auth_request_{0}'.format(self.id)], self.session['launchkey_auth_key_{0}'.format(self.id)]):
            return True
        else:
            return False

    @_auth_in_progress
    def logout(self):
        '''
        Deauthorizes the user from LaunchKey the server
        :return: Bool. Success of deauth.
        '''
        # Deauth from LaunchKey
        success = self.api.logout(self.session['launchkey_auth_request_{0}'.format(self.id)])
        self._clear_session()
        return True