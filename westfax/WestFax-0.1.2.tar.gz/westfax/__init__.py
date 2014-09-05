import requests
from hashlib import md5
# Sends fax through WestFax as a backup plan

class MissingFaxContent(Exception):
	pass

class NoRecipients(Exception):
	pass

class FaxFail(Exception):
	pass

class WestFax():

	def __init__(self, user, passwd, product):
		self.wf_user = user
		self.wf_pass = passwd
		self.wf_product = product
		self.numbers = []
	
	def add_number(self, number):
		self.numbers.append(number)

	def set_billing_code(self,code):
		self.billing_code = code

	def set_job_name(self,name):
		self.jobname = name

	def set_header(self,header):
		self.header = header

	def set_content(self,content):
		self.content = content

	def send(self):

		postdata = {
			'ProductId':	self.wf_product,
			'Username':		self.wf_user,
			'Password':		self.wf_pass,
			'BillingCode':	self.billing_code,
			'JobName':		self.jobname,
			'Header':		self.header
		}

		if len(self.numbers) < 1:
			raise NoRecipients("WestFax: No fax recipients found.")

		count = 1
		for n in self.numbers:
			postdata['Numbers' + str(count)] = n
			count += 1


		if not self.content:
			raise MissingFaxContent('No message specified')


		files = {'Files1': ( md5(self.content).hexdigest() + '.html', self.content ) }

		resp = requests.post( 'https://api.westfax.com/Polka.Api/REST/SendFax/JSON', data=postdata, files=files )

		if resp.status_code == 200:
			info = resp.json()
			
			if info.get('Success'):
				return info.get('Result')

			else:
				raise FaxFail(info.get('ErrorString'))
		
		else:
			raise FaxFail( "WestFax API failed with HTTP: " + str(resp.status) + " " + resp.reason )
