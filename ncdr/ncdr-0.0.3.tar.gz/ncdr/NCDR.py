#!/usr/bin/env python
# encoding: utf-8

"""
NCDR.py

Normalized Call Detail Record data model.


2012 StoneWork Solutions

@author Enrique Cervantes Mora <enrique.cervantes@stoneworksolutions.net>
"""
import hashlib, time

class NCDR:

	def __init__(self, data):

		self.content = {'backend_type':None, 	
					'sourceserver':None, 		
					'sourceserver_ip':None, 	
					'uniqueid':None,			
					'inbound_id':None, 			
					'outbound_id':None, 		
					'caller_nr':None, 			
					'called_nr':None, 			
					'start_calldate':None, 		
					'end_calldate':None, 		
					'answer_calldate':None,		
					'progress_time':None, 	
					'duration':None, 			
					'billsec':None, 			
					'billsec_msec':None,		
					'billsec_msec_provider':None,
					'billsec_provider':None,	
					'hangup_code_rcv':None,		
					'hangup_code':None,		 	
					'hangup_desc':None, 		
					'hangup_init':None, 		
					'inbound_codec':None,		
					'outbound_codec':None, 		
					'inbound_peer':None, 		
					'outbound_peer':None, 		
					'inbound_peer_ip':None, 	
					'outbound_peer_ip':None, 	
					'inbound_remote_rtp_ip':None,
					'resource_id':None,			
					'other_resource_id':None,	
					'last_app':None, 			
					'last_data':None, 			
					'remote_rtp_ip':None,		
					'ss_processtime':None, 		
					'ss_request':None, 			
					'ss_response':None, 		
					'userfield':None, 			
					'routing_tries':None,		
					'timezone':None,			
					'inbound_prefix':None,		
					'outbound_prefix':None,		
					'last_tried':None,			
					'callid':None,
					'redirect_callid':None,
					'carrier':None,
					}

		self.setContent(data)
		
	def setContent(self, data):
		for var in data:
			self.content[var]=data[var]

		if self.content['carrier'] is None:
			self.content['carrier'] = 'default'
			
		if self.content['outbound_id'] is None:
			self.content ['uniqueid'] = hashlib.sha1(str(self.content['start_calldate']) + str(self.content['inbound_id'])).hexdigest()
		else:
			self.content ['uniqueid'] = hashlib.sha1(str(self.content['start_calldate']) + str(self.content['inbound_id']) + str(self.content['outbound_id'])).hexdigest()

		if self.content['backend_type'].lower() == 'asterisk':
			self.content['callid'] = self.content['uniqueid']


		if self.content['timezone'] == None:
			if time.timezone < 0:
				strtime = 'GMT +'
			else:
				strtime = 'GMT '
			self.content ['timezone'] = strtime + str(time.timezone/-3600)

		if self.content['inbound_codec']:
			self.content ['inbound_codec'] = self.translateCodec(self.content['inbound_codec'])

		if self.content['outbound_codec']:
			self.content ['outbound_codec'] = self.translateCodec(self.content['outbound_codec'])


	def getContent (self):
		return self.content

	def toString (self):

		cadena = """
""" + '*' * 70 + """
'backend_type': """ + str(self.content['backend_type'])+ """
'sourceserver': """ + str(self.content['sourceserver'])+ """
'sourceserver_ip': """ + str(self.content['sourceserver_ip'])+ """
'uniqueid': """ + str(self.content['uniqueid'])+ """
'inbound_id': """ + str(self.content['inbound_id'])+ """
'outbound_id': """ + str(self.content['outbound_id'])+ """
'caller_nr': """ + str(self.content['caller_nr'])+  """
'called_nr': """ + str(self.content['called_nr'])+"""
'start_calldate': """ + str(self.content['start_calldate'])+ """
'end_calldate': """ + str(self.content['end_calldate'])+ """
'answer_calldate': """ + str(self.content['answer_calldate'])+ """
'progress_time': """ + str(self.content['progress_time'])+ """
'duration': """ + str(self.content['duration'])+ """
'billsec': """ + str(self.content['billsec'])+ """
'hangup_code': """ + str(self.content['hangup_code'])+ """
'hangup_desc': """ + str(self.content['hangup_desc'])+ """
'hangup_init': """ + str(self.content['hangup_init'])+ """
'inbound_codec': """ + str(self.content['inbound_codec'])+ """
'outbound_codec': """ + str(self.content['outbound_codec'])+ """
'inbound_peer': """ + str(self.content['inbound_peer'])+ """
'outbound_peer': """ + str(self.content['outbound_peer'])+ """
'inbound_peer_ip': """ + str(self.content['inbound_peer_ip'])+ """
'outbound_peer_ip': """ + str(self.content['outbound_peer_ip'])+ """
'last_app': """ + str(self.content['last_app'])+ """
'last_data': """ + str(self.content['last_data'])+ """
'remote_rtp_ip': """ + str(self.content['remote_rtp_ip'])+ """
'ss_processtime': """ + str(self.content['ss_processtime'])+ """
'ss_request': """ + str(self.content['ss_request'])+ """
'ss_response': """ + str(self.content['ss_response'])+ """ 
'userfield': """ + str(self.content['userfield'])+ """
'routing_tries': """ + str(self.content['routing_tries'])+ """
'timezone': """ + str(self.content['timezone'])+ """
'inbound_prefix': """ + str(self.content['inbound_prefix'])+ """
'outbound_prefix': """ + str(self.content['outbound_prefix'])+ """
""" + '*' * 70 + """
"""
		return cadena

	def translateCodec (self, codec):
		codecList = ['alaw','ulaw','g729','g726','g723','g722','gsm','iLBC','speex']

		if codec == '0':
			return codecList[0]
		elif codec == '1':
			return codecList[1]
		elif codec == '2':
			return codecList[2]
		elif codec == '3':
			return codecList[3]
		elif codec == '4':
			return codecList[4]
		elif codec == '5':
			return codecList[5]
		elif codec == '6':
			return codecList[6]
		elif codec == '7':
			return codecList[7]
		elif codec == '8':
			return codecList[8]
		else:
			return codec
