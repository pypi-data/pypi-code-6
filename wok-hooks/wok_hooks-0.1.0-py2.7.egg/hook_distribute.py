import logging

import os
from ftplib import FTP as FTPClient
from paramiko import SFTPClient, Transport as SFTPTransport

ALLOWED_BACKEND_TYPES = ['ftp', 'sftp']
DEFAULT_BACKEND_TYPE = 'ftp'

from wok_hooks.misc import Configuration as _Configuration


class Configuration(_Configuration):
    def __init__(self, path, **kwargs):
        _Configuration.__init__(self, path, **kwargs)

        if not 'type' in self or not self['type'] in ALLOWED_BACKEND_TYPES:
            self['type'] = DEFAULT_BACKEND_TYPE
            self.save()


class Observable:
    def __init__(self, observer=None):
        self._observer = []
        if observer:
            for item in observer:
                self.register_observer(item)

    def register_observer(self, observer):
        self._observer.append(observer)


class Stateful(Observable):
    def __init__(self, observer=None):
        if not hasattr(self, '_state'):
            self._state = None

        Observable.__init__(self, observer)

        if self._state is None:
            raise NotImplementedError()

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        if value != self._state:
            self._state = value
            logging.info('%s is now %s' % (self, value))
            self._raise_state_update()

    def _raise_state_update(self):
        for observer in self._observer:
            observer.on_state_update(self)


class FileBackend(Stateful):
    STATE_DISCONNECTED = 'disconnected'
    STATE_CONNECTED = 'connected'

    class ConnectionException(Exception):
        pass

    def __init__(self, config, observer=None):
        self.config = config
        self._state = self.STATE_DISCONNECTED
        Stateful.__init__(self, observer)

    def file_create_folder(self, path):
        raise NotImplementedError()

    def put_file(self, path, file_handle):
        raise NotImplementedError()

    def get_metadata(self, path):
        raise NotImplementedError()

    def get_file_and_metadata(self, path):
        raise NotImplementedError()

    def get_root_path(self):
        raise NotImplementedError()

    def connect(self):
        raise NotImplementedError()

    def disconnect(self):
        raise NotImplementedError()


class FTP(FileBackend):
    def __init__(self, config):
        FileBackend.__init__(self, config)
        self._init_config()
        self.session = None
        self._init_session()

    DEFAULT_CONFIG = {
        'ftp_host': 'localhost',
        'ftp_user': 'anonymous',
        'ftp_password': '',
        'ftp_output_path': ''}

    def _init_config(self):
        some_changes = False
        if 'type' in self.config:
            for option, value in FTP.DEFAULT_CONFIG.items():
                if not option in self.config:
                    self.config[option] = value
                    some_changes = True
                    logging.info('set default ftp config.')
        else:
            self.config['type'] = 'ftp'
            self.config.update(FTP.DEFAULT_CONFIG)
            some_changes = True
            logging.info('set default ftp config.')
        if some_changes:
            self.config.save()

    def _init_session(self):
        self.connect()

    def connect(self):
        self._authenticate()
        self.state = self.STATE_CONNECTED

    def _authenticate(self):
        self.session = FTPClient(self.config['ftp_host'],
                                 self.config['ftp_user'],
                                 self.config['ftp_password'])
        logging.info('FTP Authorization succeed')

    def disconnect(self):
        if self.session:
            self.session.quit()

    def file_create_folder(self, path):
        if self.state == self.STATE_CONNECTED:
            self.session.cwd('/')
            dirlist = path.split('/')
            while '' in dirlist:
                dirlist.remove('')
            previous = self.session.pwd()
            for dirname in dirlist:
                dir_contents = self.session.nlst(previous)
                if not dirname in dir_contents:
                    self.session.mkd(dirname)
                self.session.cwd(dirname)
                previous += dirname + '/'
        elif self.state == self.STATE_DISCONNECTED:
            raise self.ConnectionException('FTP is %s' % self.state)
        else:
            raise NotImplementedError()

    def put_file(self, path, file_handle):
        if self.state == self.STATE_CONNECTED:
            dirpath = '/'.join(path.split('/')[:-1])
            self.file_create_folder(dirpath)
            self.session.storbinary('STOR ' + path.split('/')[-1], file_handle)
        elif self.state == self.STATE_DISCONNECTED:
            raise self.ConnectionException('FTP is %s' % self.state)
        else:
            raise NotImplementedError()

    def get_root_path(self):
        raise NotImplementedError()


class SFTP(FileBackend):
    def __init__(self, config):
        FileBackend.__init__(self, config)
        self._init_config()
        self.session = None
        self._init_session()

    DEFAULT_CONFIG = {
        'sftp_host': 'localhost',
        'sftp_port': 22,
        'sftp_user': 'anonymous',
        'sftp_password': '',
        'output_path': ''}

    def _init_config(self):
        some_changes = False
        if 'type' in self.config:
            for option, value in SFTP.DEFAULT_CONFIG.items():
                if not option in self.config:
                    self.config[option] = value
                    some_changes = True
                    logging.info('set default sftp config.')
        else:
            self.config['type'] = 'sftp'
            self.config.update(SFTP.DEFAULT_CONFIG)
            some_changes = True
            logging.info('set default sftp config.')
        if some_changes:
            self.config.save()

        # cast config types
        self.config['sftp_port'] = int(self.config['sftp_port'])

    def _init_session(self):
        self.connect()

    def connect(self):
        self._authenticate()
        self.state = self.STATE_CONNECTED

    def _authenticate(self):
        self._transport = SFTPTransport((self.config['sftp_host'],
                                         self.config['sftp_port']))
        self._transport.connect(username=self.config['sftp_user'],
                                password=self.config['sftp_password'])
        self.session = SFTPClient.from_transport(self._transport)
        logging.info('SFTP Authorization succeed')

    def disconnect(self):
        self.session.close()
        self._transport.close()

    def file_create_folder(self, path):
        if self.state == self.STATE_CONNECTED:
            dirlist = path.split('/')
            current_dirlist = ['']
            missing_dirlist = []
            current_dirlist.extend(dirlist[:])
            while len(current_dirlist) > 0:
                current_path = '/'.join(current_dirlist)
                try:
                    self.session.chdir(current_path)
                    break
                except:
                    missing_dirlist.append(current_dirlist.pop())
            missing_dirlist.reverse()
            for dirname in missing_dirlist:
                dir_contents = self.session.listdir()
                if not dirname in dir_contents:
                    self.session.mkdir(dirname)
                    logging.info('Create remote directory %s' % self.session.getcwd() + '/' + dirname)
                self.session.chdir(dirname)
        elif self.state == self.STATE_DISCONNECTED:
            raise self.ConnectionException('SFTP is %s' % self.state)
        else:
            raise NotImplementedError()

    def put_file(self, path, file_handle):
        if self.state == self.STATE_CONNECTED:
            dirpath = '/'.join(path.split('/')[:-1])
            self.file_create_folder(dirpath)
            try:
                self.session.putfo(fl=file_handle, remotepath='/' + path)
                logging.info('Create remote file %s' % '/' + path)
            except Exception as ex:
                logging.error(ex)
        elif self.state == self.STATE_DISCONNECTED:
            raise self.ConnectionException('SFTP is %s' % self.state)
        else:
            raise NotImplementedError()


def distribute_output(options, output_path=None):
    if not output_path:
        from wok.engine import Engine  # @UnresolvedImport
        import yaml

        options = Engine.default_options.copy()

        if os.path.isfile('config'):
            with open('config') as f:
                yaml_config = yaml.load(f)

            if yaml_config:
                options.update(yaml_config)

        output_path = options['output_dir']

    remote_server = None
    try:
        config = Configuration('distribute.config')
        if config['type'] == 'ftp':
            remote_server = FTP(config)
        if config['type'] == 'sftp':
            remote_server = SFTP(config)
        for root, dirnames, filenames in os.walk(output_path, topdown=True):
            for filename in filenames:
                path = os.path.sep.join([root, filename])
                file_handle = open(path, 'rb')
                try:
                    remote_server.put_file(path.replace(output_path,
                                                        remote_server.config['output_path']),
                                           file_handle)
                except Exception as ex:
                    file_handle.close()
                    logging.error(ex)
                    raise ex
    except Exception as ex:
        logging.error(ex)
        raise
    finally:
        remote_server.disconnect()

