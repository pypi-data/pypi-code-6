#!/usr/bin/python
# -*- coding: utf-8 -*-

# PARAMETERS
import yaml
import subprocess

class Parameters:
    def __init__(self):
        import os
        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        rel_path = "parameters.yml"
        abs_file_path = os.path.join(script_dir, rel_path)

        stream = open(abs_file_path, "r")
        docs = yaml.load_all(stream)
        for doc in docs:
            self.database = doc["database"]["use"]
            self.host = doc["database"]["host"]
            self.user = doc["database"]["user"]
            self.passwd = doc["database"]["passwd"]
            self.db = doc["database"]["db"]
            self.table = doc["database"]["table"]

            script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
            rel_path = doc["database"]["sqlite"]
            self.sqlite = os.path.join(script_dir, rel_path)

            self.lang = doc["pyjoke"]["lang"]
            self.jokelen = doc["pyjoke"]["jokelen"]
            self.debug = doc["pyjoke"]["debug"]
            self.nao = doc["pyjoke"]["nao"]

            self.postag = doc["postag"]["active"]

            try:
                subprocess.call(["tree-tagger"])
            except OSError as e:
                if e.errno == os.errno.ENOENT:
                    # handle file not found error.
                    print "[!] PyJoke parameters error: tree-tagger not found"
                    print "[!] PosTag deactivated"
                    self.postag = 0
                else:
                    #nope
                    raise

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
