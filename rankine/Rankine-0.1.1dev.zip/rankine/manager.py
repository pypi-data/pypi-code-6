from core import RankineError, Call


class Manager(object):
    _raw = None # overwritten with most recent
    _result = None # overwritten with most recent
    _call = None # overwritten with most recent
    supported = None # overwritten by get_supported()
    
    
    def __init__(self, api_key, response_format='json',
                 populate_supported=True):
        self._api_key = api_key
        self._response_format = response_format
        if populate_supported:
            self._get_supported()
    
    
    def call(self, method, **kwargs):
        self._call = Call(api_key=self._api_key, method=method,
            response_format=self._response_format, **kwargs)
        self._raw = self._call.get()
        return self._raw
        
    
    def _get_supported(self):
        """
        Requests Valve's own API list via their API.
        
        Munges a bit to make it slightly more human-friendly.
        """
        self.call('GetSupportedAPIList', interface='ISteamWebAPIUtil')
        self._result = self._raw['apilist']['interfaces']
        self.supported = []
        
        # scratch this for now because it overwrites when multiple versions
        # TODO: re-implement with support for version handling.
        for x in self._raw['apilist']['interfaces']:
            
            for m in x['methods']:
                c = Call(self._api_key, m['name'], x['name'], **m)
                self.supported.append(c)
                setattr(self, m['name'] + '_v' + str(m['version']), c)
    
    def get_app_list(self):
        calls = [x for x in self.supported if 'GetAppList' == x.method]
        if len(calls) == 0:
            raise RankineError("Found no supported methods for GetAppList")
        
        calls.sort(key=lambda x: x.version, reverse=True)
        self._call = calls[0]
        self._raw = self._call.get()
        self._result = self._raw['applist']['apps']
        return self._result

