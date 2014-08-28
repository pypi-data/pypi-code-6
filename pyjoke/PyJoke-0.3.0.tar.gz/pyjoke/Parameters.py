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

        self.paramfile = abs_file_path

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
            self.treetagger=doc["postag"]["folder"]

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

    def change(self):
        print "Editing params file ("+self.paramfile+")"

        # Absolute path of parameters file
        fname = self.paramfile

        # Load it in the script
        with open(fname) as f:
            newdct = yaml.load(f)

        # For each entry, ask if change
        for entry in newdct:
            print "Editing: " + entry
            for sub in newdct[entry]:
                print "[?] "+sub+" ("+str(newdct[entry][sub])+")"
                var = raw_input(">>> ")
                # If user doesn't enter anything, previous value it is
                if (var!=""):
                    newdct[entry][sub] = var

        # rewrite the file
        with open(fname, "w") as f:
            yaml.dump(newdct, f,default_flow_style=False)

        # Reload parameter file
        self.__init__()
