#!/usr/bin/env python
# coding:utf-8

"""sparql11 server module"""

__author__ = "Thomas Scharrenbach"
__copyright__ = "Copyright (C) 2014 Thomas Scharrenbach"
__license__ = "Apache License v2"
__version__ = "0.0.1"

import argparse

from rdflib import Graph

from .SPARQLEndpoint import SPARQLEndpoint

import traceback

import logging as log

import json

import rdflib

from .QueryHandler import QueryHandler

def parse_args(args):
	"""Parse command line arguments for generating a SPARQL endpoint.

	:param args:
	:return:
	"""
	parser = argparse.ArgumentParser()
	parser.add_argument(
		"dataset",
		help="list of rdf graphs",
		type=json.loads,
		default={})
	parser.add_argument(
		"--hostname",
		help="hostname",
		required=False,
		default='localhost')
	parser.add_argument(
		"--port",
		help="port number",
		type=int,
		required=False,
		default=3030)
	return parser.parse_args(args=args)


def endpoint(dataset, hostname='localhost', port=3030, queryHandlerClass=QueryHandler):
	"""sparql11.endpoint(dataset, hostname='localhost', port=3030, queryHandlerClass=sparql11.QueryHandler)
	Creates a SPARQL endpoint from a dataset of RDF graphs.

	:param dataset:
	:param hostname:
	:param port:
	:param queryHandlerClass:
	:return:
	"""
	server_address = (hostname, port)
	server = SPARQLEndpoint(server_address, QueryHandler)

	t = type(dataset)

	if t is str:
		try:
			server.addGraph(Graph().parse(dataset, format='xml'))
		except:
			try:
				server.addGraph(Graph().parse(dataset, format='turtle'))
			except:
				raise Exception('Could not add graph <{}>'.format(dataset))
	elif t is rdflib.Graph:
		server.addGraph(dataset)
	else:
		for key, value in dataset.items():
			try:
				server.addGraph(Graph().parse(value, format='xml'), key)
			except:
				try:
					server.addGraph(Graph().parse(value, format='turtle'), key)
				except:
					import sys
					traceback.print_exc(file=sys.stdout)
					log.error('Could not add graph <{}>'.format(value))
	return server



