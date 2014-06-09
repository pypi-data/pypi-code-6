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
		log.msg("index :  %s" % (idex))		
		for rs in self.configuration_plugin['param_dz']:
			log.msg("ids  :  %s" % (rs['ids']))
			if rs['ids'] == idex :
#				log.msg("index trouvé :  ***")
				bodies = rs['boy']
				log.msg("BODIES  :  %s" % (bodies))
				log.msg("on off  :  %s" % (on_off))
				log.msg("number  :  %s" % (int(rs['idx'])))
				resp = requests.get ('http://192.168.0.3:8080/json.htm?type=command&param=switchlight&idx=%s&switchcmd=%s&level=0' % (rs['idx'],on_off.capitalize()))
#				log.msg("resp  :  %s" % (req))				
#				resp = requests.get (req)
				log.msg("resp  :  %s" % (resp))
		if bodies == "":
			bodies = "j'ai rien compris aux switch"
		return {"plugin": "Domoticz",
			"method": "switchlight",
			"body": bodies
		}


	def devices(self, jsonInput):
		bodies = ""
		if jsonInput['outcome']['entities']['location']['body'] :
			location = jsonInput['outcome']['entities']['location']['body']
		else:
			bodies = "pas de lieu"

		if jsonInput['outcome']['entities']['local_search_query']['value'] :
			local = jsonInput['outcome']['entities']['local_search_query']['value']
		else:
			bodies = "pas de local_search_query"
#
		idex= local + " " + location +  "_"
		log.msg("index :  %s" % (idex))		
		log.msg("self.configuration_plugin['param_dz']:  %s" % (self.configuration_plugin['param_dz']))		
		for rs in self.configuration_plugin['param_dz']:
			log.msg("ids  :  %s" % (rs['ids']))
			if rs['ids'] == idex :
#				log.msg("index trouvé :  ***")
				bodies = rs['boy']
				log.msg("BODIES  :  %s" % (bodies))
				log.msg("local  :  %s" % (local))
				log.msg("number  :  %s" % (int(rs['idx'])))
#periph action
##http://192.168.0.1:8080/json.htm?type=command&param=switchlight&idx=39&switchcmd=On&level=0
#Panel security
##http://192.168.0.1:8080/json.htm?type=command&param=setsecstatus&secstatus=0&seccode=1234
#Sensor action
##http://192.168.0.1:8080/json.htm?type=devices&filter=temp&used=true&order=Name
###température 	/ consommation / état batterie / Humidity 
#0scenario action 
##http://192.168.0.1:8080/json.htm?type=command&param=switchscene&idx=1&switchcmd=On
#				
		#		resp = requests.get ('http://192.168.0.3:8080/json.htm?type=command&param=switchlight&idx=%s&switchcmd=%s&level=0' % (rs['idx'],on_off.capitalize()))
				resp = requests.get ('http://192.168.0.3:8080/json.htm?type=devices&filter=temp&used=true&order=Name')
				jsonreq = resp.json()
#				log.msg("resp  :  %s" % (req))				
				log.msg("resp  :  %s" % (resp))
				log.msg("response   :  %s" % (jsonreq))
				log.msg("*********************************************  : ")
				log.msg("jsonreq.result :  %s" % (jsonreq['result']))
				total = len (jsonreq['result'])
				log.msg(" total    :  %s" % (total))
				total = range(total)
				log.msg(" total - range    :  %s" % (total))
				for xx in jsonreq['result'] :
					log.msg(" jsonreq - idx   :  %s" % (xx['idx']))
					log.msg("   jsonreq - type   :  %s" % (xx['Type']))
		if bodies == "":
			bodies = "j'ai rien compris aux devices"
		return {"plugin": "Domoticz",
			"method": "switchlight",
			"body": bodies
		}
