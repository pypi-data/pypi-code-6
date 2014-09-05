from functools import wraps
import re

from bosun import network
from bosun import plugins
from bosun import settings

from .base import BaseListener


class WatchedFolder(object):

    ftp_port = settings.FTP_PORT
    ftp_username = settings.FTP_USERNAME
    ftp_password = settings.FTP_PASSWORD

    def __init__(self, base_path, path, func, instance):
        """
        :param base_path: safe base path
        :param path: full path
        :param func: callable handler
        :param instance: Device instance that is watching this folder
        """
        self.base_path = base_path
        self.path = path
        self.func = func
        self.instance = instance

    def __call__(self, *args, **kwargs):
        if not self.instance:
            raise TypeError('Cannot call route without a Device instance (eg, outside a request)')

        # call the func with our instance
        return self.func(self.instance, *args, **kwargs)

    def get_base_url(self):
        return self.build_url(self.base_path)

    def get_url(self):
        return self.build_url(self.path)

    def build_url(self, path):
        """ Returns returns ftp://host:port/path """
        if not self.instance:
            raise TypeError('Cannot call get_url() without a Device instance')
        return 'ftp://{host}:{port}{path}'.format(
            host=network.get_my_host(self.instance.host),
            port=settings.FTP_PORT,
            path=path,
        )


class FTPWrapper(object):

    def __init__(self, partial_path, func, watched_folders):
        if not partial_path.startswith('/'):
            partial_path = '/' + partial_path
        self.partial_path = partial_path
        self.func = func

        self.watched_folders = watched_folders

        # this will be added later by contribute_to_class()
        self.DeviceClass = None

    def __get__(self, instance, owner):
        if not owner:
            raise Exception("WatchedFolder must be attached to a class")

        return WatchedFolder(self.base_path, self.full_safe_path, self.func, instance)

    def contribute_to_class(self, DeviceClass):
        self.DeviceClass = DeviceClass

        # register a tuple of this DeviceClass + the name of the attribute as a watched folder.
        # we need to use the *name* of the attribute to be funneled through the __get__().
        # otherwise, we won't have the Device instance to use.
        self.watched_folders[self.full_safe_path] = (DeviceClass, self.func.__name__)

    @property
    def base_path(self):
        if not self.DeviceClass:
            raise ValueError("Must call contribute_to_class() beforing using this property")

        return '/' + self.DeviceClass.__module__ + '.' + self.DeviceClass.__name__

    @property
    def full_safe_path(self):
        return self.base_path + self.partial_path


class FTPListener(BaseListener):

    # our watched folders are *global* to FTP Listeners
    watched_folders = {}

    @classmethod
    def __nonzero__(cls):
        """ Boolean test is whether or not we have watched_folders """
        return bool(cls.watched_folders)

    def watched_folder(self, path):
        """ Decorates a method that is an event handler for FTP storage events on the given path.

        FTP storage handlers must accept the following arguments:
            - `filelike` - thinly wrapped StringIO instance; treat as StringIO object
        """
        def decorator(func):
            return wraps(func)(
                FTPWrapper(path, func, self.watched_folders)
            )

        return decorator

    @classmethod
    def get_handler_function(cls, search_path, host):
        """ Given a path and host, find the right Device and return the handler function """

        # plugins must be loaded for this to work
        plugins.ensure_loaded()

        print 'search path:', search_path
        for path, (DeviceClass, attr_name) in cls.watched_folders.iteritems():
            print 'trying:', path
            # if this patch matches the search path, then create an instance of this DeviceClass with the host
            if re.match('^' + path, search_path):
                device_instance = DeviceClass(host)
                # return the *bound* method (the handler) named by the watched folders
                return getattr(device_instance, attr_name)
        else:
            # TODO: real exception
            raise Exception("No handlers found for " + search_path)
