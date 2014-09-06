from glim.component import Controller
from glim.facades import View

import json

class BaseController(Controller):
	def hello(self):

		return View.render('hello')

		return json.dumps({
			'error' : None,
			'msg' : 'Welcome to glim!'
		})
