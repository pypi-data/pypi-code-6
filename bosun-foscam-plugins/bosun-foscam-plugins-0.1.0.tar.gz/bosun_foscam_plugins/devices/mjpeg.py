__all__ = ['FoscamMJPEGCamera']

import re
from urllib import urlencode
import time

import requests
from requests.auth import HTTPDigestAuth
from requests.exceptions import ConnectionError, Timeout

from bosunplugins.devices import Device


# camera urls
camera_urls = {
    'capture': '/snapshot.cgi',

    'get_uuid': '/get_params.cgi',
    'set_uuid': '/set_msn.cgi',

    'set_alarm': '/set_alarm.cgi',
    'get_alarm': '/get_params.cgi',

    'scan_for_wifi': '/wifi_scan.cgi',
    'get_wifi_results': '/get_wifi_scan_result.cgi',
    'set_wifi': '/set_wifi.cgi',
}

ap_modes = {
    0: 'infrastructure',
    1: 'adhoc',

    'infrastructure': 0,
    'adhoc': 1,
}

# forwards and backwards
ap_auth_types = {
    1: 'wep',
    2: 'wpa-tkip',
    3: 'wpa-aes',
    4: 'wpa2-aes',
    5: 'wpa2-tkip+aes',

    'wep': 1,
    'wpa-tkip': 2,
    'wpa-aes': 3,
    'wpa2-aes': 4,
    'wpa2-tkip+aes': 5,
}

js_regex = re.compile(r"var (\w+)=(.*);$")

def scrape_js(js):
    data = {}
    for line in js.split('\n'):
        match = js_regex.match(line)
        if match:
            value = match.group(2)
            # everything that isn't a single-quote string is an int
            if not (value.startswith("'") and value.endswith("'")):
                value = int(value)
            # strip the quotes from the stinrgs
            else:
                value = value.strip("'")
            data[match.group(1)] = value
    return data


class FoscamMJPEGCamera(Device):

    # BOSUN PLUGIN METHODS / ATTRIBUTES #

    verbose_name = 'Foscam MJPEG Camera'

    ports_to_scan = [80]

    @staticmethod
    def is_my_type(host, port):
        try:
            response = requests.get("http://{}:{}/get_status.cgi".format(host, port), timeout=FoscamMJPEGCamera.detection_timeout)
            # 11.37.2.49
            if response.status_code == 200 and response.content.startswith('var id'):
                return True
            # 11.37.2.56
            elif response.headers.get('WWW-Authenticate', '').startswith('Digest realm="ipcamera_'):
                return True
        except (ConnectionError, Timeout):
            pass
        return False

    credentials_field_names = ('username', 'password')

    def get_uuid(self):
        response = requests.get(self.make_camera_url('get_uuid'))
        match = re.search(r"var msn_friend1='([\w-]*)';", response.content)
        if match:
            return match.group(1)
        else:
            return ''

    def set_uuid(self, uuid):
        params = {
            'next_url': 'msn.htm',
            'friend1': uuid,
        }
        url = self.make_camera_url('set_uuid') + '&' + urlencode(params)

        response = requests.get(url, auth=self.get_requests_auth())
        if not response.status_code == 200:
            raise Exception("Error saving UUID")

    def authenticate(self, username, password):
        response = requests.get(self.make_camera_url('get_alarm'), auth=HTTPDigestAuth(username, password))
        return response.status_code == 200

    def connect_to_bosun(self):
        # get the settings to preserve some user settings
        settings = self.get_settings()
        base_url = self.make_camera_url('set_alarm')

        params = {
            'next_url': 'alarm.htm',
            'motion_armed': 1,
            'input_armed': 1,
            'motion_sensitivity': settings['alarm_motion_sensitivity'],
            'iolinkage': settings['alarm_iolinkage'],
            'mail': 0,
            'upload_interval': 0,
            'http': 1,
            # give the url for handle_alarm_callback()
            'http_url': self.handle_alarm_callback.get_url(),
            'schedule_enable': settings['alarm_schedule_enable'],
        }
        url = base_url + '&' + urlencode(params)

        response = requests.get(url, auth=self.get_requests_auth())

        if not response.status_code == 200:
            raise Exception("Error auto configuring")

    def is_connected_to_bosun(self):
        # alarm callback is correct, and it's detecting
        return self.get_alarm_callback() == self.handle_alarm_callback.get_url() and self.is_detecting()


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

    @Device.listeners.http.route('/capture')
    def handle_alarm_callback(self):
        """ This route is called when the alarm goes off. Generate a capture event. """
        self.capture_still_on_alarm()

        # send back a response for flask
        return '', 200


    # INTERNAL METHODS #

    def get_requests_auth(self):
        return HTTPDigestAuth(self.credentials['username'], self.credentials['password'])

    def load_image(self):
        response = requests.get(self.make_camera_url('capture'), auth=self.get_requests_auth())
        if not response.status_code == 200:
            raise Exception("Error getting image")
        return response.content

    def get_access_points(self):
        # trigger a scan for wifi
        requests.get(self.make_camera_url('scan_for_wifi'))

        # try to get the results forever
        while True:
            response = requests.get(self.make_camera_url('get_wifi_results'), auth=self.get_requests_auth())
            if response.content:
                break
            # if we didn't get it, sleep for a quarter second
            time.sleep(0.25)

        access_points = []
        lines = response.content.split('\n')

        # first 4 lines and last 2 lines are garbage
        for i in xrange(4, len(lines) - 2, 4):

            bssid_line = lines[i + 0]
            match = re.search(r"=([^;]+);", bssid_line)
            bssid = match.group(1).strip("'")

            ssid_line = lines[i + 1]
            match = re.search(r"=([^;]+);", ssid_line)
            ssid = match.group(1).strip("'")

            mode_line = lines[i + 2]
            match = re.search(r"=([^;]+);", mode_line)
            mode_id = match.group(1).strip("'")
            mode_id = int(mode_id)

            auth_type_line = lines[i + 3]
            match = re.search(r"=([^;]+);", auth_type_line)
            auth_type_id = match.group(1).strip("'")
            auth_type_id = int(auth_type_id)

            access_point = {
                'bssid': bssid,
                'ssid': ssid,
                'mode': ap_modes[mode_id],
                'auth_type': ap_auth_types[auth_type_id],
            }
            access_points.append(access_point)

        return access_points

    def set_wifi(self, ssid, mode, auth_type, password):
        params = {
            'enable': 1,
            'ssid': ssid,
            'mode': ap_modes[mode],
            'encrypt': ap_auth_types[auth_type],
            'next_url': 'rebootme.htm',

            # wep params
            'authtype': 0,
            'keyformat': 0,
            'defkey': 0,
            'key1': '',
            'key2': '',
            'key3': '',
            'key4': '',
            'key1_bits': 0,
            'key2_bits': 0,
            'key3_bits': 0,
            'key4_bits': 0,

            # wpa params
            'wpa_psk': password,
        }

        # add logic here to determine if auth_type is WEP and
        # update params acordingly by looking at password

        url = self.make_camera_url('set_wifi') + '&' + urlencode(params)
        response = requests.get(url, auth=self.get_requests_auth())
        if not response.status_code == 200:
            raise Exception("Error setting wifi")

    def get_settings(self):
        response = requests.get(self.make_camera_url('get_alarm'))
        return scrape_js(response.content)

    def is_detecting(self):
        settings = self.get_settings()
        return bool(settings['alarm_input_armed']) and bool(settings['alarm_motion_armed'])

    def make_camera_url(self, name):
        return 'http://{host}{url}?user={username}&pwd={password}'.format(host=self.host, url=camera_urls[name], **self.credentials)

    def get_alarm_callback(self):
        return self.get_settings()['alarm_http_url']
