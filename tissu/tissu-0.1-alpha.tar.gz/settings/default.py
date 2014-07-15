# -*- coding: utf-8 -*-
# generate with tissu                
import os

PROJECT_PATH =  os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

# Sample of configuration
#
# A = { 
#  "user" : "foo",
#  "hostname" : "localhost",
#  "password": "password",
# }
# 
# B = { 
#  "user" : "bar",
#  "hostname" : "server.example.org",
#  "key": "/home/bar/.ssh/id_rsa.pub"
# 
# }
# 
# C = { 
#  "user" : "john",
#  "hostname" : "server2.example.org",
#  "port": "22000",
#  "password" : "supermario",
# }
# 
# FABRIC_ROLES = {
#     "db":       [A],
#     "web":      [B,C],
# }
# 
FABRIC_ROLES = {}
