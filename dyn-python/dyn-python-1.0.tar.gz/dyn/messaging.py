from dyn.client import DynMessagingClient

class DynMessaging(object):
    def __init__(self, apikey):
        self._client         = DynMessagingClient()
        self._client._apikey = apikey
        self.senders      = Senders(self)
        self.accounts     = Accounts(self)
        self.recipients   = Recipients(self)
        self.suppressions = Suppressions(self)
        self.send_mail    = SendMail(self)
        self.delivery     = Report(self, 'delivered')
        self.sent_mail    = Report(self, 'sent')
        self.bounces      = Report(self, 'bounces')
        self.complaints   = Report(self, 'complaints')
        self.issues       = Report(self, 'issues')
        self.opens        = Report(self, 'opens', True)
        self.clicks       = Report(self, 'clicks', True)

class Senders(object):
    def __init__(self, dyn):
       self._dyn = dyn

    def list(self, startindex=0):
        return self._dyn._client.execute('/senders', 'GET', dict({'startindex':startindex}))

    def details(self, email):
        return self._dyn._client.execute('/senders/details', 'GET', dict({'emailaddress':email}))

    def status(self, email):
        return self._dyn._client.execute('/senders/status', 'GET', dict({'emailaddress':email}))

    def create(self, email, seeding='0'):
        return self._dyn._client.execute('/senders', 'POST', dict({'emailaddress':email,'seeding':seeding}) )

    def update(self, email, seeding='0'):
        return self._dyn._client.execute('/senders', 'POST', dict({'emailaddress':email,'seeding':seeding}) )

    def dkim(self, email, dkim):
        return self._dyn._client.execute('/dkim', 'POST', dict({'emailaddress':email,'dkim':dkim}) )

    def destroy(self, email):
        return self._dyn._client.execute('/senders/delete', 'POST', dict({'emailaddress':email}) )

class Accounts(object):
    def __init__(self, dyn):
       self._dyn = dyn

    def list(self, startindex=0):
        return self._dyn._client.execute('/accounts', 'GET', dict({'startindex':startindex}))

    def list_xheaders(self):
        return self._dyn._client.execute('/accounts/xheaders', 'GET', {})

    def create(self, username, password, companyname, phone, address, city, state, zipcode, country, timezone, bounceurl, spamurl, unsubscribeurl, trackopens, tracelinks, trackunsubscribes, generatenewapikey):
        return self._dyn._client.execute('/accounts', 'POST', DictIgnoresNone({'username':username,'password':password,'companyname':companyname,
            'phone':phone,'address':phone,'city':city,'state':state,'zipcode':zipcode,'country':country,'timezone':timezone,
            'bounceurl':bounceurl,'spamurl':spamurl,'unsubscribeurl':unsubscribeurl,'trackopens':trackopens,'tracelinks':tracelinks,'trackunsubscribes':trackunsubscribes,'generatenewapikey':generatenewapikey}))

    def update(self, username, password, companyname, phone, address, city, state, zipcode, country, timezone, bounceurl, spamurl, unsubscribeurl, trackopens, tracelinks, trackunsubscribes, generatenewapikey):
        return self._dyn._client.execute('/accounts', 'POST', DictIgnoresNone({'username':username,'password':password,'companyname':companyname,
			'phone':phone,'address':phone,'city':city,'state':state,'zipcode':zipcode,'country':country,'timezone':timezone,
			'bounceurl':bounceurl,'spamurl':spamurl,'unsubscribeurl':unsubscribeurl,'trackopens':trackopens,'tracelinks':tracelinks,'trackunsubscribes':trackunsubscribes,'generatenewapikey':generatenewapikey}))

    def update_xheaders(self, xheader1, xheader2, xheader3, xheader4):
        return self._dyn._client.execute('/accounts/xheaders', 'POST', dict({'xheader1':xheader1,'xheader2':xheader2,'xheader3':xheader3,'xheader4':xheader4}))

    def destroy(self, username):
        return self._dyn._client.execute('/accounts/delete', 'POST', dict({'username':username}) )

class Recipients(object):
    def __init__(self, dyn):
       self._dyn = dyn

    def status(self, email):
        return self._dyn._client.execute('/recipients/status', 'GET', dict({'emailaddress':email}))

    def activate(self, email):
        return self._dyn._client.execute('/recipients/activate', 'POST', dict({'emailaddress':email}) )

class Suppressions(object):
    def __init__(self, dyn):
       self._dyn = dyn

    def list(self, startindex=0, startdate=None, enddate=None):
        return self._dyn._client.execute('/suppressions', 'GET', DictIgnoresNone({'startindex':startindex,'startdate':startdate,'enddate':enddate}))

    def count(self, startindex=0, startdate=None, enddate=None):
        return self._dyn._client.execute('/suppressions/count', 'GET', DictIgnoresNone({'startindex':startindex,'startdate':startdate,'enddate':enddate}))

    def create(self, email):
        return self._dyn._client.execute('/suppressions', 'POST', dict({'emailaddress':email}) )

    def activate(self, email):
        return self._dyn._client.execute('/suppressions/activate', 'POST', dict({'emailaddress':email}) )

class SendMail(object):
    def __init__(self, dyn):
       self._dyn = dyn

    def send(self, from_addr, to_addr, subject, bodytext, bodyhtml, cc, replyto, xheaders):
        return self._dyn._client.execute('/send', 'POST', DictIgnoresNone({'from':from_addr, 'to':to_addr, 'subject':subject, 'bodytext':bodytext, 'bodyhtml':bodyhtml, 'cc':cc, 'replyto':replyto, 'xheaders':xheaders}))

class Report(object):
    def __init__(self, dyn, the_type, has_unique=False):
       self._dyn  = dyn
       self._type = the_type
       self._has_unique = has_unique

    def list(self, starttime, endtime, startindex=0, sender=None, xheaders=None):
        return self._dyn._client.execute('/reports/' + self._type, 'GET', DictIgnoresNone({'startindex':startindex,'starttime':starttime,'endtime':endtime,'sender':sender,'xheaders':xheaders}))

    def count(self, starttime, endtime, startindex=0, sender=None, xheaders=None):
        return self._dyn._client.execute('/reports/' + self._type + '/count', 'GET', DictIgnoresNone({'startindex':startindex,'starttime':starttime,'endtime':endtime,'sender':sender,'xheaders':xheaders}))

    def unique(self, starttime, endtime, startindex=0, sender=None, xheaders=None):
        if not self._has_unique:
            raise ValueError("unique endpoints not supported for: " + self._type)
        return self._dyn._client.execute('/reports/' + self._type + '/unique', 'GET', DictIgnoresNone({'startindex':startindex,'starttime':starttime,'endtime':endtime,'sender':sender,'xheaders':xheaders}))

    def unique_count(self, starttime, endtime, startindex=0, sender=None, xheaders=None):
        if not self._has_unique:
            raise ValueError("unique endpoints not supported for: " + self._type)
        return self._dyn._client.execute('/reports/' + self._type + '/count/unique', 'GET', DictIgnoresNone({'startindex':startindex,'starttime':starttime,'endtime':endtime,'sender':sender,'xheaders':xheaders}))

class DictIgnoresNone(dict):
	def __init__(self, iterable):
		for k, v in iterable.iteritems():
			if v is not None:
				self[k] = v

	def __setitem__(self, key, value):
		if key in self or value is not None:
			dict.__setitem__(self, key, value)
