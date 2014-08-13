#!/usr/bin/env python3
# coding:utf-8

"""sparql11 Sparql11HTTPRequestHandler class"""

__author__ = "Thomas Scharrenbach"
__copyright__ = "Copyright (C) 2014 Thomas Scharrenbach"
__license__ = "Apache License v2"
__version__ = "0.0.1"

from http.server import BaseHTTPRequestHandler

import cgi

from urllib.parse import urlparse, parse_qs

from rdflib import Graph, URIRef

import rdflib.plugins.sparql

from rdflib.plugins.sparql.algebra import translateQuery
from rdflib.plugins.sparql.parser import parseQuery

from rdflib.query import ResultSerializer
from rdflib.serializer import Serializer

import rdflib.plugin

import traceback

import sys




class QueryHandler(BaseHTTPRequestHandler):
	"""Handles requests according to the SPARQL1.1 Protocol."""


	def _do_request(self, request_params):
		"""Execute the actions for a SPARQL query request.

		:param request_params:
		:return:
		"""
		query_results = None

		try:
			sparql_query = request_params.get('query')[0]

			if 'default-graph-uri' in request_params:
				self.send_error(
					code=400,
					message='This service does not allow protocol clients to specify the RDF Dataset')
				return

			if 'named-graph-uri' in request_params:
				self.send_error(
					code=400,
					message='This service does not allow protocol clients to specify the RDF Dataset')
				return

			# TODO Check that body contains no content
			# if self.rfile.closed:
			# 	self.send_error(code=500)
			# 	return

			# check response formats
			if 'format' in request_params:
				result_format = request_params.get('format')[0]
			query_tree = parseQuery(sparql_query)
			query_object = translateQuery(query_tree)
			query_type = query_object.algebra.name
			if query_type in ['ConstructQuery', 'DescribeQuery']:
				try:
					rdflib.plugin.get(result_format, Serializer)
				except:
					# traceback.print_exc(file=sys.stdout)
					result_format = 'application/rdf+xml'

			else:
				try:
					rdflib.plugin.get(result_format, ResultSerializer)
				except:
					# traceback.print_exc(file=sys.stdout)
					result_format = 'application/sparql-results+xml'

		except:
			#traceback.print_exc(file=sys.stdout)
			self.send_error(code=500)
			return

		try:
			query_results = self.server.dataset.query(sparql_query)
		except:
			traceback.print_exc(file=sys.stdout)
			self.send_error(code=500)
			return


		enc = 'UTF-8'
		self.send_response(200)
		self.send_header('Content-type', '{}; charset={}'.format(result_format, enc))
		self.end_headers()
		if query_results is not None:
			query_results.serialize(destination=self.wfile, encoding=enc, format=result_format)
		self.wfile.flush()


	def do_GET(self):
		"""Perform a SPARQL query GET request.

		:return:
		"""
		try:
			# Check that message body is empty.
			length = self.headers['Content-Length']
			if length is not None and length > 0:
				#traceback.print_exc(file=sys.stdout)
				self.send_error(code=500)
				return

			request = urlparse(self.path)
			request_params = parse_qs(request.query)
			self._do_request(request_params=request_params)
		except:
			#traceback.print_exc(file=sys.stdout)
			self.send_error(code=500)
			return




	def do_POST(self):
		"""Perform a SPARQL query POST request.

		:return:
		"""
		try:
			length = self.headers['Content-Length']
			ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
			if ctype == 'multipart/form-data':
				postvars = cgi.parse_multipart(self.rfile, pdict)
			elif ctype == 'application/x-www-form-urlencoded':
				postvars = parse_qs(self.rfile.read(int(length)).decode('utf-8'), keep_blank_values=1)
			else:
				postvars = {}

			print('DATA: {}'.format(postvars))
		except:
			#traceback.print_exc(file=sys.stdout)
			self.send_error(code=500)
			return

		self._do_request(request_params=postvars)