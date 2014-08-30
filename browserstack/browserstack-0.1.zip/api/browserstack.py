import sys, json
from api.rest import REST

ENDPOINT = "http://api.browserstack.com/3"


class Browser():
	os = ""
	os_version = ""
	browser = ""
	b_version = ""
	device = ""

	def __init__(self, os, os_version, browser, b_version, device = None):
		self.os = os
		self.os_version = os_version
		self.browser = browser
		self.b_version = b_version
		self.device = device


class Worker():
	id = ""
	url = ""
	name = ""
	timeout = 300
	build = ""
	project = ""
	browser = None
	rest = None

	def __init__(self, rest, browser = None, url = None, name = "", timeout = 0, build = "", project = "", worker_id = None):
		self.rest = rest
		self.browser = browser
		self.url = url
		self.name = name
		self.timeout = timeout
		self.build = build
		self.project = project
		self.id = worker_id

		if not self.id:
			data = {
				'os': self.browser.os,
				'os_version': self.browser.os_version,
				'browser': self.browser.browser,
				'browser_version': self.browser.b_version,
				'url': self.url,
			}

			if self.browser.device:
				data['device'] = self.browser.device
			if self.name:
				data['name'] = self.name
			if self.timeout:
				data['timeout'] = self.timeout
			if self.build:
				data['build'] = self.build
			if self.project:
				data['project'] = self.project

			worker = json.loads(self.rest.create('/worker', data = data))
			self.id = worker['id']

	def __str__(self):
		return "Worker: " + str(self.id) + ": " + self.name

	def status(self):
		return self.rest.query('/worker/' + str(self.id))

	def screenshot(format = 'png'):
		pass

	def terminate(self):
		return self.rest.delete('/worker/' + str(self.id))


class API():
	used_time = 0
	total_available_time = 0
	running_sessions = 0
	sessions_limit = 0
	browsers = {}

	rest = None

	def __init__(self, username, access_key):
		self.rest = REST(ENDPOINT, username, access_key)

	def __str__(self):
		return "\nAPI Status" + "\n\t" + "Used Time: " + str(self.used_time) + "\n\t" + "Total Available Time: " + str(self.total_available_time) + "\n\t" + "Running Sessions: " + str(self.running_sessions) + "\n\t" + "Sessions Limit: " + str(self.sessions_limit) + "\n"

	def status(self):
		status = json.loads(self.rest.query('/status'))
		self.used_time = status['used_time']
		self.total_available_time = status['total_available_time']
		self.running_sessions = status['running_sessions']
		self.sessions_limit = status['sessions_limit']
		return self

	def spawn(self, browser, url, name = "", timeout = 0, build = "", project = ""):
		return Worker(self.rest, browser, url, name, timeout, build, project)

	def reload(self, worker_id):
		return Worker(self.rest, worker_id = worker_id)

	# todo
	def browsers(self):
		return json.loads(self.rest.query('/browsers'))

	# todo
	def workers(self):
		return json.loads(self.rest.query('/workers'))


