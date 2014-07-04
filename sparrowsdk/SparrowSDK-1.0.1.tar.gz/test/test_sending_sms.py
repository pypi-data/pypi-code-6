'''
Created on May 26, 2014

@author: bijay
'''
import unittest
from sparrow import SparrowClient

class Test(unittest.TestCase):

    def setUp(self,):
        self.client_id = 'bijay'
        self.username = 'bijay'
        self.password = 'bijay'
        self.url = None
        
        self.ERROR_NO_USERNAME='Error 1.1: 403 - Username'
        self.ERROR_NO_CLIENT_ID='Error 1: 403 - You must be someone'  
        self.ERROR_UNAUTHORIZED='Error 2: 403'
        
        #sendsms parameters
        self.FROM='9848422934'
        self.TO='9848422934'
        self.TEXT="Hello testing"

    def tearDown(self):
        print "Success"
    
    def test_outgoing_with_username_only(self):
        out = SparrowClient(client_id = "",username = self.username,password= "")
        resp = out.sendsms( to=self.TO, message=self.TEXT,sender =self.FROM)
        self.assertIn(self.ERROR_NO_CLIENT_ID, resp)
    
    def test_outgoing_with_client_id_only(self):
        out = SparrowClient(client_id=self.client_id,username="",password="")
        resp = out.sendsms(sender = self.FROM, to = self.TO, message = self.TEXT)
        self.assertIn(self.ERROR_NO_USERNAME, resp)
    
    def test_outgoing_with_password_only(self):
        out = SparrowClient(client_id="",username="",password = self.password,)
        resp = out.sendsms(sender = self.FROM, to = self.TO, message = self.TEXT)
        self.assertIn(self.ERROR_NO_USERNAME, resp)
    
    def test_outgoing_without_client_id(self):
        out = SparrowClient(client_id='',username=self.username,password=self.password,) 
        resp = out.sendsms(sender = self.FROM, to = self.TO, message = self.TEXT)
        self.assertIn(self.ERROR_NO_CLIENT_ID,resp)
    
    def test_outgoing_without_password(self):
        out = SparrowClient(client_id=self.client_id,username=self.username,password='') 
        resp = out.sendsms(sender = self.FROM, to = self.TO, message = self.TEXT)
        self.assertIn(self.ERROR_UNAUTHORIZED,resp)
    
    def test_outgoing_without_username(self):
        out = SparrowClient(client_id=self.client_id,username='',password=self.password) 
        resp = out.sendsms(sender = self.FROM, to = self.TO, message = self.TEXT)
        self.assertIn(self.ERROR_NO_USERNAME,resp)
    
    def test_sendsms_without_from(self):
        out = SparrowClient(client_id=self.client_id,username=self.username,password=self.password) 
        resp = out.sendsms(sender = '', to = self.TO,message = self.TEXT)
        print resp
    
    def test_sendsms_without_to(self):
        out = SparrowClient(client_id=self.client_id,username=self.username,password=self.password) 
        resp = out.sendsms(sender = self.FROM,to = '',message = self.TEXT)
        print resp
    
    
    def test_sendsms_without_message(self):
        out = SparrowClient(client_id=self.client_id,username=self.username,password=self.password) 
        resp = out.sendsms(sender = self.FROM,to = self.TO,message =  '')
        print resp

    
    def test_sendsms_(self):
        out = SparrowClient(client_id=self.client_id,username=self.username,password=self.password) 
        resp = out.sendsms(sender = self.FROM, to = self.TO, message = self.TEXT)
        print resp

if __name__ == "__main__":
    unittest.main()
