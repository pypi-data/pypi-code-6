__all__ = ['FoscamH264Camera']

from urllib import urlencode, unquote_plus
import time
import xmltodict

import requests
from requests.exceptions import ConnectionError, Timeout

from bosunplugins.devices import Device


# camera url mappings
camera_urls = {
    'capture': '/cgi-bin/CGIProxy.fcgi?cmd=snapPicture2',
    'set_snap': '/cgi-bin/CGIProxy.fcgi?cmd=setSnapConfig',

    'set_osd': '/cgi-bin/CGIProxy.fcgi?cmd=setOSDSetting',

    'get_uuid': '/cgi-bin/CGIProxy.fcgi?cmd=getDevName',
    'set_uuid': '/cgi-bin/CGIProxy.fcgi?cmd=setDevName',

    'set_alarm': '/cgi-bin/CGIProxy.fcgi?cmd=setMotionDetectConfig',
    'get_alarm': '/cgi-bin/CGIProxy.fcgi?cmd=getMotionDetectConfig',

    'set_ftp': '/cgi-bin/CGIProxy.fcgi?cmd=setFtpConfig',
    'get_ftp': '/cgi-bin/CGIProxy.fcgi?cmd=getFtpConfig',

    'scan_for_wifi': '/cgi-bin/CGIProxy.fcgi?cmd=refreshWifiList',
    'get_wifi_results': '/cgi-bin/CGIProxy.fcgi?cmd=getWifiList&startNo=0',
    'set_wifi': '/cgi-bin/CGIProxy.fcgi?cmd=setWifiSetting',

    'set_startup_mode': '/cgi-bin/CGIProxy.fcgi?cmd=setPTZSelfTestMode',
    'get_startup_mode': '/cgi-bin/CGIProxy.fcgi?cmd=getPTZSelfTestMode',

    'set_infrared_config': '/cgi-bin/CGIProxy.fcgi?cmd=setInfraLedConfig',
    'get_infrared_config': '/cgi-bin/CGIProxy.fcgi?cmd=getInfraLedConfig',

    'infrared_on': '/cgi-bin/CGIProxy.fcgi?cmd=openInfraLed',
    'infrared_off': '/cgi-bin/CGIProxy.fcgi?cmd=closeInfraLed',
}

# wifi mode mappings forwards and backwards
ap_modes = {
    0: 'infrastructure',
    1: 'adhoc',

    'infrastructure': 0,
    'adhoc': 1,
}

# wifi auth mappings forwards and backwards
ap_auth_types = {
    0: 'open',
    1: 'wep',
    2: 'wpa',
    3: 'wpa2',
    4: 'wpa/wpa2',

    'open': 0,
    'wep': 1,
    'wpa': 2,
    'wpa2': 3,
    'wpa/wpa2': 4
}


class FoscamH264Camera(Device):

    # BOSUN PLUGIN METHODS / ATTRIBUTES #

    verbose_name = 'Foscam H.264 HD Camera'

    ports_to_scan = [88]

    @classmethod
    def is_my_type(cls, host, port):
        try:
            response = requests.get(cls._base_make_camera_url(host=host, port=port, url_name='get_uuid'), timeout=cls.detection_timeout)
            # TODO: make this detection stronger
            if response.status_code == 200 and response.content.startswith('<CGI_Result>'):
                return True
        except (ConnectionError, Timeout):
            pass
        return False

    credentials_field_names = ('username', 'password')

    def get_uuid(self):
        response = requests.get(self._make_camera_url('get_uuid'))
        doc = xmltodict.parse(response.content)
        return doc['CGI_Result']['devName']

    def set_uuid(self, uuid):
        params = {
            'devName': uuid
        }
        url = self._make_camera_url('set_uuid') + '&' + urlencode(params)

        requests.get(url)

    def authenticate(self, username, password):
        response = requests.get(self._make_camera_url('get_uuid', username=username, password=password))
        doc = xmltodict.parse(response.content)
        # result = 0 means success, -2 means bad username and password
        result = doc['CGI_Result']['result']
        if result == '0':
            return True
        elif result == '-2':
            return False
        else:
            raise Exception("Bad result from camera for auth test: {}".format(result))

    def connect_to_bosun(self):
        # configure snap settings
        self._set_snap_config()
        # disable the OSD
        self._set_osd_config()
        # do no "startup dance"
        self._set_startup_mode('none')
        # disable the infrared
        self._set_infrared_config('manual')
        self._set_infrared('off')
        # configure the ftp
        # get the base URL from the handler
        self.set_ftp_config(
            self.handle_ftp_upload.get_base_url(),
            self.handle_ftp_upload.ftp_port,
            self.handle_ftp_upload.ftp_username,
            self.handle_ftp_upload.ftp_password,
        )

        # set up motion detection *only if not already configured*.
        # this will wipe out existing settings otherwise.
        if not self.is_detecting():
            self.configure_detection()

    def is_connected_to_bosun(self):
        # the callback must be properly set to the base FTP url, and
        # detection must be on
        return self._get_alarm_callback() == self.handle_ftp_upload.get_base_url() and self.is_detecting()

    # CAPABILITIES METHODS #

    @Device.action('action.camera.still.capture')
    def capture_still_on_demand(self):
        return {
            'image': self.load_image(),
            'mimetype': 'image/jpeg',
        }

    @Device.emits('event.camera.still.capture')
    def capture_still_on_alarm(self):
        return {
            'image': self.load_image(),
            'mimetype': 'image/jpeg',
        }

    # LISTENERS #

    @Device.listeners.ftp.watched_folder('/snap')
    def handle_ftp_upload(self, filelike):
        """ The uploaded file is terrible, so disregard the filelike and emit a capture event instead. """
        self.capture_still_on_alarm()

    # INTERNAL METHODS #

    def configure_detection(self):
        """ Sets up default alarm settings. """

        base_url = self._make_camera_url('set_alarm')

        params = {
            'isEnable': 1,
            # how camera reacts to motion bin2dec(bit3: record, bit2: picture, bit1:email, bit0:ring)
            'linkage': 4,
            'snapInterval': 10,
            'sensitivity': 0,
            'triggerInterval': 5,
            # default schedule is 24-7
            'schedule0': 281474976710655,
            'schedule1': 281474976710655,
            'schedule2': 281474976710655,
            'schedule3': 281474976710655,
            'schedule4': 281474976710655,
            'schedule5': 281474976710655,
            'schedule6': 281474976710655,
            # default trigger area is 100% of frame
            'area0': 1023,
            'area1': 1023,
            'area2': 1023,
            'area3': 1023,
            'area4': 1023,
            'area5': 1023,
            'area6': 1023,
            'area7': 1023,
            'area7': 1023,
            'area8': 1023,
            'area9': 1023
        }
        url = base_url + '&' + urlencode(params)

        requests.get(url)

    def is_detecting(self):
        response = requests.get(self._make_camera_url('get_alarm'))
        doc = xmltodict.parse(response.content)
        # isEnable says whether or not detection is turned on
        return doc['CGI_Result']['isEnable'] == '1'

    def set_ftp_config(self, ftp_url, ftp_port, user_name, password):
        base_url = self._make_camera_url('set_ftp')

        params = {
            'ftpAddr': ftp_url,
            'ftpPort': ftp_port,
            'mode': 0,
            'userName': user_name,
            'password': password
        }
        url = base_url + '&' + urlencode(params)

        requests.get(url)

    def load_image(self):
        response = requests.get(self._make_camera_url('capture'))
        if not response.status_code == 200:
            raise Exception("Error getting image")
        return response.content

    # TODO: still needs tweaking
    def get_access_points(self):
        # trigger a scan for wifi
        requests.get(self._make_camera_url('scan_for_wifi'))

        # try to get the results forever
        while True:
            response = requests.get(self._make_camera_url('get_wifi_results'))
            if response.content:
                break
            # if we didn't get it, sleep for a quarter second
            time.sleep(0.25)

        access_points = []

        doc = xmltodict.parse(response.content)

        for key, value in doc['CGI_Result'].iteritems():

            if key[:2] == 'ap' and isinstance(value, basestring):
                # these are url quoted
                ssid, mac_address, signal_quality, is_encrypted, encrypt_type = unquote_plus(value).rsplit('+', 5)
                access_point = {
                    'ssid': ssid,
                    'mode': 'infrastructure',
                    'auth_type': ap_auth_types[int(encrypt_type)],
                }
                access_points.append(access_point)

        return access_points

    def set_wifi(self, ssid, mode, auth_type, password):
        params = {
            'isEnable': 1,
            'isUseWifi': 1,
            'ssid': ssid,
            'netType': ap_modes[mode],
            'encryptType': ap_auth_types[auth_type],

            # wep params
            'authMode': 0,
            'keyFormat': 0,
            'defaultKey': 0,
            'key1': '',
            'key2': '',
            'key3': '',
            'key4': '',
            'key1Len': 0,
            'key2Len': 0,
            'key3Len': 0,
            'key4Len': 0,

            # wpa params
            'psk': password,
        }

        # add logic here to determine if auth_type is WEP and
        # update params acordingly by looking at password

        url = self._make_camera_url('set_wifi') + '&' + urlencode(params)
        requests.get(url)

    @staticmethod
    def _base_make_camera_url(host, port, url_name, **kwargs):
        """ Helper for making the full camera url that doesn't need an instance """
        url = 'http://{host}:{port}{url}'.format(host=host, port=port, url=camera_urls[url_name])

        # url encode any kwargs we were given as well
        if kwargs:
            url = '{base}&{params}'.format(base=url, params=urlencode(kwargs))

        return url

    def _make_camera_url(self, url_name, **kwargs):
        """ Make the requested url for this instance (provides credentials automatically) """
        # updates kwargs with credentials, defaulting to kwargs, if supplied
        kwargs['usr'] = kwargs['username'] if 'username' in kwargs else self.credentials['username']
        kwargs['pwd'] = kwargs['password'] if 'password' in kwargs else self.credentials['password']
        return self._base_make_camera_url(self.host, self.port, url_name, **kwargs)

    def _get_alarm_callback(self):
        """ Get the camera's currently configured FTP callback URL """
        response = requests.get(self._make_camera_url('get_ftp'))

        doc = xmltodict.parse(response.content)
        # totally unconfigured cameras come back with this as None
        ftp_address = doc['CGI_Result']['ftpAddr'] or ''
        # the address is url quoted in the new firmware
        ftp_address = unquote_plus(ftp_address)
        if ftp_address:
            return ftp_address
        else:
            return ''

    def _set_snap_config(self):
        """ Set the camera to send captured images ('snaps') to FTP """
        base_url = self._make_camera_url('set_snap')

        params = {
            # The documentation for this says 'snapPicQuality', but the param is actually 'snapQuality'.
            # There is a bug where using the high quality setting can wreck something:
            # http://foscam.us/forum/fi9805w-snapshot-image-quality-t6205.html
            # quality: 0-low, 1-normal, 2-high
            'snapQuality': 1,
            # save_location: 0-SD, 1-nope, 2-FTP
            'saveLocation': 2,
        }
        url = base_url + '&' + urlencode(params)

        requests.get(url)

    def _set_osd_config(self):
        """ Remove the OSD, so that timestamp and device name aren't displayed on captured images """
        base_url = self._make_camera_url('set_osd')

        params = {
            'isEnableTimeStamp': 0,
            'isEnableDevName': 0,
            'dispPos': 0,
            'isEnableOSDMask': 0
        }
        url = base_url + '&' + urlencode(params)

        requests.get(url)

    def _set_startup_mode(self, mode):
        """ Set where the camera moves to on startup """
        modes = ('none', 'normal', 'preset')
        if not mode in modes:
            raise Exception("Bad option, 'mode' must be in {}".format(modes))

        mode_id = modes.index(mode)

        response = requests.get(self._make_camera_url('set_startup_mode', mode=mode_id))
        if not response.status_code == 200:
            raise Exception("Could not set startup mode.")

    def _set_infrared_config(self, mode):
        """ Set infrared to auto or manual """
        modes = ('auto', 'manual')
        if not mode in modes:
            raise Exception("Bad option, 'mode' must be in {}".format(modes))

        mode_id = modes.index(mode)

        response = requests.get(self._make_camera_url('set_infrared_config', mode=mode_id))
        if not response.status_code == 200:
            raise Exception("Could not set infrared mode")

    def _set_infrared(self, mode):
        """ If infrared is configured to be manual, use this to turn it on or off """
        if mode == 'on':
            requests.get(self._make_camera_url('infrared_on'))
        elif mode == 'off':
            requests.get(self._make_camera_url('infrared_off'))
        else:
            raise Exception("Bad option, 'mode' must be in 'on' or 'off'")
