# Standard library imports
import datetime
import inspect
import io
import json
import os
import platform
import random
import shutil
import subprocess
import tarfile
import tempfile
import uuid

# Third party imports
#import docopt # https://github.com/docopt/docopt
import requests # https://github.com/kennethreitz/requests

# This is for debbuging purposes only
try:
    import pydevd # http://pydev.org/
except:
    pass

# All OS dependent data should go here
all_oses_data = {'Windows' : 
                 {'download_URL' : 'http://download-lb.utorrent.com/endpoint/btsync/os/windows/track/stable',
                  'application_folder' : os.path.join(os.environ.get('APPDATA') or '','pybtsync'),
                  'btsync_file' : 'BTSync.exe',
                  'settings_file' : 'pybtsync'},
                  'Linux' :
                 {'download_URL' : 'http://download-lb.utorrent.com/endpoint/btsync/os/linux-x64/track/stable',
                  'application_folder' : os.path.join(os.environ.get('HOME') or '','.pybtsync'),
                  'btsync_file' : 'btsync',
                  'settings_file' : 'pybtsync'},
                 }

def _is_good_ipv4(s):
    """
    Checks if string is a good IPv4 address
    """
    # http://stackoverflow.com/questions/3462784/how-to-check-if-a-string-matches-an-ip-adress-pattern-in-python
    pieces = s.split('.')
    if len(pieces) != 4:
        return False
    try:
        return all(0<=int(p)<256 for p in pieces)
    except ValueError:
        return False

def write_conf_file(storage_path=None,
                    use_gui=False,
                    address='127.0.0.1',
                    port=None,
                    login=None,
                    password=None,
                    api_key=None,
                    conf_file_location=None):
    """
    Writes a basic sync configuration file for api communication. If no values are set all settings are randomized.
    
    :param storage_path: Path where temporary sync files will be stored.
    :type storage_path: str.

    :param use_gui: Boolean signaling if the sync GUI should be started.
    :type use_gui: boolean.

    :param address: IP address that sync will listen too, defaults to the loopback interface.
    :type address: str.     

    :param port: Port number to serve the API.
    :type port: int.
    
    :param login: Login (username) used to connect to the API.
    :type login: str.
    
    :param password: Password used to connect to the API.
    :type password: str.

    :param api_key: API key to be used.
    :type api_key: str.
    
    :param conf_file_location: Full file path to the location where the file should be saved to.
    :type conf_file_location: str.
    
    :return: path of configuration file.
    :rtype: str.
    
    :raises Exception: if ip or port are invalid values.
    """
    
    # Block below sets any variable that was not set as an input
    storage_path = storage_path or tempfile.mkdtemp()
    port = port or str(random.randrange(10000, 65000 ,1))  #http://www.bittorrent.com/help/manual/appendixa0204
    login = login or uuid.uuid4()
    password = password or uuid.uuid4()
    api_key = api_key or os.environ['PYBTSYNC_APIKEY']
    conf_file_location = conf_file_location or os.path.join(storage_path, 'sync.conf')
    
    # Code below checks if ip and port are inside expected ranges. Normally one would "ask for forgiveness",
    # but catching errors after sync started is more demanding than having this simple checks. 
    if not _is_good_ipv4(address):
        raise Exception("address is not a valid ip")
    if not 0<int(port)<=65535:
        raise Exception("port is not inside the valid port range 1-65535")
        
    # Configuration files are basically JSONs. Code below creates a dicitonary with previous values,
    # then dumps it as a JSON to the configuration file
    with open(conf_file_location,'w') as btsync_conf_file_fp:
        btsyn_conf_file_dict = {
                                "storage_path" : storage_path.replace("\\","//"), # unix <> windows
                                "use_gui" : use_gui,
                                "webui" : {
                                           "api_key" : api_key,
                                           "listen" : ":".join([address, port]),
                                           "login" : str(login),
                                           "password" : str(password),
                                           },
                                }
        json.dump(btsyn_conf_file_dict, btsync_conf_file_fp, indent=4, sort_keys=True)
        
    # returns the full file path in case it was not set
    return conf_file_location

def get_btsync():
    """
    Downloads the bittorrent sync from the bittorrent server.
    Sync will be saved to an OS dependent folder (see source for extra info).
    If a donwload happened on the last week the previously downloaded client will be used.
    
    :return: path of downloaded sync client.
    :rtype: str.
    
    """
    
    # checks if current executing platform has a proper configuration
    try:
        current_os_data = all_oses_data[platform.system()]
    except:
            raise(NotImplementedError)
    
    # Tries to load a configuration JSON file that holds the last download date
    application_folder = current_os_data['application_folder']
    settings_file = current_os_data['settings_file'] 
    try:
        with open(os.path.join(application_folder, settings_file), 'r') as settings_file_fp:
            settings = json.load(settings_file_fp)
    except:
        if not os.path.exists(application_folder):
            os.makedirs(application_folder)
        settings = {}
    
    # If no entry is present on when the last download happened, set it to a year back
    last_donwload_date_str = settings.get('last_donwload_date')
    if last_donwload_date_str:
        last_donwload_date = datetime.datetime.strptime(last_donwload_date_str, "%Y-%m-%dT%H:%M:%S.%f")
    else:
        last_donwload_date = (datetime.datetime.now() - datetime.timedelta(days=-365))
    
    #assembles application file name
    btsync_file = current_os_data['btsync_file']
    btsync_file_path = os.path.join(application_folder, btsync_file)
    
    # If downloaded more than one week ago, download it again (might be a new version)
    if (last_donwload_date -  datetime.datetime.now()).days > 7: 
        download_url = current_os_data['download_URL']
        
        response = requests.get(download_url)
        if not response.status_code == requests.codes.ok:  # @UndefinedVariable
            response.raise_for_status()
        
        try:
            if platform.system() == 'Windows':
                # normal download
                with open(btsync_file_path,'wb') as btsync:
                    btsync.write(response.content)
                    
            elif platform.system() == 'Linux':
                # On Linux the file is a tar.gz, so download it to memory and extract it to the desired path
                tar_gz = io.BytesIO()
                tar_gz.write(response.content)
                tar_gz.seek(0)
                with tarfile.open(mode='r:gz', fileobj=tar_gz) as btsync:
                    btsync.extract(btsync_file, path=application_folder)
            else:
                raise(NotImplementedError)
            
            # refresh configuration with new download date
            settings['last_donwload_date'] = datetime.datetime.now().isoformat()
        except:
            pass
    # dump configuration file to disk
    with open(os.path.join(application_folder, settings_file), 'w') as settings_file_fp:
        json.dump(settings, settings_file_fp)
        
    return btsync_file_path

class BTSyncProcess(object):
    """
    Wrapper for a sync process.
    
    :param btsync_conf_file: Path to the sync configuration file.
    :type btsync_conf_file: str.
    
    :param btsync_app: Path to the sync client application.
    :type btsync_app: str.  
    
    :attribute keep_alive: Dafaults to False. If True will ignore context switches and keep process running even after context switch is closed.
    :attribute clean_on_close: Dafaults to True. If False deletes the sync temporary folder. Ignored if keep_alive is set to True.    
    """
    def __init__(self, btsync_conf_file=None, btsync_app=None):
        
        # Load defaults if no values passed
        self.btsync_conf_file = btsync_conf_file or write_conf_file()
        self.btsync_app = btsync_app or get_btsync()
        
        # Reads configuration file and starts app
        self._read_conf_file(self.btsync_conf_file)
        self.start_process(self.btsync_app, self.btsync_conf_file)
        
        # See docstring for description
        self.keep_alive = False
        self.clean_on_close = True

    @classmethod
    def with_settings(cls, btsync_app=None, 
                           storage_path=None, use_gui=False,
                           address='127.0.0.1', port=None, login=None, password=None, api_key=None):
        """
        Instead of starting the client application from a configuration file it writes the configuration
        file and then starts the application. This function is a wrapper for :func:`write_conf_file`.
        """
              
        btsync_conf_file = write_conf_file(storage_path, use_gui, 
                                           address, port, login, password, api_key)
        
        return cls(btsync_conf_file=btsync_conf_file, btsync_app=btsync_app)


    def BTSync(self):
        """
        Returns a :class:`BTSync` object already configured to use the API.
        """
        return BTSync(self.address, self.port, self.login, self.password)

    def __del__(self):
        self.clean_up()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.clean_up()
        
    def clean_up(self):
        """
        Terminates process and cleans up temporary folder. Both actions are overriden by the ``keep_alive``, and the ``clean_on_close`` attributes. 
        """
        # Kill process if still running 
        if (not self.keep_alive) and (self.btsync_process.poll() is None):
            try:
                btsync = self.BTSync()
                btsync.shutdown()
            except:
                self.btsync_process.kill()
            
            while (self.btsync_process.poll() is None):
                pass
            
            # Clean up temporary folder
            try:                
                if self.clean_on_close:
                    shutil.rmtree(self.storage_path)
            except FileNotFoundError:
                pass


    def _read_conf_file(self, conf_file):
        """
        Reads main configuration file settings to attributes. This should be used with care.
        If a process is already running and a new configuration file is read the object will lose the ability to use the API.
        """
        with open(conf_file, 'r') as conf_file_fp:
            config = json.load(conf_file_fp)
        
        self.api_key = config['webui']['api_key']
        self.storage_path = config['storage_path']
        self.address = config['webui']['listen'].split(':')[0]
        self.port = config['webui']['listen'].split(':')[1]
        self.login = config['webui']['login']
        self.password = config['webui']['password']
        
    
    def start_process(self, btsync_app, btsync_conf_file):
        """
        Starts the sync process.
        
        :attribute btsync_process: The sync process ``subprocess.Popen`` object.
        """
        if platform.system() == 'Windows': 
            self.btsync_process = subprocess.Popen([btsync_app, '/config', btsync_conf_file])
        elif platform.system() == 'Linux': # On linux forces the 'nodaemon' switch to prevent forking
            self.btsync_process = subprocess.Popen([btsync_app, '--config', btsync_conf_file])
        else:
            raise(NotImplementedError)
        
        # dummy test to check if everything started correctly
        btsync = self.BTSync()
        btsync.get_version()

           

class _BTSyncConnect(object):
    """
    Base class which handles the connections to the API. 

    :param address: IP address that sync will listen too, defaults to the loopback interface.
    :type address: str.     

    :param port: Port number to serve the API.
    :type port: int.
    
    :param login: Login (username) used to connect to the API.
    :type login: str.
    
    :param password: Password used to connect to the API.
    :type password: str.    
    """
    def __init__(self, address, port, login, password):
        self.address=address
        self.port=port
        self.login=login
        self.password=password
        self.URL = 'http://' + self.address + ':' + self.port +'/api'
        
    def _request_function(self, method, params={}, key=None):
        """
        The function that handles connections to the API.
        
        :param method: The API function being called.
        :type method: str.
        
        :param password: Any extra parameters passed to the API.
        :type password: dict.
        
        :param key: The specific key that should be returned from the API response.
        :type key: str.   
        """
        params['method'] = method
        request_data = requests.get(self.URL, auth=(self.login, self.password), params=params).json()
        if isinstance(request_data, dict) and request_data.get('error', 0) != 0:
            raise Exception(request_data.get('message'))
        if key:
            return request_data[key]
        return request_data
    
class BTSync(_BTSyncConnect):
    """
    The main abstract object used to deal with the API.
    
    :param address: IP address that sync will listen too, defaults to the loopback interface.
    :type address: str.     

    :param port: Port number to serve the API.
    :type port: int.
    
    :param login: Login (username) used to connect to the API.
    :type login: str.
    
    :param password: Password used to connect to the API.
    :type password: str.   
    
    """
    def __init__(self, address, port, login, password):
        super().__init__(address, port, login, password)
 
    def get_folders(self,secret=None):
        """
        Returns a list with folders info. If a secret is specified, will return info about the folder with this secret.
        `Get folders documentation. <http://www.bittorrent.com/sync/api#getFolder>`_
        
        :param secret: Requests specific folder info.
        :type secret: str.
        
        :return: List with folders info.
        :rtype: list.
        
        """
        return self._request_function(inspect.stack()[0][3], locals())

    def add_folder(self, dir, secret='', selective_sync=0):  # @ReservedAssignment
        """
        Adds a folder to Sync. If a secret is not specified, it will be generated automatically.
        The folder will have to pre-exist on the disk and Sync will add it into a list of syncing folders.
        `Add folder documentation. <http://www.bittorrent.com/sync/api#addFolder>`_

        :param secret: Specifies the directory secret that should be used.
        :type secret: str.
        
        :param selective_sync: Turns on or off the folder selective sync. Off by default.
        :type selective_sync: str.
         
        """
        force = 1 
        return self._request_function(inspect.stack()[0][3], locals())

    def remove_folder(self, secret):
        """
        Removes folder from Sync while leaving actual folder and files on disk.
        It will remove a folder from the Sync list of folders and does not touch any files or folders on disk. 
        `Remove folder documentation. <http://www.bittorrent.com/sync/api#removeFolder>`_

        :param secret: Specifies the directory secret that should be used.
        :type secret: str.
         
        """
        return self._request_function(inspect.stack()[0][3], locals())

    def get_files(self, secret, path=None):
        """
        Returns list of files within the specified directory.
        If a directory is not specified, will return list of files and folders within the root folder. 
        `Get files documentation. <http://www.bittorrent.com/sync/api#getFiles>`_

        :param secret: Specifies the directory secret that should be used.
        :type secret: str.

        :param path: Specifies the directory of interest.
        :type path: str.
        
        :return: List with files info.
        :rtype: list.
         
        """        
        return self._request_function(inspect.stack()[0][3], locals())

    def set_file_prefs(self, secret, path, download): #relative path
        """
        Selects file for download for selective sync folders. Returns file information with applied preferences.
        `Set file preferences documentation. <http://www.bittorrent.com/sync/api#setFilePref>`_

        :param secret: Specifies the directory secret that should be used.
        :type secret: str.

        :param path: Specifies the file of interest.
        :type path: str.

        :param download: Set selective sync.
        :type download: int. (1-0)
         
        """   
        return self._request_function(inspect.stack()[0][3], locals())
            
    def get_folder_peers(self, secret):
        """
        Returns list of peers connected to the specified folder.
        `Get folder peer documentation. <http://www.bittorrent.com/sync/api#getPeers>`_

        :param secret: Specifies the directory secret that should be used.
        :type secret: str.

        :return: List with peers info.
        :rtype: list.
         
        """         
        return self._request_function(inspect.stack()[0][3], locals())
    
    def get_secrets(self, secret=None, type='encryption'): #encryption enabled always @ReservedAssignment
        """
        Generates read-write, read-only and encryption read-only secrets.
        If ‘secret’ parameter is specified, will return secrets available for sharing under this secret.
        This is a secret for a read-only peer with encrypted content (the peer can sync files but can not see their content).
        One example use is if a user wanted to backup files to an untrusted, unsecure, or public location.
        `Get secrets documentation. <http://www.bittorrent.com/sync/api#getSecrets>`_

        :param secret: Specifies the directory secret that should be used.
        :type secret: str.

        :param type: One of the following: encryption, read_write, or read_only
        :type type: str.

        :return: Folder secrets.
        :rtype: Dict.
         
        """     
        return self._request_function(inspect.stack()[0][3], locals())
        
    def get_folder_prefs(self, secret, pref=None):
        """
        Returns preferences for the specified sync folder.
        `Get folder preferences documentation. <http://www.bittorrent.com/sync/api#getFolderPref>`_

        :param secret: Specifies the directory secret that should be used.
        :type secret: str.

        :return: Folder preferences.
        :rtype: Dict.
        """          
        return self._request_function(inspect.stack()[0][3], locals(), key=pref)
    
    def set_folder_prefs(self, secret,
                         search_lan=None, use_dht=None, use_hosts=None, use_relay_server=None, use_sync_trash=None, use_tracker=None):
        """
        Sets preferences for the specified sync folder. Parameters are the same as in :func:`get_folder_prefs`
        `Set folder preferences documentation. <http://www.bittorrent.com/sync/api#setFolderPref>`_

        :param secret: Specifies the directory secret that should be used.
        :type secret: str.

        :return: Folder preferences.
        :rtype: Dict.
        """              
        params = locals()
        keys = params.keys()
        for key in keys:
            if params[key] is None:
                params.pop(key)
        return self._request_function(inspect.stack()[0][3], params)
    
    def get_folder_hosts(self, secret):
        """
        Returns list of predefined hosts for the folder.
        `Get folder hosts documentation. <http://www.bittorrent.com/sync/api#getFolderHost>`_

        :param secret: Specifies the directory secret that should be used.
        :type secret: str.

        :return: Hosts list.
        :rtype: List.
        """     
        return self._request_function(inspect.stack()[0][3], locals(), 'hosts')
    
    def set_folder_hosts(self, secret, hosts):
        """
        Sets one or several predefined hosts for the specified sync folder. Existing list of hosts will be replaced. Hosts should be added as values of the ‘host’ parameter and separated by commas.
        `Set folder hosts documentation. <http://www.bittorrent.com/sync/api#setFolderHost>`_

        :param secret: Specifies the directory secret that should be used.
        :type secret: str.

        :param hosts: Comma separated list of host:port.
        :type hosts: str.

        :return: Folder preferences.
        :rtype: Dict.
        """  
        return self._request_function(inspect.stack()[0][3], locals())

    def get_prefs(self, pref=None):
        """
        Returns BitTorrent Sync preferences.
        `Get Preferences documentation. <http://www.bittorrent.com/sync/api#getPref>`_

        :param secret: Specifies the directory secret that should be used.
        :type secret: str.

        :return: Folder preferences.
        :rtype: Dict.
        """  
        return self._request_function(inspect.stack()[0][3], key=pref)

    def set_prefs(self, device_name=None, disk_low_priority=None, download_limit=None, folder_rescan_interval=None,
                        lan_encrypt_data=None, lan_use_tcp=None, lang=None, listening_port=None, max_file_size_diff_for_patching=None,
                        max_file_size_for_versioning=None, rate_limit_local_peers=None, send_buf_size=None, sync_max_time_diff=None, 
                        sync_trash_ttl=None, upload_limit=None, use_upnp=None, recv_buf_size=None):
        """
        Sets BitTorrent Sync preferences. Parameters are the same as in :func:`get_prefs`.
        Parameters not documented purposily.
        `Get Preferences documentation. <http://www.bittorrent.com/sync/api#getPref>`_

        :return: Current preferences.
        :rtype: Dict.
        """ 
        params = locals()
        keys = params.keys()
        for key in keys:
            if params[key] is None:
                params.pop(key)
        return self._request_function(inspect.stack()[0][3], params)

    def get_os(self):
        """
        Returns OS name where BitTorrent Sync is running.
        `Get OS documentation. <http://www.bittorrent.com/sync/api#getOS>`_

        :return: OS Name.
        :rtype: str.
        """         
        return self._request_function(inspect.stack()[0][3], locals(), 'os')

    def get_version(self):
        """
        Returns Returns BitTorrent Sync version.
        `Get Version documentation. <http://www.bittorrent.com/sync/api#getVersion>`_

        :return: Sync version.
        :rtype: str.
        """           
        return self._request_function(inspect.stack()[0][3], locals(), 'version')

    def get_speed(self):
        """
        Returns current upload and download speed.
        `Get speed documentation. <http://www.bittorrent.com/sync/api#getSpeed>`_

        :return: current upload and download speed.
        :rtype: str.
        """           
        return self._request_function(inspect.stack()[0][3], locals())
    
    def shutdown(self):
        """
        Gracefully stops Sync.
        `Shutdown documentation. <http://www.bittorrent.com/sync/api#shutdown>`_

        :return: 0 on sucess, other values on failure.
        :rtype: int.
        """           
        return self._request_function(inspect.stack()[0][3], locals(), 'error')

