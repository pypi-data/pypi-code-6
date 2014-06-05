# -*- coding: UTF-8 -*-
#
# manque scenario et panel securité
# manque devices -temp, batterie, humidité
# doit marcher et a tester on/off - switch et HC 
# param à faire ip et port
#
from lisa.server.plugins.IPlugin import IPlugin
from twisted.python import log
import gettext
import inspect
import os
import requests
import json



class Domoticz(IPlugin):
	def __init__(self):
		super(Domoticz, self).__init__()
		self.configuration_plugin = self.mongo.lisa.plugins.find_one({"name": "Domoticz"})
		self.path = os.path.realpath(os.path.abspath(os.path.join(os.path.split(
		inspect.getfile(inspect.currentframe()))[0],os.path.normpath("../lang/"))))
		self._ = translation = gettext.translation(domain='domoticz',
			localedir=self.path,
                        languages=[self.configuration_lisa['lang']]).ugettext
#
	
	def switchlight(self, jsonInput):
		bodies = ""
		if jsonInput['outcome']['entities']['location']['body'] :
			location = jsonInput['outcome']['entities']['location']['body']
		else:
			bodies = "pas de lieu"

		if jsonInput['outcome']['entities']['on_off']['value'] :
			on_off = jsonInput['outcome']['entities']['on_off']['value']
		else:
			bodies = "pas de on/off"
#
		idex= location + "_" + on_off
#		#log.msg("WAMP session data received (transport ID %s): %s" % (self._parent._transportid, payload))
		log.msg("index :  %s" % (idex))		
		for rs in self.configuration_plugin['param_dz']:
			log.msg("ids  :  %s" % (rs['ids']))
			if rs['ids'] == idex :
#				log.msg("index trouvé :  ***")
				bodies == rs['boy']
				resp = requests.get ('http://192.168.0.3:8080/json.htm?type=command&param=switchlight&idx=%02d&switchcmd=%s&level=0' % (rs['idx'],on_off.capitalize()))
				log.msg("resp  :  %s" % (resp))
		return {"plugin": "Domoticz",
			"method": "switchlight",
			"body": bodies
		}
