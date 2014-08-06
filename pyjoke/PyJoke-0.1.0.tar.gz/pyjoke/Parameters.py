#!/usr/bin/python
# -*- coding: utf-8 -*-

# PARAMETERS
import yaml

class Parameters:
    def __init__(self):
        stream = open("/home/laurent/Documents/PyJoke/parameters.yml", "r")
        docs = yaml.load_all(stream)
        for doc in docs:
            self.database = doc["database"]["use"]
            self.host = doc["database"]["host"]
            self.user = doc["database"]["user"]
            self.passwd = doc["database"]["passwd"]
            self.db = doc["database"]["db"]
            self.table = doc["database"]["table"]
            self.sqlite = doc["database"]["sqlite"]

            self.lang = doc["pyjoke"]["lang"]
            self.jokelen = doc["pyjoke"]["jokelen"]
            self.debug = doc["pyjoke"]["debug"]
            self.nao = doc["pyjoke"]["nao"]

            self.postag = doc["postag"]["active"]
            self.default = doc["postag"]["default"]
            self.adj = doc["postag"]["adj"]
            self.noun = doc["postag"]["noun"]
            self.verb = doc["postag"]["verb"]
            self.brute = doc["postag"]["brute"]

            self.conv = doc["conversation"]["level"]

            if self.debug:
                for k,v in doc.items():
                    print k, "->", v
                print "\n",
