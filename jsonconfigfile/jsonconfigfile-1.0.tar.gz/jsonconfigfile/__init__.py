'''
Created on May 9, 2014

@author: lwoydziak
'''
import os
import json
from singleton3 import Singleton
    
## Singleton
class Env(object, metaclass=Singleton):
    def __init__(self, initialJson=None, configFileName=None, envConfigFileNameOverride=None):
        self.__json = json.loads(initialJson)
        self.__configFileName = configFileName
        self.__envConfigFileNameOverride = envConfigFileNameOverride
        
        self.load()
        
    def envConfigFileNameOverride(self, envConfigFileNameOverride):
        self.__envConfigFileNameOverride = envConfigFileNameOverride
        
    def load(self):
        if self.__envConfigFileNameOverride in str(os.environ):
            self.__configFileName = os.environ.get(self.__envConfigFileNameOverride)
        
        try:
            configFile = open(self.__configFileName, "r")
        except Exception as e:
            print(str(e))
            pass
        
        try:
            self.__json = json.load(configFile)
        except Exception as e:
            print(str(e))
            return

    def get(self, firstLevel, secondLevel=None):
        try:
            if secondLevel is None:
                return self.__json[firstLevel]
            else:
                return self.__json[firstLevel][secondLevel]
        except KeyError:
            return ""