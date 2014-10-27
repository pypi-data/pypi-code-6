#!/usr/bin/python

import unittest
import subprocess
from time import sleep
import urllib2
import json
import os

nlgserv = None

def setUpModule():
    global nlgserv
    print "Starting up nlgserv..."
    nlgserv = subprocess.Popen([os.path.join(os.path.dirname(__file__),"../jython.jar"), os.path.join(os.path.dirname(__file__), "../_server.py"), "localhost", "8080"],
                               stdin=subprocess.PIPE,
                               stdout=open(os.path.join(os.path.dirname(__file__), "nlgserv.stdout.log"), "w+"),
                               stderr=open(os.path.join(os.path.dirname(__file__), "nlgserv.stderr.log"), "w+"),
                               preexec_fn=os.setsid)
    sleep(60) # It needs longer now it's loading from the standalone package...
    print "Commencing testing..."
    
def tearDownModule():
    global nlgserv
    print "Shutting down nlgserv..."
    os.killpg(nlgserv.pid, subprocess.signal.SIGTERM)
    nlgserv.wait()
    

def send_data(json_data):
    req = urllib2.Request("http://localhost:8080/generateSentence",
                          data=json_data,
                          headers={"Content-Type":"application/json"})
    return urllib2.urlopen(req).read()

class TestCake(unittest.TestCase):
    def test(self):
        self.assertEqual(send_data(open(os.path.join(os.path.dirname(__file__), "fixtures/cake.json"),"r").read()), "John baked a cake from some ingredients.")
        
class TestIngredients(unittest.TestCase):
    def test(self):
        self.assertEqual(send_data(open(os.path.join(os.path.dirname(__file__), "fixtures/ingredients.json"),"r").read()), "The ingredients were flour, sugar, butter and eggs.")

class TestTense(unittest.TestCase):
    def test(self):
        sentence = {}
        sentence["subject"] = "John"
        sentence["verb"] = "kick"
        sentence["object"] = "Dave"

        sentence["features"] = {"tense":"past"}
        self.assertEqual(send_data(json.dumps({"sentence":sentence})), "John kicked Dave.")

        sentence["features"] = {"tense":"present"}
        self.assertEqual(send_data(json.dumps({"sentence":sentence})), "John kicks Dave.")
        
        sentence["features"] = {"tense":"future"}
        self.assertEqual(send_data(json.dumps({"sentence":sentence})), "John will kick Dave.")
