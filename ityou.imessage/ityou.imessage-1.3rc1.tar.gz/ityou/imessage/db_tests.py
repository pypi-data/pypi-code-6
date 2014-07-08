# -*- coding: utf-8 -*-
from datetime import datetime, timedelta 
import logging

from dbapi import DBApi


class DBTest():
    """Tests for the DB
    """
    
    def __init__(self):    
        self.db = DBApi()
        self.tdelta = datetime.now() - timedelta(seconds = 3600)

        self.md5 = self.test_addMessage()['md5']
        self.test_getMessage(self.md5)['md5']
        self.test_getMessages(timestamp=self.tdelta)
        self.test_updateMessage(self.md5, u'Das ist ein Update! ÖÄÜ')
        
        self.test_getDialog(u'lmuller', u'ppan')

    def test_addMessage(self):        
        message1 = {
            'sender_id':        u'lmuller',
            'sender_name':      u'Luc Müller',
            'sender_email':     u'lmuller@ityou.de',
            'receiver_id':      u'ppan',
            'receiver_name':    u'Petra Pan',
            'receiver_email':   u'support@ityou.de',
            'message':          u'Das ist der Kern der Mitteilung:ÖÄÜß',
            'approved':         False
        }
        message2 = {
            'sender_id':        u'ppan',
            'sender_name':      u'Peter Pan',
            'sender_email':     u'support@ityou.de',
            'receiver_id':      u'lmuller',
            'receiver_name':    u'Luc Müller',
            'receiver_email':   u'lmuller@ityou.de',
            'message':          u'Das ist eine Mitteilung von pp an lm',
            'approved':         False
        }
        message3 = {
            'sender_id':        u'hmustermann',
            'sender_name':      u'Hans Mustermann',
            'sender_email':     u'support@ityou.de',
            'receiver_id':      u'lmuller',
            'receiver_name':    u'Luc Müller',
            'receiver_email':   u'lmuller@ityou.de',
            'message':          u'Das ist eine Mitteilung von pp an lm',
            'approved':         False
        }
        message3 = {
            'sender_id':        u'hmustermann',
            'sender_name':      u'Hans Mustermann',
            'sender_email':     u'support@ityou.de',
            'receiver_id':      u'ppan',
            'receiver_name':    u'Petra Pan',
            'receiver_email':   u'info@ityou.de',
            'message':          u'Das ist eine Mitteilung von hh an pp',
            'approved':         False
        }

        db_message = self.db.addMessage(message3)
        
        logging.info("\n\nADD MESSAGE:\n\t\t %s\n" % str(db_message))
        return db_message
        
        
    def test_getMessage(self, md5):
        db_message = self.db.getMessage(md5=md5)
        logging.info("\n\n GET MESSAGE: \n\t\t %s \n" % str( db_message ))
        return db_message
        

    def test_getMessages(self, timestamp):
        db_messages =  [ str(m) for m in self.db.getMessages(timestamp=timestamp) ]  
        logging.info("\n\n GET MESSAGES: \n\t\t %s \n" % str(  db_messages   ))
        return db_messages
        
    def test_updateMessage(self, md5, message):
        db_message = self.db.updateMessage(md5, message)
        logging.info("\n\n UPDATE MESSAGE: \n\t\t: %s \n" %  db_message)
        return db_message

    def test_getDialog(self, sender_id, receiver_id):
        db_messages = self.db.getDialog(sender_id=sender_id, receiver_id=receiver_id)
        logging.info(str("\n\n DIALOG \n\t\t: %s\n" %  db_messages  ))
        return db_messages
