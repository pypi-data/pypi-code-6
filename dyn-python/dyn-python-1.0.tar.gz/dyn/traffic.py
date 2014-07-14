from dyn.client import DynTrafficClient


class DynTraffic(object):
    def __init__(self, customername, username, password):
        self._client = DynTrafficClient()

        self._customername = customername
        self._username = username
        self._password = password

        self.session = Session(self, customername, username, password)
        self.record  = Record(self)
        self.zone    = Zone(self)
        self.http_redirect = HttpRedirect(self)
        self.gslb = Gslb(self)

    def with_zone(self, zone):
        self._zone = zone
        return self

class Session(object):
    def __init__(self, dyn, customername, username, password):
       self._dyn = dyn
       self._customername = customername
       self._username = username
       self._password = password

    def create(self):
        creds = {
            'customer_name': self._customername,
            'user_name': self._username,
            'password': self._password
        }
        return self._dyn._client.execute('/Session', 'POST', creds)

    def destroy(self):
        return self._dyn._client.execute('/Session', 'DELETE')

class Zone(object):
    def __init__(self, dyn):
        self._dyn = dyn

    def create(self, rname, ttl):
        return self._dyn._client.execute('/Zone/' + self._dyn._zone, 'POST', dict({'rname':rname, 'ttl':ttl}))

    def list(self):
        return self._dyn._client.execute('/Zone/' + self._dyn._zone, 'GET')

    def delete(self):
        return self._dyn._client.execute('/Zone/' + self._dyn._zone, 'DELETE')

    def update(self, rname, ttl):
        return self._dyn._client.execute('/Zone/' + self._dyn._zone, 'PUT', dict({'rname':rname, 'ttl':ttl}))

    def publish(self):
        return self._dyn._client.execute('/Zone/' + self._dyn._zone, 'PUT', {'publish':True})

    def freeze(self):
        return self._dyn._client.execute('/Zone/' + self._dyn._zone, 'POST', {'freeze':True})

    def thaw(self):
        return self._dyn._client.execute('/Zone/' + self._dyn._zone, 'POST', {'thaw':True})

class Record(object):
    def __init__(self, dyn):
        self._dyn = dyn

    def create(self, type, fqdn, rdata):
        return self._dyn._client.execute('/' + type + 'Record/' + self._dyn._zone + '/' + fqdn, 'POST', dict({'rdata':rdata}))

    def update(self, type, fqdn, rdata):
        return self._dyn._client.execute('/' + type + 'Record/' + self._dyn._zone + '/' + fqdn, 'PUT', dict({'rdata':rdata}))

    def replace(self, type, fqdn, rdata):
        return self._dyn._client.execute('/' + type + 'Record/' + self._dyn._zone + '/' + fqdn, 'PUT', dict({'rdata':rdata}))

    def list(self, fqdn=''):
        return self._dyn._client.execute('/AllRecord/' + self._dyn._zone + '/' + fqdn, 'GET')

    def delete(self, type, fqdn, id=''):
        return self._dyn._client.execute('/' + type + 'Record/' + self._dyn._zone + '/' + fqdn + '/' + id, 'DELETE')

class HttpRedirect(object):
    def __init__(self, dyn):
        self._dyn = dyn

    def create(self, fqdn, code, keep_uri, url):
        return self._dyn._client.execute('/HTTPRedirect/' + self._dyn._zone + '/' + fqdn, 'POST', {'code':code, 'keep_uri':keep_uri, 'url':url})

    def update(self, fqdn, code, keep_uri, url):
        return self._dyn._client.execute('/HTTPRedirect/' + self._dyn._zone + '/' + fqdn, 'PUT', {'code':code, 'keep_uri':keep_uri, 'url':url})

    def delete(self, fqdn):
        return self._dyn._client.execute('/HTTPRedirect/' + self._dyn._zone + '/' + fqdn, 'DELETE')

    def list(self, fqdn=''):
        return self._dyn._client.execute('/HTTPRedirect/' + self._dyn._zone + '/' + fqdn, 'GET')


class Gslb(object):
    def __init__(self, dyn):
        self._dyn = dyn

    def create(self, fqdn, region, monitor):
        return self._dyn._client.execute('/GSLB/' + self._dyn._zone + '/' + fqdn, 'POST', dict({'region':region, 'monitor':monitor}))

    def update(self, fqdn, region, monitor):
        return self._dyn._client.execute('/GSLB/' + self._dyn._zone + '/' + fqdn, 'PUT', dict({'region':region, 'monitor':monitor}))

    def activate(self, fqdn, activate):
        return self._dyn._client.execute('/GSLB/' + self._dyn._zone + '/' + fqdn, 'PUT', {'activate':True})

    def deactivate(self, fqdn, deactivate):
        return self._dyn._client.execute('/GSLB/' + self._dyn._zone + '/' + fqdn, 'PUT', {'deactivate':True})

    def recover(self, fqdn, recover):
        return self._dyn._client.execute('/GSLB/' + self._dyn._zone + '/' + fqdn, 'PUT', {'recover':True})

    def recoverip(self, fqdn, recoverip, address):
        return self._dyn._client.execute('/GSLB/' + self._dyn._zone + '/' + fqdn, 'PUT', {'recoverip':True, 'address':address})

    def list(self, fqdn=''):
        return self._dyn._client.execute('/GSLB/' + self._dyn._zone + '/' + fqdn, 'GET')

    def delete(self, fqdn):
        return self._dyn._client.execute('/GSLB/' + self._dyn._zone + '/' + fqdn, 'DELETE')

