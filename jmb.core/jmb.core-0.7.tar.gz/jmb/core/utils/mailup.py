#! -*- coding: utf-8 -*-

#!/usr/bin/env python
import logging, urllib, urllib2, os
from xml.dom import minidom

from django.utils.translation import ugettext_lazy as _
from django.conf import settings

WS_MAILUP = 'http://ws.mailupnet.it/'


# QUesta classe serve per l'importazione di contatti in mailup attraverso il
# servizio soap ws_mailupimport
class ImportMailupNewsletter:

    def __init__(self, soap_url, auth_uid = None, auth_psw = None):
        self.url = soap_url
        self.user = auth_uid
        self.password = auth_psw
        self.client = self.connect()
    
    def connect(self):
        if settings.USE_MAILUP_WEBSERVICE:
            from suds.client import Client
            from suds.xsd.doctor import Import, ImportDoctor

            imp = Import('http://www.w3.org/2001/XMLSchema')
            imp.filter.add(WS_MAILUP)
            doctor = ImportDoctor(imp)

            client = Client(self.url, doctor=doctor)

            if self.user and self.password: 
                token = client.factory.create('Authentication')
                token.User = self.user
                token.Password = self.password
                client.set_options(soapheaders=token)
            return client
        else:
            raise Exception(_('MAILUP WS functionalitySetting USE_MAILUP_WEBSERVICE is set to FALSE'))

    def getLists(self):
        return
    
    def createList(self):
        return
    
    def getGroups(self):
        return
    
    def createGroups(self):
        return

    def createMultiSubscribers(self, list_id, list_guid, values_list, group="", forced=False):
        # values_list deve essere una lista di tuple, ogni tupla rappresenta un utente da iscrivere.
        # I campi della tupla sono i campi da registrare su mailup. Per sapere quali siano è necessario
        # fare riferimento alla console mailup.
        ## N.B. Il primo dei campi deve essere la mail dell'utente!!! Questo poichè non è possibile
        ## passare un dizionario come value_list in quanto quest'ultimo non ha ordinamento. Mailup memorizza
        ## invece i campi solo in base al loro ordine.
        xml_tot = ""
        for value in values_list:
            xml_header = """<subscriber email="%(email)s" Prefix="" Number="%(tel)s" Name="">""" % {
                            'email': value[0],
                            'tel': ""
                         }
            xml_body = ""
            for i, item in enumerate(value):
                if i != 0: #salto il primo perchè la mail l'ho già messa nell'header
                    xml_body += "<campo%(indice)s>%(value)s</campo%(indice)s>" % {
                        'indice': i-1,
                        'value': item,
                    }
    
            xml_footer = "</subscriber>"
            xml_tot += xml_header + xml_body + xml_footer 

        xml = "<subscribers>" + xml_tot + "</subscribers>"

        nl = self.client.service.StartImportProcesses(list_id, list_guid, xml, group, 3, 1, False, False, False, forced, False)

        xmldoc = minidom.parseString(nl)
        error_code = xmldoc.getElementsByTagName("ReturnCode")[1].firstChild.data
        return error_code

    def createSubscriber(self, list_id, list_guid, email, values, group="", phone_number="", forced=False):
        xml_header = """<subscribers><subscriber email="%(email)s" Prefix="" Number="%(tel)s" Name="">""" % {
                        'email': email,
                        'tel': phone_number
                     }
        xml_body = ""
        for i, item in enumerate(values):
            xml_body += "<campo%(indice)s>%(value)s</campo%(indice)s>" % {
                'indice': i,
                'value': item,
            }

        xml_footer = "</subscriber></subscribers>"

        xml = xml_header + xml_body + xml_footer

        nl = self.client.service.StartImportProcesses(list_id, list_guid, xml, group, 3, 1, False, False, False, forced, False)
        #nl = client.service.CreateGroup(1, "bb341a9c-310f-45e7-b5f7-e7ebd39e0c47", "GruppoProva2")

        xmldoc = minidom.parseString(nl)
        error_code = xmldoc.getElementsByTagName("ReturnCode")[1].firstChild.data
        return error_code
    
# QUesta classe serve per l'invio di newsletter attraverso il
# servizio soap ws_mailupsend
class SendMailupNewsletter:
    def __init__(self, soap_url):
        self.url = soap_url
        self.client = self.connect()

    def connect(self):
        if settings.USE_MAILUP_WEBSERVICE:
            from suds.client import Client
            from suds.xsd.doctor import Import, ImportDoctor

            imp = Import('http://www.w3.org/2001/XMLSchema')
            imp.filter.add(WS_MAILUP)
            doctor = ImportDoctor(imp)

            client = Client(self.url, doctor=doctor)

            return client
        else:
            raise Exception(_('MAILUP WS functionalitySetting USE_MAILUP_WEBSERVICE is set to FALSE'))

    def get_element_data(self, xml, element = 'errorCode'):
        xmldoc = minidom.parseString(xml)
        data = xmldoc.getElementsByTagName(element)[0].firstChild.data
        return data

    def login(self, user, psw, console_url = 'news.eroom.it'):
        nl = self.client.service.Login(user, psw, console_url)
        return self.get_element_data(nl, 'accessKey')

    def logout(self, accessKey):
        response = self.client.service.Logout(accessKey)
        return self.get_element_data(response)
    
    # Crea e invia una singola newsletter
    # il parametro options deve essere una lista di dizionari nel formato
    # {'Option': [{'Key':'chiave', 'Value':'valore'},{'Key':'chiave', 'Value':'valore'},]}
    def sendNewsletterFast(self, user, psw, listID, subject, type, content, options = '', console_url = 'news.eroom.it'):
        ak = self.login(user, psw, console_url)
        result = self.client.service.SendNewsletterFast(accessKey=ak,
                                                        listID=listID,
                                                        subject=subject,
                                                        type=type,
                                                        content=content,
                                                        options=options)
        error_code = self.get_element_data(result)
        self.logout(ak)
        return error_code

    # Invia una newsletter gia' presente sulla consele mailup
    # il parametro options deve essere una lista di dizionari nel formato
    # {'Option': [{'Key':'chiave', 'Value':'valore'},{'Key':'chiave', 'Value':'valore'},]}
    def sendNewsletter(self, user, psw, listID, newsletterID, options = '', console_url = 'news.eroom.it'):
        ak = self.login(user, psw, console_url)
        result = self.client.service.SendNewsletter(accessKey=ak,
                                                    listID=listID,
                                                    newsletterID=newsletterID,
                                                    options=options)
        error_code = self.get_element_data(result)
        error_description = self.get_element_data(result, 'errorDescription')
        self.logout(ak)
        return error_code

    # CREATO DA MARCO MINUTOLI PER EVITARE DI TOCCARE LA FUNZIONE VECCHIA; AGGIUNGE
    # LA FUNZIONALITA DI LETTURA DELLA DESCRIZIONE DELL'ERRORE TORNATO DA MAILUP
    # Invia una newsletter gia' presente sulla consele mailup
    # il parametro options deve essere una lista di dizionari nel formato
    # {'Option': [{'Key':'chiave', 'Value':'valore'},{'Key':'chiave', 'Value':'valore'},]}
    def sendNewsletterNew(self, user, psw, listID, newsletterID, options = '', console_url = 'news.eroom.it'):
        ak = self.login(user, psw, console_url)
        result = self.client.service.SendNewsletter(accessKey=ak,
                                                    listID=listID,
                                                    newsletterID=newsletterID,
                                                    options=options)
        error_code = self.get_element_data(result)
        error_description = self.get_element_data(result, 'errorDescription')
        self.logout(ak)
        return error_code, error_description

    # Invia una singola mail.
    # I metodi login e logout vanno chiamati a parte.
    # il parametro options deve essere una lista di dizionari nel formato
    # {'Option': [{'Key':'chiave', 'Value':'valore'},{'Key':'chiave', 'Value':'valore'},]}
    def sendSingleNewsletter(self, user, psw, listID, subject, type, content, recipientEmail, options = '', console_url = 'news.eroom.it'):
        ak = self.login(user, psw, console_url)
        result = self.client.service.SendSingleNewsletter(accessKey=ak,
                                                    listID=listID,
                                                    subject=subject,
                                                    type=type,
                                                    content=content,
                                                    recipientEmail=recipientEmail,
                                                    options=options)
        error_code = self.get_element_data(result)
        self.logout(ak)
        return error_code

# questa classe serve per effettuare chiamate verso mailup
class HttpMailupNewsletter:

    CONSOLE_URL= 'http://news.eroom.it/'

    def unsubscribeUser(self, list_id, list_guid, email):

        url = os.path.join(self.CONSOLE_URL, 'frontend/xmlUnSubscribe.aspx')
        values = {
                    'ListGuid' : list_guid,
                    'List' : list_id,
                    'Email' : email
                 }
        data = urllib.urlencode(values)

        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        return response.read()

    def updateUser(self, list_id, list_guid, email, csv_fld_names, csv_fld_values):

        url = os.path.join(self.CONSOLE_URL, 'frontend/xmlUpdSubscriber.aspx')
        values = {
                    'ListGuid' : list_guid,
                    'List' : list_id,
                    'Email' : email,
                    'csvFldNames': csv_fld_names,
                    'csvFldValues': csv_fld_values
                 }
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        return response.read()
