import time
import datetime
import hashlib
import requests
from Crypto.Random.random import StrongRandom
import flask
import functools

PARAMS = {
    'schema': 'http',
    'host': '127.0.0.1',
    'port': 4001
}

SESSION_TIMEOUT = 1800 # 1/2h

class DissectException(Exception):
    pass

class Session():

    INVALID_SESSION='-1'

    def __init__(self, cookie_jar=None):

        self.salt = self.get_salt()
        self.sid = Session.INVALID_SESSION
        self.cookie_jar = cookie_jar
        self.restore()

#============================================================================================================
    def new(self):
        self.sid = self.get_new_session_id()

#============================================================================================================
    def restore(self):
        if self.cookie_jar.get('dsid') and self.is_valid_session(self.cookie_jar.get('dsid')):
            self.sid = self.cookie_jar.get('dsid')
            self.touch()
        else:
            self.sid = Session.INVALID_SESSION

#============================================================================================================
    def set_cookie(self, response):
        """
        Sets a cookie on the client's browser.
        This function is specific for the web2py framework.
        """
        if self.sid == Session.INVALID_SESSION:
            response.set_cookie('dsid', expires=0)
        else:
            expires = int(time.time()) + SESSION_TIMEOUT
            response.set_cookie('dsid', value=self.sid, expires=expires, path='/', httponly=True)
        return response

#============================================================================================================
    def rm_cookie(self):
        """
        Clears a cookie on the client's browser.
        This function is specific for the web2py framework.
        """

        self.sid = Session.INVALID_SESSION

#============================================================================================================
    def get_salt(self):
        """
        Read the salt value from the shared database.
        """

        params = PARAMS.copy()
        params['sid'] = '__shared_key__'
        url = '%(schema)s://%(host)s:%(port)d/v2/keys/%(sid)s' % params

        res = requests.get(url)

        if not res.ok:
            raise DissectException, 'Failed to connect to URL: %s' % url

        try:
            return res.json()['node']['value']
        except:
            raise DissectException, 'Invalid system salt.'

#============================================================================================================
    def get_new_session_id(self):
        """
        Generate a new SessionID value. By default, it is 128 bits wide.
        """

        NUM_BITS = 128

        id = StrongRandom().getrandbits(NUM_BITS)

        bts=[]
        for i in xrange(NUM_BITS/8):
            p = id & 0xFF
            id = id >> 8
            bts.append('%02X' % p)
        bts.reverse()
        sidonly = ''.join(bts).lower()
        hsh = self.get_hash(sidonly)
        return sidonly+'-'+hsh

#============================================================================================================
    def is_valid_session(self, session_id):
        """
        Compares the provided session id signature with the calculated one, using the stored salt obtained from the database.
        """
        sidonly, hash = session_id.split('-')[0:2]
        calc_hash = self.get_hash(sidonly)
        return calc_hash == hash

#============================================================================================================
    def get_hash(self, sid):
        """
        Utility method to calculate the 64 bits part of the 256 bits hash signature. Internal use only.
        """
        return hashlib.sha256(sid+self.salt).hexdigest()[10:26]

#============================================================================================================
    def getAll(self):
        """
        Returns all the values stored under the key as a dictionary.
        """

        self.touch()

        params = PARAMS.copy()
        params['sid'] = self.sid
        url = '%(schema)s://%(host)s:%(port)d/v2/keys/%(sid)s' % params

        res = requests.get(url)

        if not res.ok:
            #raise DissectException, 'Failed to connect to URL: %s' % url
            return None

        result_dict = {}

        try: 
            for i in res.json()['node']['nodes']:
                key = i['key'].split('/')[-1]
                value = i.get('value')
                result_dict[key] = value
        except:
            pass # returns {} in worst case

        return result_dict

#============================================================================================================
    def __getitem__(self, key):
        return self.get(key)
#============================================================================================================
    def get(self, key):
        """
        Returns the value identified by the provided key.
        """

        self.touch()

        params = PARAMS.copy()
        params['sid'] = self.sid
        params['key'] = key
        url = '%(schema)s://%(host)s:%(port)d/v2/keys/%(sid)s/%(key)s' % params

        res = requests.get(url)

        if not res.ok:
            #raise DissectException, 'Failed to connect to URL: %s' % url
            return None

        try:
            return res.json()['node']['value']
        except:
            return None

#============================================================================================================
    def __setitem__(self, key, value):
        self.put(key, value)
#============================================================================================================
    def put(self, key, value):
        """
        Sets or updates a key with a new value.
        """

        self.touch()

        if type(key) not in [str, int, long]:
            raise DissectException, 'The session key must be either a string or integer. Found '+str(type(key))

        if type(value) not in [str, int, long, bool]:
            raise DissectException, 'The session value must be either a string or integer. Found '+str(type(value))

        params = PARAMS.copy()
        params['sid'] = self.sid
        params['key'] = key

        dir_url = '%(schema)s://%(host)s:%(port)d/v2/keys/%(sid)s' % params
        requests.put(dir_url, {'dir': True})

        url = '%(schema)s://%(host)s:%(port)d/v2/keys/%(sid)s/%(key)s' % params
        dic = {'value': value}

        try:
            requests.put(url, dic)
        except:
            raise DissectException, 'Unable to put key: '+str(key)

#============================================================================================================
    def putAll(self, dic):
        """
        Utiliry method to batch store all key-values pairs in a dictionary on the session.
        """

        self.touch()

        if type(dic) != dict:
            raise DissectException, 'The argument must be a dictionary. Found '+str(type(key))

        for k in dic.keys():
            try:
                self.put(k, dic[k])
            except:
                raise DissectException, 'Failed to set key: '+str(k)

#============================================================================================================
    def touch(self):
        """
        Utility method to reset the session timestamp. Internal use only.
        """

        params = PARAMS.copy()
        params['sid'] = self.sid

        url = '%(schema)s://%(host)s:%(port)d/v2/keys/%(sid)s/__last_updated__' % params
        dic = {'value': int(time.time())}

        try:
            requests.put(url, dic)
        except:
            raise DissectException, 'Unable to put timestamp'

#============================================================================================================
    def __delitem__(self, key):
        self.delete(key)
#============================================================================================================
    def delete(self, key):
        """
        Deletes the value associated with the provided key.
        """

        self.touch()

        params = PARAMS.copy()
        params['sid'] = self.sid
        params['key'] = key
        url = '%(schema)s://%(host)s:%(port)d/v2/keys/%(sid)s/%(key)s' % params

        res = requests.delete(url)

        return res.ok

#============================================================================================================
    def deleteAll(self):
        """
        Deletes all the key-values pairs under this session.
        """

        self.touch()

        dic = self.getAll()

        for k in dic.keys():
            try:
                self.delete(k)
            except:
                raise DissectException, 'Failed to delete key: '+str(k)

#============================================================================================================
    def destroy(self, sid=None):
        """
        Removes the session entry on the database.
        """
        params = PARAMS.copy()
        if not sid:
            params['sid'] = self.sid
        else: 
            params['sid'] = sid
        url = '%(schema)s://%(host)s:%(port)d/v2/keys/%(sid)s?dir=true&recursive=true' % params

        res = requests.delete(url)

        self.rm_cookie()
        
        return res.ok



#============================================================================================================
    def session_destroy(self):
        """
        Completely deletes session from database and clears the client's cookie.
        """

        self.destroy()
        self.rm_cookie()

#============================================================================================================
#============================================================================================================
def gc():


    params = PARAMS.copy()
    url = '%(schema)s://%(host)s:%(port)d/v2/keys/?dir=true' % params

    res = requests.get(url)

    if not res.ok:
        #raise DissectException, 'Failed to connect to URL: %s' % url
        return False

    sids = []

    try: 
        for i in res.json()['node']['nodes']:
            key = i['key'].split('/')[-1]
            sids.append(key)
    except:
        pass # returns {} in worst case

    gcan = []

    for sid in sids:
        params['sid'] = sid
        url = '%(schema)s://%(host)s:%(port)d/v2/keys/%(sid)s/__last_updated__' % params
        res = requests.get(url)


        if res.ok:
            last = int(res.json()['node']['value'])
            if time.time()-last > SESSION_TIMEOUT:
                gcan.append(sid)
        else:
            gcan.append(sid)

    total = len(gcan)

    for sid in gcan:
        params['sid'] = sid
        url = '%(schema)s://%(host)s:%(port)d/v2/keys/%(sid)s?dir=true&recursive=true' % params
        res = requests.delete(url)
        if not res.ok:
            print 'Failed for %s' % sid
            total -= 1

    print 'Entries purged: %d.' % total

#============================================================================================================
