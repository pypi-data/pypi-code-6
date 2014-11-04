#!/usr/bin/env python

from clam.common.client import CLAMClient

clamclient = CLAMClient("https://anaproy.nl/clamtest/",None,None,True)

#index of all projects
print "INDEX OF ALL PROJECTS"
index = clamclient.index()
for project in index.projects:
    print "\t" + project


