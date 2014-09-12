import json
import urllib2

BASE_URL  = 'https://api.meetup.com'
GROUP_URL = 'PyMNtos-Twin-Cities-Python-User-Group'
GROUP_ID  = 9892262

class Meetup(object):
    def __init__(self, api_key):
        self.api_key = api_key

    def request(self, path):
        url = '{0}/{1}/?key={2}'.format(BASE_URL, path, self.api_key)
        resp = urllib2.urlopen(url)
        return json.loads(resp.read())

    def group_info(self):
        return self.request(GROUP_URL)

    def next_meeting(self):
        group = self.group_info()
        event_id = group['next_event']['id']
        return self.request('2/event/' + event_id)