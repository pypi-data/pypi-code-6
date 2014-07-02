import json
import requests
import urlparse

class RankineError(Exception):
    pass


class App(object):
    def __init__(self, appid, **kwargs):
        self.appid = appid
        [setattr(self, k, v) for k, v in kwargs.iteritems()]


class User(object):
    def __init__(self, steamid, **kwargs):
        self.steamid = steamid
        [setattr(self, k, v) for k, v in kwargs.iteritems()]
    
    def __repr__(self):
        return '<User: steamid={id}>'.format(id=self.steamid)


class Call(object):
    _base_web_url = 'http://api.steampowered.com/'
    # Steamworks Web API
    # http://api.steampowered.com/<interface>/<method>/<method_version>/
    
    # so-called "Big Picture" api
    _base_store_url = 'http://store.steampowered.com/api/'
    _url = None # overwritten with most recent
    
    
    def __init__(self, api_key, method, interface=None,
                 response_format='json', api='web', version=1,
                 parameters=[], **kwargs):
        self._api_key = api_key
        self.method = method
        
        self.interface = interface
        self._response_format = response_format
        self.api = api
        self.version = version
        
        if len(parameters) > 0:
            self.parameters = [CallParameter(**p) for p in parameters if str(CallParameter(**p).name) != 'key']
        else:
            self.parameters = []

        # dynamic docstring construction for mgr.method_name() access
        self.__doc__ = ''
        if self.interface is not None:
            self.__doc__ += '{i}.'.format(i=self.interface)
        self.__doc__ += '{m} version {v}\n(via {a} API)\n\n'.format(
            m=self.method,
            v=self.version,
            a=self.api)
        
        if len(self.parameters) > 0:
            self.__doc__ += 'Pass parameters below as keyword arguments when calling this method.'
            self.__doc__ += '\nFor example, {m}({kw}=your_value)\n====================' \
                .format(kw=self.parameters[0].name, m=self.method)
            for p in self.parameters:
                self.__doc__ += '\n{n}: {t} '.format(n=p.name, t=p.type)
                if p.optional:
                    self.__doc__ += '(optional)'
                else:
                    self.__doc__ += '(required)'
                
                self.__doc__ += '\n{d}\n'.format(d=p.description)
        else:
            self.__doc__ += 'Takes no parameters (keyword arguments)'
    
    
    def __call__(self, **kwargs):
        return self.get(**kwargs)
    
    
    def get(self, **kwargs):
        if self.api == 'web':
            url = urlparse.urljoin(
                self._base_web_url,
                '/'.join([self.interface, self.method, 'v%04i' % self.version])
            )
            url += '/?'
        
        elif self.api == 'store':
            # used pretty much exclusively for GetAppDetails
            url = urlparse.urljoin(
                self._base_store_url,
                self.method
            )
            url += '/?v=%i&' % self.version
        else:
            raise RankineError("Call object kwarg api must be either 'web' or 'store' (got %s)" % self.api)
        
        url += 'format={rf}&key={k}' \
            .format(rf=self._response_format, k=self._api_key)
        
        # we have much of the url built
        # move on to appending any further parameters supplied
        if len(kwargs) > 0:
            # there are additional keyword arguments, which
            # should pretty much be parameters to pass along at
            # this point
            
            if 'Service' in self.interface:
                # param formatting is different for "service" APIs
                # e.g. IPlayerService
                # Service APIs accept parameters in a JSON blob
                # which may need to be url encoded--testing pending
                param_str = 'input_json=%s' % json.dumps(kwargs)
            
            else:
                # these are standard foo=bar&parrot=dead URL params
                param_str = '&'.join('{k}={v}'.format(k=k, v=v) for k, v in kwargs.iteritems())
            
            url += '&%s' % param_str
        
        self._url = url
        request = requests.get(self._url)
        if request.status_code is 200:
            return request.json()
        else:
            return False
    
    
    def __repr__(self):
        if self.api == 'web':
            # distinct interface
            s = '<Web API Call: {i}.{m} v{v}>' \
                .format(i=self.interface, m=self.method, v=str(self.version))
        else:
            # implied interface
            s = '<Big Picture API Call: {m} v{v}>' \
                .format(m=self.method, v=str(self.version))
        return s


class CallParameter(object):
    def __init__(self, name, optional=True, type=None, description=None):
        self.name = name
        self.optional = optional
        self.type = type
        self.description = description

        if self.description is None:
            self.description = "No description provided by API"
    
    def __repr__(self):
        s = '<CallParameter: {n}, optional={o}, type={d}>' \
            .format(n=self.name, o=self.optional, d=self.type)
        return s
