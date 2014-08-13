#!/usr/bin/env python3
# coding:utf-8

"""sparql11 SPARQLEndpoint class"""

__author__ = "Thomas Scharrenbach"
__copyright__ = "Copyright (C) 2014 Thomas Scharrenbach"
__license__ = "Apache License v2"
__version__ = "0.0.1"

from http.server import HTTPServer

from rdflib.graph import ConjunctiveGraph

import rdflib

from rdflib.query import ResultSerializer

import threading

class SPARQLEndpoint(HTTPServer):
	"""SPARQL Protocol Endpoint

	"""

	def server_activate(self):
		"""Register serializers and initialize dataset.

		:return:
		"""
		super(SPARQLEndpoint, self).server_activate()
		rdflib.plugin.register(
			'application/sparql-results+xml', ResultSerializer,
			'rdflib.plugins.sparql.results.xmlresults', 'XMLResultSerializer')
		rdflib.plugin.register(
			'text/plain', ResultSerializer,
			'rdflib.plugins.sparql.results.txtresults', 'TXTResultSerializer')
		rdflib.plugin.register(
			'application/json', ResultSerializer,
			'rdflib.plugins.sparql.results.jsonresults', 'JSONResultSerializer')
		rdflib.plugin.register(
			'text/csv', ResultSerializer,
			'rdflib.plugins.sparql.results.csvresults', 'CSVResultSerializer')

		self.__dataset = ConjunctiveGraph()
		self.__thread = threading.Thread(target=self.serve_forever, daemon=True)


	def addGraph(self, g, iri=None):
		if iri is None or iri == 'default':
			for s, p, o in g:
				self.__dataset.add((s, p, o))
		else:
			for s, p, o in g:
				self.__dataset.add((iri, s, p, o))

	def start(self):
		self.__thread.start()

	def isAlive(self):
		return self.__thread and self.__thread.isAlive()

	def shutdown(self):
		super(SPARQLEndpoint, self).shutdown()
		self.__thread.join()


	def __exit__(self, exc_type, exc_val, exc_tb):
		if self.isAlive():
			self.shutdown()

	@property
	def dataset(self):
		return self.__dataset
