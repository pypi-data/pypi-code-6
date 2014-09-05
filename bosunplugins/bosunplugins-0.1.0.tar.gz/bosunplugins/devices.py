from functools import wraps
import json
import inspect

from bosun import storage, network
from bosun.exceptions import CrowsnestDeviceNotFound, InvalidCredentialsKeys, DeviceIdentifyError
from bosun.transport import DefaultTransport, DeviceAPI
from crowsnest_capabilities import capabilities

from . import util
from .listeners import Listeners


class DeviceMetaclass(type):
    def __new__(cls, clsname, bases, attrs):
        """ The actual registration of several things needs to happen here so we have the attrs and the class. """

        actions = {}

        # go through the attributes looking for ones marked with special case markers
        for attr in attrs.values():
            # register capability methods marked with the action() decorator
            # actions are marked with '_action'
            action_name = getattr(attr, '_action', None)
            if action_name:
                actions[action_name] = attr

        # attach our actions, now that we're done iterating on attrs
        attrs['_unbound_actions'] = actions

        # create poller() decorator for this cls
        pass

        return super(DeviceMetaclass, cls).__new__(cls, clsname, bases, attrs)

    def __init__(cls, name, bases, attrs):

        # set up our listeners object for this class
        cls.listeners = Listeners()

        # contribute all of the routes to the class
        for attr in attrs.values():
            if hasattr(attr, 'contribute_to_class') and callable(attr.contribute_to_class):
                attr.contribute_to_class(cls)


class Device(object):

    __metaclass__ = DeviceMetaclass

    # CAPABILITY DECORATORS #

    @staticmethod
    def action(name):
        """ Decorator used for actions """
        def decorator(func):
            # check that the named capability exists and that we've defined things correctly
            assert name in capabilities, "'{}' is not defined in the capabilities".format(name)

            # check that the inputs are correct for this method
            # we prepend self
            expected_args = ['self'] + capabilities[name].inputs.keys()
            assert sorted(inspect.getargspec(func).args) == sorted(expected_args), "'{}' expects {}() to have the following arguments: {}".format(name, func.__name__, expected_args)

            # we can't do any registration yet, since the new class *doesn't exist* yet,
            # but we will wrap this function in validation
            @wraps(func)
            def wrapper(self, **kwargs):
                cleaned_input = capabilities[name].clean_input(kwargs)
                output = func(self, **cleaned_input)
                cleaned_output = capabilities[name].clean_output(output)
                return cleaned_output

            # mark the wrapper with the capability name
            wrapper._action = name

            return wrapper
        return decorator

    # @staticmethod decorator is applied at the end of the class so @emits is usable
    # without having to do @emits.__func__ (because staticmethods are not callable)
    def emits(name):
        """ Decorator used for events """
        def decorator(func):
            # check that the named event exists and that we've defined things correctly
            assert name in capabilities, "'{}' is not defined in the capabilities".format(name)

            @wraps(func)
            def wrapper(self, _prevent_emit=False, *args, **kwargs):
                """ May use _prevent_emit to stop the call to Crowsnest; useful for testing """
                output = func(self, *args, **kwargs)
                cleaned_output = capabilities[name].clean_output(output)

                # as long as we are not supposed to prevent the emit, do it
                if not _prevent_emit:
                    # send cleaned_output to Crowsnest
                    self.transport.send_event(name, cleaned_output)

                return cleaned_output

            return wrapper
        return decorator

    # CLASS ATTRIBUTES #

    # default timeout for all devices is 200ms
    detection_timeout = 0.2

    # INSTANCE METHODS & ATTRIBUTES #

    def __init__(self, host, port=None, credentials=None):
        self.host = host
        # if we were not given a port, try to guess using is_my_type()
        if not port:
            for port in self.ports_to_scan:
                # on success, break
                if self.is_my_type(host, port):
                    break
            else:
                # if no ports worked, then something is wrong
                raise DeviceIdentifyError('Unknown device at ' + host)

        # whether we were given the port or had to guess in the loop, store it
        self.port = port

        # storage for magic properties
        self._meta = None
        self._hardware_address = None

        # bind up our actions
        assert not hasattr(self, 'actions'), "{}.actions is a reserved attribute".format(self.__class__.__name__)
        # func.__get__(self, cls) binds to the instance
        # Doing this binding here is probably more proficient than searching for all
        # of the marked attributes (as we do in the metaclass) every time a class
        # is instantiated. At least this doesn't involve a search.
        self.actions = {name: unbound_function.__get__(self, self.__class__) for name, unbound_function in self._unbound_actions.iteritems()}

        # if we were given credentials, use them
        if credentials:
            self.credentials = credentials

        # set up a device api instance
        self.device_api = DeviceAPI()

        # if we are successfully authenticated, set up the device
        if self.is_authenticated:
            # if we don't have a uuid, register the device with crowsnest
            if not self.uuid:
                self.register_with_crowsnest()

            # set up a transport
            self.transport = DefaultTransport(self.uuid)

            # always make sure the hardware address is up to date (not that it should change)
            storage.set_device_attr(self.uuid, 'hardware_address', self.hardware_address)

            # if credentials were provided, they worked and we should save them
            if credentials:
                # credentials are stored as json, need to encode them
                storage.set_hardware_attr(self.hardware_address, 'credentials', json.dumps(self.credentials))

    def register_with_crowsnest(self):
        self._meta = self.device_api.create_device()

        # set the uuid on the device to the uuid from crowsnest
        self.uuid = self.meta.uuid

        # store the secret key, if we have it
        if self.meta.secret_key:
            storage.set_device_attr(self.uuid, 'secret_key', self.meta.secret_key)

    @property
    def uuid(self):
        if not hasattr(self, '_uuid'):
            # we'll start with a value of None in case our attemp doesn't work
            self._uuid = None

            # only try to get the uuid if we're authenticated
            if self.is_authenticated:
                value = self.get_uuid()
                # only save if the value is a uuid
                if util.is_uuid(value):
                    self._uuid = value

        return self._uuid

    @uuid.setter
    def uuid(self, value):
        self.set_uuid(value)
        # should we trust set_value() or re-query with get_uuid()?
        self._uuid = value

    @property
    def hardware_address(self):
        """ Self-populating property for the hardware (mac) address of this device """
        if not self._hardware_address:
            self._hardware_address = network.arp.get_hardware_address(self.host)
        return self._hardware_address

    @property
    def credentials(self):
        """ Magic, self-populating-if-we-can property for device credentials """

        if not hasattr(self, '_credentials'):
            guessed_credentials = storage.get_hardware_attr(self.hardware_address, 'credentials')

            # if we get credentials, keep them
            if guessed_credentials:
                # credentials are stored as json, need to decode them
                self._credentials = json.loads(guessed_credentials)
            # otherwise, we don't have any
            else:
                self._credentials = None

        return self._credentials

    @credentials.setter
    def credentials(self, value):
        """ You're allowed to set your own credentials if you know them. """
        # validate that the keys are valid
        if not sorted(value.keys()) == sorted(self.credentials_field_names):
            raise InvalidCredentialsKeys()
        self._credentials = value

    @property
    def is_authenticated(self):
        """ Test auth for our credentials """

        # if not already computed, find out
        if not hasattr(self, '_authenticated'):
            # if there are no required credentials for this device, then we're all set
            if not self.credentials_field_names:
                self._authenticated = True

            # otherwise, we require credentials and a successful authentication attempt
            else:
                self._authenticated = bool(self.credentials and self.authenticate(**self.credentials))

        return self._authenticated

    @property
    def meta(self):
        if not self._meta:
            if not self.is_authenticated:
                # TODO: real exception
                raise Exception("Device not authenticated")
            try:
                # look up the device for the meta
                self._meta = self.device_api.get_device(self.uuid)
            except CrowsnestDeviceNotFound:
                # if a device is not found on Crowsnest, then we'll register it
                self.register_with_crowsnest()

        return self._meta

    def is_healthy(self):
        """ Health check for heartbeats, etc """
        return self.is_authenticated and self.is_connected_to_bosun()

    @emits('event.generic.heartbeat.beat')
    def heartbeat(self):
        """ Generates a heartbeat event. """
        return {}

    def as_dict(self):
        base = {
            'host': self.host,
            'verbose_name': self.verbose_name,
        }
        if self.is_authenticated:
            # Make sure the meta is set up *before* doing this.
            # In the case where the camera has a bad UUID, this will fix the UUID
            # before building this dict.
            self.meta

            result = {
                'is_authenticated': True,
                'uuid': self.uuid,
                'is_registered': self.meta.is_registered,
                'name': self.meta.name,
                'visit_url': self.meta.visit_url,
                'registration_url': self.meta.registration_url,
                'is_connected_to_bosun': self.is_connected_to_bosun(),
            }
        else:
            result = {
                'is_authenticated': False,
                'credentials_field_names': self.credentials_field_names,
            }

        # update this with the base
        result.update(base)
        return result

    # CLEANUP #

    # make emits() a staticmethod here (see notes at emits() definition)
    emits = staticmethod(emits)

    # SUBCLASS INSTANCE METHODS & ATTRIBUTES #

    # name
    verbose_name = None

    # network discovery
    ports_to_scan = []

    @classmethod
    def is_my_type(cls, host, port):
        """ Returns True or False for whether this class can interact with the service at the host and port """
        raise NotImplementedError('{} must implement `is_my_type()`'.format(cls))

    # auth
    credentials_field_names = None

    def authenticate(self, **credentials):
        """ Attemps to authenticate with device using supplied credentials.

        Keyword arguments guaranteed to be named to match credentials_field_names.
        Returns True or False for whether or not authentication attempt was successful.
        """
        raise NotImplementedError('{} must implement `authenticate()`'.format(self.__class__))

    # uuid
    def get_uuid(self):
        """ Returns a uuid if set, or None if not """
        raise NotImplementedError('{} must implement `get_uuid()`'.format(self.__class__))

    def set_uuid(self, value):
        """ Sets the uuid on the device to the given value """
        raise NotImplementedError('{} must implement `set_uuid()`'.format(self.__class__))

    # connect to bosun
    def connect_to_bosun(self):
        """ Configure the device to communicate to Bosun. """
        raise NotImplementedError('{} must implement `connect_to_bosun()`'.format(self.__class__))

    def is_connected_to_bosun(self):
        """ Detect if this device is configured to communicate with Bosun. """
        raise NotImplementedError('{} must implement `is_connected_to_bosun()`'.format(self.__class__))

    # UTILITY #

    @classmethod
    def test_subclass(cls):
        """ Runs basic assertions for subclass methods and attributes """

        # when comparing methods, need to use 'not ==' instead of 'is' because methods
        # are created every time their accessed

        # verbose_name
        assert cls.verbose_name, '{}.verbose_name should be set'.format(cls)

        # get_uuid()
        assert not cls.get_uuid == Device.get_uuid, '{} must implement `get_uuid()`'.format(cls)
        assert len(inspect.getargspec(cls.get_uuid).args) == 1, '{}.get_uuid() takes 1 argument, `self`'.format(cls)

        # set_uuid()
        assert not cls.set_uuid == Device.set_uuid, '{} must implement `set_uuid()`'.format(cls)
        assert len(inspect.getargspec(cls.set_uuid).args) == 2, '{}.set_uuid() takes 2 arguments, `self` and `value`'.format(cls)

        # ports_to_scan
        assert isinstance(cls.ports_to_scan, (list, tuple)), '{}.ports_to_scan must be a list or tuple'.format(cls)
        assert cls.ports_to_scan, '{}.ports_to_scan must not be empty'.format(cls)

        # is_my_type()
        assert not cls.is_my_type == Device.is_my_type, '{} must implement `is_my_type()`'.format(cls)

        # make sure is_my_type is not an instance method
        # instance methods have `im_self` and it is None when unbound
        # class methods have `im_self` and it is the class (they are bound to the class)
        # static methods do not have `im_self`, because they are never bound
        if hasattr(cls.is_my_type, 'im_self'):
            # it's either an instance method or class method
            # `im_self` will be the cls if it's a class method
            assert cls.is_my_type.im_self is cls, '{}.is_my_type() should be a staticmethod or classmethod'.format(cls)
            # class methods should have 3 args
            assert len(inspect.getargspec(cls.is_my_type).args) == 3, '{}.is_my_type() as a @classmethod takes 2 arguments, `cls`, `host`, and `port`'.format(cls)
        else:
            # otherwise, it's a static method
            assert len(inspect.getargspec(cls.is_my_type).args) == 2, '{}.is_my_type() as a @staticmethod takes 1 argument, `host` and `port`'.format(cls)

        # credentials_field_names
        assert cls.credentials_field_names is None or isinstance(cls.credentials_field_names, (list, tuple)), '{}.credentials_field_names must be None, a list, or tuple'.format(cls)

        # authenticate(), only required when credentials_field_names is set
        if cls.credentials_field_names:
            assert not cls.authenticate == Device.authenticate, '{} must implement `authenticate()`'.format(cls)
            # assemple a tuple of the arg names; credentials_field_names may be None, which is why we supply []
            authenticate_arg_names = ['self'] + list(cls.credentials_field_names or [])
            assert inspect.getargspec(cls.authenticate).args == authenticate_arg_names, '{}.authenticate() takes exactly these arguments: {}'.format(cls, authenticate_arg_names)

        # connect_to_bosun()
        assert not cls.connect_to_bosun == Device.connect_to_bosun, '{} must implement `connect_to_bosun()`'.format(cls)
        assert len(inspect.getargspec(cls.connect_to_bosun).args) == 1, '{}.connect_to_bosun() takes 1 argument, `self`'.format(cls)

        # is_connected_to_bosun()
        assert not cls.is_connected_to_bosun == Device.is_connected_to_bosun, '{} must implement `is_connected_to_bosun()`'.format(cls)
        assert len(inspect.getargspec(cls.is_connected_to_bosun).args) == 1, '{}.is_connected_to_bosun() takes 1 argument, `self`'.format(cls)
