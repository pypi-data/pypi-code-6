#!/usr/bin/python
#
# Materialize.py , recreates .env files from etcd 
# (C) Department of Parks and Wildlife(DPAW) 2014 
# Go look up GPL 3 and use that as the license.
#
# Authors: Shayne O'Neill 
import os
import sys
import etcpy

def constpath(cluster,app,key,common=False):
	if not common:
		return "/"+cluster+"/"+app+"/"+key
	if common:
		return "/"+cluster+"/common/"+key

def dematerialize(etchost,cluster,app):
	import etcpy
	e = etcpy.Etcd(etchost, secure=False)
	f = file('.env','r')
	for line in f.readlines():
		l = line.strip()
		#Get rid of export commands if necessary
		toks = l.split(' ')
		if toks[0]=='export':
			del(toks[0])
		l = ' '.join(toks)
		#Deal with #
		toks = l.split('#')
		common=False
		if len(toks) > 1:
			if toks[1]=='common':
				common=True
		l = toks[0]
		#Now split on '='
		toks = l.split('=')
		e[constpath(cluster,app,toks[0],common)]=toks[1]




def constpath2(cluster,app,common=False):
	if not common:
		return "/"+cluster+"/"+app
	if common:
		return "/"+cluster+"/common"

def rematerialize(etchost,cluster,app):
	import etcpy
	outarray={}
	e = etcpy.Etcd(etchost, secure=False)
	f = file('.env','w')
	path = constpath2(cluster,app,False)
	keyvals = e[path]
	for item in keyvals:
		f.write ( item.key.split('/')[-1]+"="+item.value+"\n" )
		os.environ[item.key.split('/')[-1].replace(' ','')] = item.value.replace('\"','')
	path = constpath2(cluster,app,True)
	keyvals = e[path]
	for item in keyvals:
		f.write( item.key.split('/')[-1]+"="+item.value+" #common\n" )
		os.environ[item.key.split('/')[-1]] = item.value.replace('\"','')
	f.close()


def magic_rematerialize(app):
	etchost='localhost'
	if os.environ.has_key('etchost'):
	        etchost = os.environ['etchost']
	cluster=os.environ['etccluster']
	rematerialize(etchost,cluster,app)
	
