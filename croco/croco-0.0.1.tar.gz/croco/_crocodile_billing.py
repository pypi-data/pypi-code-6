# -*- coding:utf-8 -*-
"""
Simple Receipt Validator

@author Anderson (Chang Min)
@email a141890@gmail.com
"""
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from base64 import b64decode
import json


class CrocodileValidator(object):
    
    def __init__(self, public_key, market='google'):
        """
        @param market (str): Market ID
        @param public_key (str): In Google, The Public Key is provided in Google Console
            You can find it in Services & API -> Base64-encoded RSA public key
        """
        self._market = market
        self._public_key = public_key
    
    def validate(self, receipt, signature):
        """
        @todo For the timebeing, only google validation is provided. Validation for IOS will be updated soon.
        """
        return self._validate_google(receipt, signature)
            
    
    def _validate_google(self, receipt, signature):
        """
        @receipt (str) : the string json data received when the Android user purchase an item. 
        @signature (str) : base64 hash key
        """
        
        if type(receipt) == dict:
            receipt = json.dumps(receipt)
            
        key = RSA.importKey(self._pem_format(self._public_key))
        verifier = PKCS1_v1_5.new(key)
        data = SHA.new(receipt)
        sig = b64decode(signature)
        return bool(verifier.verify(data, sig))
    
    def _pem_format(self, key):
        """
        the method makes the key string into PEM File string
        """
        splited = [key[i:i + 64] for i in range(0, len(key), 64)]
        
        return '\n'.join([
            '-----BEGIN PUBLIC KEY-----',
            '\n'.join(splited),
            '-----END PUBLIC KEY-----',
        ])
        
    def __del__(self):
        del self._market
        del self._public_key
        



    
         
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    





